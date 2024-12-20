from pymilvus import (
    connections,
    utility,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define the schema
fields = [
    FieldSchema(name="email", dtype=DataType.VARCHAR, max_length=255, is_primary=True, auto_id=False),
    FieldSchema(name="chat_history", dtype=DataType.JSON)
]
chat_history_schema = CollectionSchema(fields=fields, description="Schema for chat history collection")

# Define the collection name
collection_name = "chat_history"

# Check if the collection already exists
if utility.has_collection(collection_name):
    print(f"Collection '{collection_name}' already exists. Dropping and recreating it.")
    utility.drop_collection(collection_name)

# Create the new collection
chat_history_collection = Collection(name=collection_name, schema=chat_history_schema)
print(f"Collection '{collection_name}' created successfully.")

# Define the index parameters
index_params = {
    "index_type": "IVF_FLAT",  # Index type, change as needed
    "metric_type": "L2",       # Distance metric: L2 (Euclidean) or IP (Inner Product)
    "params": {"nlist": 128},  # Number of clusters
}

# Create an index on the 'embedding' field
chat_history_collection.create_index(field_name="embedding", index_params=index_params)
print("Index created successfully.")

# Load the collection into memory
chat_history_collection.load()
print(f"Collection '{collection_name}' loaded into memory and ready for querying.")
