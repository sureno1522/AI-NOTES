from rag.pipeline import RAGPipeline


class RetrievalAgent:
    def __init__(self):
        self.pipeline = RAGPipeline()

    def search_notes(self, query: str, top_k: int = 5) -> str:
        results = self.pipeline.retrieve(query, top_k=top_k)
        if not results:
            return "No relevant passages found. Please upload your notes or try a different query."
        response_texts = []
        for item in results:
            source = item["metadata"].get("source", "unknown")
            response_texts.append(f"Source: {source}\n{item['text'][:800]}\n---")
        return "\n\n".join(response_texts)
