from utils.config import VECTOR_STORE_PATH, TOP_K
from utils.file_helpers import load_document, build_text_chunks
from models.embedding_model import EmbeddingService
from vectorstore.faiss_store import FAISSStore


class RAGPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store: FAISSStore | None = None

    def ingest_files(self, file_paths: list[str]) -> FAISSStore:
        documents = [load_document(path) for path in file_paths]
        chunks = build_text_chunks(documents)
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        self.vector_store = FAISSStore.from_texts(texts, self.embedding_service, metadatas)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        return self.vector_store

    def load_store(self) -> FAISSStore | None:
        if self.vector_store is None:
            self.vector_store = FAISSStore.load_local(VECTOR_STORE_PATH, self.embedding_service)
        return self.vector_store

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        store = self.load_store()
        if not store:
            return []
        results = store.similarity_search_with_score(query, k=top_k)
        return [
            {
                "text": doc.page_content,
                "metadata": doc.metadata,
                "score": score,
            }
            for doc, score in results
        ]
