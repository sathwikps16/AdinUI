from pymilvus import connections, utility

def list_all_collections():
    try:
        # Connect to Milvus
        connections.connect(alias="default", host="localhost", port="19530")  # Update host and port if needed

        # List all collections
        collections = utility.list_collections()
        if collections:
            print("Collections in Milvus:")
            for collection in collections:
                print(f"- {collection}")
        else:
            print("No collections found in Milvus.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect from Milvus
        connections.disconnect("default")


if __name__ == "__main__":
    list_all_collections()


# from pymilvus import connections, utility
 
# # Milvus Connection Setup
# connections.connect(alias="default", host="localhost", port="19530")
 
# # Name of the collection to drop
# collection_name = "other_collection"
 
# # Check if collection exists before trying to remove it
# if utility.has_collection(collection_name):
#     utility.drop_collection(collection_name)
#     print(f"Collection '{collection_name}' has been removed.")
# else:
#     print(f"Collection '{collection_name}' does not exist.")