# Streamlit Community Cloud Deployment

This project is designed to run as a Streamlit application.

## Recommended entrypoint

Use either:

- `streamlit run ui/streamlit_app.py`
- `streamlit run streamlit_app.py`

The root `streamlit_app.py` file is provided to make deployment simpler.

## Deploy on Streamlit Community Cloud

1. Sign in to https://streamlit.io/cloud
2. Click **New app**
3. Choose your GitHub repository
4. Select the branch `master`
5. Set the app file path to:
   - `streamlit_app.py`
6. Click **Deploy**

## Environment variables

Set the following secrets in the Streamlit Cloud app settings:

- `GEMINI_HOST`
- `GEMINI_MODEL`
- `GEMINI_API_KEY`
- `EMBEDDING_MODEL`
- `VECTOR_STORE_PATH`
- `TOP_K`

If you want to use a local Ollama server for local testing only, set:

- `OLLAMA_HOST`
- `OLLAMA_MODEL`
- `OLLAMA_API_KEY`

> Do not set `OLLAMA_HOST` to `http://127.0.0.1:11434` in Streamlit Cloud. That will fail because the cloud app cannot reach your local machine.

## Notes

- This repo requires the `requirements.txt` file to install dependencies.
- Do not commit `.env` secrets to GitHub.
- If you need local testing, run:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
