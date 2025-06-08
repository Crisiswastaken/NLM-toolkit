import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class AgentMemory:
    def __init__(self, persist_directory=".chroma_memory", collection_name="agent_memory"):
        self.client = chromadb.Client(Settings(persist_directory=persist_directory))
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_memory(self, text, metadata=None, id=None):
        embedding = self.embedder.encode([text])[0]
        # Ensure metadata is a non-empty dict with at least one key
        if not isinstance(metadata, dict) or not metadata:
            metadata = {"source": "agent", "date": "2025-05-24"}
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[id or str(hash(text))]
        )

    def query_memory(self, query, n_results=3):
        embedding = self.embedder.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results

    def clear_memory(self):
        self.collection.delete()
