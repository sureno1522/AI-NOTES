import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np


def _embed_documents(embeddings: Any, texts: list[str]) -> list[list[float]]:
    if hasattr(embeddings, "embed_documents"):
        return embeddings.embed_documents(texts)
    if hasattr(embeddings, "encode"):
        encoded = embeddings.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        if hasattr(encoded, "tolist"):
            return [vector.tolist() for vector in encoded]
        return [list(vector) for vector in encoded]
    raise AttributeError("Provided embeddings object must implement embed_documents() or encode().")


def _embed_query(embeddings: Any, text: str) -> list[float]:
    if hasattr(embeddings, "embed_query"):
        return embeddings.embed_query(text)
    if hasattr(embeddings, "encode"):
        vector = embeddings.encode(text, show_progress_bar=False, convert_to_numpy=True)
        if hasattr(vector, "tolist"):
            vector = vector.tolist()
        if isinstance(vector, list) and vector and isinstance(vector[0], list):
            return vector[0]
        return list(vector)
    raise AttributeError("Provided embeddings object must implement embed_query() or encode().")


class SimpleDocument:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


class FAISSStore:
    def __init__(self, index: faiss.IndexFlatL2, texts: list[str], metadatas: list[dict], embeddings: Any):
        self.index = index
        self.texts = texts
        self.metadatas = metadatas
        self.embeddings = embeddings

    @classmethod
    def from_texts(cls, texts: list[str], embeddings: Any, metadatas: list[dict] | None = None) -> "FAISSStore":
        metadatas = metadatas or [{} for _ in texts]
        if len(texts) != len(metadatas):
            raise ValueError("texts and metadatas must have the same length")

        vectors = _embed_documents(embeddings, texts)
        if len(vectors) == 0:
            raise ValueError("No vectors were created for the provided text chunks.")

        dimension = len(vectors[0])
        index = faiss.IndexFlatL2(dimension)
        array = np.array(vectors, dtype=np.float32)
        index.add(array)

        return cls(index, texts, metadatas, embeddings)

    def add_texts(self, texts: list[str], metadatas: list[dict] | None = None) -> None:
        metadatas = metadatas or [{} for _ in texts]
        if len(texts) != len(metadatas):
            raise ValueError("texts and metadatas must have the same length")

        vectors = _embed_documents(self.embeddings, texts)
        array = np.array(vectors, dtype=np.float32)
        self.index.add(array)
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def save_local(self, path: str | Path) -> None:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "index.faiss"))
        payload = {
            "texts": self.texts,
            "metadatas": self.metadatas,
        }
        with open(path / "store.json", "w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

    @classmethod
    def load_local(cls, path: str | Path, embeddings: Any) -> "FAISSStore" | None:
        path = Path(path)
        if not path.exists() or not (path / "index.faiss").exists() or not (path / "store.json").exists():
            return None

        index = faiss.read_index(str(path / "index.faiss"))
        with open(path / "store.json", "r", encoding="utf-8") as file:
            payload = json.load(file)

        return cls(index, payload.get("texts", []), payload.get("metadatas", []), embeddings)

    def similarity_search_with_score(self, query: str, k: int = 5) -> list[tuple[SimpleDocument, float]]:
        query_vector = np.array([_embed_query(self.embeddings, query)], dtype=np.float32)
        distances, indices = self.index.search(query_vector, k)
        results: list[tuple[SimpleDocument, float]] = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.texts):
                continue
            results.append((SimpleDocument(self.texts[idx], self.metadatas[idx]), float(distance)))
        return results


def create_faiss_store(text_chunks: list[str], embeddings: Any, metadatas: list[dict], vector_path: str) -> FAISSStore:
    store = FAISSStore.from_texts(text_chunks, embeddings, metadatas)
    store.save_local(vector_path)
    return store


def load_faiss_store(vector_path: str, embeddings: Any) -> FAISSStore | None:
    return FAISSStore.load_local(vector_path, embeddings)
