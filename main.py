from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return (
        "<h1>Streamlit repository deployed on Vercel</h1>"
        "<p>This repo contains a Streamlit app that cannot run directly on Vercel.</p>"
        "<p>Use Streamlit Community Cloud or another Python host for the actual app.</p>"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
