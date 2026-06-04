from flask import Flask
from ui.streamlit_app import main as run_streamlit

app = Flask(__name__)

@app.route("/")
def index():
    return (
        "<h1>Streamlit deployment not supported on Vercel</h1>"
        "<p>This repository contains a Streamlit app. "
        "Use <code>streamlit run ui/streamlit_app.py</code> locally or deploy to a Streamlit-supporting platform.</p>"
    )

if __name__ == "__main__":
    run_streamlit()
