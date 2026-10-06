import chromadb
from vectors.embedding import model

client = chromadb.PersistentClient(path="./chroma_db")

def search(query, n_results=3):
    collection = client.get_collection("documents")
    query_embedding = model.encode([query])
    results = collection.query(query_embeddings=query_embedding.tolist(), n_results=n_results)

    return results["documents"][0]