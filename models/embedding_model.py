from sentence_transformers import SentenceTransformer
from utils.config import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.client = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.client.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return [embedding.tolist() for embedding in embeddings]

    def embed_query(self, text: str) -> list[float]:
        embedding = self.client.encode(text, show_progress_bar=False, convert_to_numpy=True)
        return embedding.tolist()
