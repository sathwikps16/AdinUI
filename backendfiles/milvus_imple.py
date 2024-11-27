from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from sentence_transformers import SentenceTransformer
from PIL import Image
import clip
import numpy as np
from docx import Document
import os
import logging
from PyPDF2 import PdfReader
from fpdf import FPDF  # For generating PDFs
import torch  # Make sure you import torch for device management
 
class MultiDepartmentVectorDB:
    def __init__(self, host='localhost', port='19530'):
        self.host = host
        self.port = port
        
        # Setup logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Connect to Milvus
        self._connect_to_milvus()
        
        # Initialize embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize CLIP model for image embeddings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # Ensure device is set correctly
        self.clip_model, self.preprocess = clip.load("ViT-B/32", self.device)
        
        # Define departments
        self.departments = ['IT', 'FINANCE', 'HR', 'OTHERS']
        
        # Create collections
        self._setup_databases_and_collections()
    
    def _connect_to_milvus(self):
        """Establish connection to Milvus"""
        try:
            connections.disconnect("default")
            connections.connect(host=self.host, port=self.port)
            self.logger.info(f"Connected to Milvus at {self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise
    
    def _setup_databases_and_collections(self):
        """Create collections for each department"""
        for dept in self.departments:
            # Connect to Milvus
            connections.connect(host=self.host, port=self.port)
 
            # Check if collection exists
            collection_name = f"{dept.lower()}_collection"
            if not utility.has_collection(collection_name):
                self._create_collection_if_not_exists(dept)
            else:
                self.logger.info(f"Collection {collection_name} already exists.")
            
            # Load the collection into memory for search
            collection = Collection(collection_name)
            collection.load()  # Ensure collection is loaded
            self.logger.info(f"Collection {collection_name} loaded into memory.")
    
    def _create_collection_if_not_exists(self, dept, dimension=384):
        """Create collection for a specific department"""
        collection_name = f"{dept.lower()}_collection"
        
        try:
            # Define fields
            fields = [
                FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name='filename', dtype=DataType.VARCHAR, max_length=500),
                FieldSchema(name='content', dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=dimension)
            ]
            
            # Create schema
            schema = CollectionSchema(fields, f'{dept}_collection')
            collection = Collection(name=collection_name, schema=schema)
            
            # Create index
            index_params = {
                'metric_type': 'L2',
                'index_type': 'IVF_FLAT',
                'params': {'nlist': 1024}
            }
            collection.create_index(field_name='embedding', index_params=index_params)
            
            self.logger.info(f"Created new collection: {collection_name}")
            return collection
        
        except Exception as e:
            self.logger.error(f"Error creating collection for {dept}: {e}")
            raise
    
    def _extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF"""
        try:
            reader = PdfReader(pdf_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return ""
    
    def _extract_image_embedding(self, image_path):
        """Extract embeddings from an image using CLIP and resize to match Milvus' expected dimension."""
        try:
            image = Image.open(image_path)
            image_input = self.preprocess(image).unsqueeze(0).to(self.device)
 
            with torch.no_grad():
                image_features = self.clip_model.encode_image(image_input)
 
            # Convert to numpy array and flatten the embedding
            image_embedding = image_features.cpu().numpy().flatten()
 
            # Resize (pad or truncate) the embedding to match the Milvus collection dimension (384)
            target_dim = 384
            if len(image_embedding) < target_dim:
                # If embedding is smaller, pad with zeros
                image_embedding = np.pad(image_embedding, (0, target_dim - len(image_embedding)), mode='constant')
            elif len(image_embedding) > target_dim:
                # If embedding is larger, truncate it
                image_embedding = image_embedding[:target_dim]
 
            return image_embedding
 
 
        except Exception as e:
            self.logger.error(f"Error extracting embedding from image {image_path}: {e}")
            return None
    
    def upload_file_to_department(self, department, file_path, is_image=False):
        """Upload file (PDF, DOCX, or image) to specific department's database"""
        department = department.upper()
        if department not in self.departments:
            self.logger.error(f"Invalid department: {department}")
            return False
    
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False
    
        try:
            # Connect to specific department collection
            collection_name = f"{department.lower()}_collection"
            collection = Collection(collection_name)
    
            # Process PDF, DOCX, or image file
            if file_path.endswith('.pdf'):
                text = self._extract_text_from_pdf(file_path)
                if not text.strip():
                    self.logger.error(f"No text extracted from {file_path}")
                    return False
                embedding = self.model.encode(text)
            elif file_path.endswith('.docx'):  # Handle DOCX files
                text = self._extract_text_from_docx(file_path)
                if not text.strip():
                    self.logger.error(f"No text extracted from {file_path}")
                    return False
                embedding = self.model.encode(text)
            elif is_image:
                embedding = self._extract_image_embedding(file_path)
                if embedding is None:
                    return False
            else:
                self.logger.error(f"Unsupported file type: {file_path}")
                return False
    
            # Convert embedding to list
            embedding_list = embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
    
            # Prepare data for Milvus
            data = [
                [os.path.basename(file_path)],  # List of filenames
                [text if not is_image else ""],  # List of content
                [embedding_list]               # List of embeddings
            ]
    
            # Insert data into Milvus
            collection.insert(data)
            collection.flush()
    
            self.logger.info(f"Successfully uploaded {file_path} to {department} collection")
            return True
    
        except Exception as e:
            self.logger.error(f"Error uploading {file_path} to {department} collection: {e}")
            return False


    def _extract_text_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text + '\n'
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from DOCX {docx_path}: {e}")
            return ""
