# Deployment Guide

This guide explains how to set up and run the AI College Notes Assistant locally.

## Requirements

- Python 3.11 or newer
- `pip` package manager
- Optional: local Ollama installation for LLM inference

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure environment

Create a copy of the environment template:

```bash
copy .env.example .env
```

Then update `.env` for your environment:

- `OLLAMA_HOST`: URL of your Ollama server (e.g. `http://127.0.0.1:11434`)
- `OLLAMA_MODEL`: local Ollama model name
- `OLLAMA_API_KEY`: optional Ollama API key
- `GEMINI_HOST`: Gemini API endpoint
- `GEMINI_MODEL`: Gemini model name
- `GEMINI_API_KEY`: Gemini API key
- `EMBEDDING_MODEL`: embedding model identifier
- `VECTOR_STORE_PATH`: local path for FAISS storage
- `TOP_K`: retrieval result count

> Keep `.env` private and do not commit secret keys.

## 3. (Optional) Start Ollama

If you use Ollama, start the service before running the app.

```bash
ollama pull llama3
ollama serve
```

If your model differs from `llama3`, update `OLLAMA_MODEL` in `.env`.

## 4. Run the app

Launch the Streamlit UI locally:

```bash
streamlit run streamlit_app.py
```

Then open the browser URL shown in the terminal.

> This repository is a Streamlit app. For production deployment, use Streamlit Community Cloud.

## 5. Ingest notes

1. Upload PDF, PPTX, DOCX, or TXT files in the sidebar.
2. Click `Ingest Uploaded Files`.
3. Wait for the vector store to be created.

## 6. Use the app

- Enter a study question or command.
- Select a task from the dropdown.
- Click `Run Task`.
- Review output and conversation history.

## 7. Troubleshooting

- `404 Client Error`: check `GEMINI_HOST`, `GEMINI_MODEL`, and your Gemini configuration. If Gemini is unavailable, use Ollama.
- `No relevant passages found`: verify files were uploaded and ingested, then try a broader query.
- Embedding errors: confirm the `EMBEDDING_MODEL` is available and installed.

## 8. Recommended workflow

1. Configure your backend in `.env`
2. Start Ollama if needed
3. Launch Streamlit
4. Upload and ingest notes
5. Ask questions and generate study content
