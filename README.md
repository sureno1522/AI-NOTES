# AI College Notes Assistant

AI College Notes Assistant is a Streamlit-based study assistant designed for college students. Upload lecture materials in PDF, PPTX, DOCX, or TXT format, ingest them into a local vector store, and then ask questions or generate study content with specialized AI agents.

## Features

- Upload and ingest lecture notes in multiple formats
- Convert documents into semantic embeddings
- Store vectors locally in FAISS
- Retrieve relevant passages using RAG
- Generate summaries, quizzes, exam prep plans, and doubt answers
- Maintain chat-style conversation history
- Local UI powered by Streamlit

## Technology Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Ollama or Google Gemini (LLM backend)
- LangChain-style RAG architecture

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example file and edit the values as needed:

```bash
copy .env.example .env
```

Update `.env` for your desired backend:

- `OLLAMA_HOST`, `OLLAMA_MODEL`, `OLLAMA_API_KEY` for local Ollama
- `GEMINI_HOST`, `GEMINI_MODEL`, `GEMINI_API_KEY` for Gemini

> Do not commit your `.env` file or any secret keys to source control.

### 3. Start the app

```bash
streamlit run ui/streamlit_app.py
```

Open the displayed URL in your browser (usually `http://localhost:8501`).

## Usage

1. Upload supported files in the sidebar.
2. Click `Ingest Uploaded Files` to create the FAISS index.
3. Enter a query or select a task.
4. Choose from `Auto route`, `Summary`, `Quiz`, `Doubt`, `Search`, or `Exam Prep`.
5. Review the generated response and conversation history.

## Configuration

Key environment variables in `.env`:

- `OLLAMA_HOST`: Ollama server URL
- `OLLAMA_MODEL`: Local Ollama model name
- `OLLAMA_API_KEY`: Ollama API key (if required)
- `GEMINI_HOST`: Gemini API host
- `GEMINI_MODEL`: Gemini model name
- `GEMINI_API_KEY`: Gemini API key
- `EMBEDDING_MODEL`: Sentence Transformers model for embeddings
- `VECTOR_STORE_PATH`: Local path for FAISS store
- `TOP_K`: Number of retrieval results returned

## Architecture

The app is built around a RAG pipeline and agent workflow:

- `utils/file_helpers.py`: loads documents and splits text into chunks
- `models/embedding_model.py`: creates embeddings for each chunk
- `vectorstore/faiss_store.py`: builds and persists FAISS indexes
- `rag/pipeline.py`: ingests files and retrieves relevant chunks
- `agents/router_agent.py`: determines the best task for the query
- `agents/retrieval_agent.py`: retrieves matching note passages
- `agents/summarizer_agent.py`: generates summaries
- `agents/quiz_agent.py`: generates quizzes
- `agents/doubt_agent.py`: answers direct questions
- `agents/memory_agent.py`: stores chat history
- `ui/streamlit_app.py`: renders the frontend and orchestrates user flow

## Repository Structure

- `agents/`: task-specific AI agents and router
- `assets/`: CSS and presentation assets
- `data/`: uploaded files and FAISS store data
- `docs/`: deployment and project documentation
- `models/`: embedding and LLM service wrappers
- `rag/`: retrieval-augmented generation pipeline
- `ui/`: Streamlit application
- `utils/`: configuration, prompts, and file utilities
- `vectorstore/`: FAISS persistence layer

## Deployment

This repository contains a Streamlit application. Use Streamlit Community Cloud or another Streamlit-friendly host for deployment.

- For local development, install dependencies with `pip install -r requirements.txt` and run:

```bash
streamlit run ui/streamlit_app.py
```

- The root entrypoint `streamlit_app.py` is also available for simpler deployment configuration.

See `docs/deployment.md` for local deployment instructions.

## Troubleshooting

- `Task failed: 404 Client Error`: your Gemini model endpoint is incorrect or unavailable. Check `GEMINI_HOST`, `GEMINI_MODEL`, and the API key.
- `No relevant passages found`: ingest documents first or use a broader query.
- Embeddings or indexing issues: verify `EMBEDDING_MODEL` is installed and accessible.

## Contribution

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a clear description.

## License

Specify your preferred license here, or add one to the repository.
