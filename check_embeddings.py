import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings())

def check_embeddings():
    collection_name = "my_collection"
    collections = client.list_collections()

    print("Available collections:", collections)

    if collection_name not in collections:
        print(f"Collection '{collection_name}' does not exist.")
        return

    collection = client.get_collection(name=collection_name)

    num_embeddings = collection.count()
    print(f"Number of embeddings in collection '{collection_name}':", num_embeddings)

    if num_embeddings > 0:
        print("Embeddings are stored.")
    else:
        print("No embeddings found in the collection.")

if __name__ == "__main__":
    check_embeddings()
