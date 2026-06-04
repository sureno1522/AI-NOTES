import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")

GEMINI_HOST = os.getenv("GEMINI_HOST", "https://gemini.googleapis.com")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", str(BASE_DIR / "data" / "faiss_store"))
TOP_K = int(os.getenv("TOP_K", "5"))

SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".txt"]
