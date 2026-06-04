import os
from pathlib import Path
import streamlit as st
from utils.config import SUPPORTED_EXTENSIONS, TOP_K, VECTOR_STORE_PATH
from rag.pipeline import RAGPipeline
from agents.router_agent import RouterAgent
from agents.retrieval_agent import RetrievalAgent
from agents.summarizer_agent import SummarizerAgent
from agents.quiz_agent import QuizAgent
from agents.doubt_agent import DoubtAgent
from agents.memory_agent import MemoryAgent
from utils.file_helpers import load_document


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def local_css() -> None:
    style_path = Path("assets/style.css")
    if style_path.exists():
        with open(style_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def save_uploaded_files(uploaded_files):
    saved_paths = []
    for uploaded_file in uploaded_files:
        extension = Path(uploaded_file.name).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            continue
        dest = UPLOAD_DIR / uploaded_file.name
        with open(dest, "wb") as out_file:
            out_file.write(uploaded_file.getbuffer())
        saved_paths.append(str(dest))
    return saved_paths


def build_context_from_results(results: str) -> str:
    return results if results else ""


def main():
    st.set_page_config(page_title="AI College Notes Assistant", layout="wide")
    local_css()

    if "memory_agent" not in st.session_state:
        st.session_state.memory_agent = MemoryAgent()
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = RAGPipeline()
    if "last_response" not in st.session_state:
        st.session_state.last_response = ""

    st.sidebar.title("AI College Notes Assistant")
    st.sidebar.markdown("Modern anime-inspired dashboard for study materials and exam prep.")
    st.sidebar.markdown("**Upload supported files:** PDF, PPTX, DOCX, TXT")
    uploaded_files = st.sidebar.file_uploader(
        "Upload lecture materials",
        type=[ext.replace(".", "") for ext in SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
    )

    if uploaded_files:
        if st.sidebar.button("Ingest Uploaded Files"):
            file_paths = save_uploaded_files(uploaded_files)
            if file_paths:
                st.session_state.rag_pipeline.ingest_files(file_paths)
                st.sidebar.success(f"Ingested {len(file_paths)} files into FAISS.")
            else:
                st.sidebar.error("No supported files were uploaded.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Clear Chat History"):
        st.session_state.memory_agent.clear_memory()
        st.session_state.last_response = ""
        st.sidebar.success("Conversation memory cleared.")

    st.sidebar.markdown("### Quick Actions")
    st.sidebar.markdown("- Ask subject doubts\n- Generate summaries\n- Create exam quizzes\n- Review topics by semester")

    st.markdown("# 🎓 AI College Notes Assistant")
    st.markdown(
        "Use the sidebar to upload course documents, then ask questions or generate summaries based on your own notes."
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Ask a question or request a study task", value="Explain the key concepts in the uploaded notes.")
        task = st.selectbox(
            "Choose task",
            ["Auto route", "Summary", "Quiz", "Doubt", "Search", "Exam Prep"],
        )
        if st.button("Run Task"):
            if not query.strip():
                st.warning("Please enter a study question or command.")
            else:
                try:
                    router = RouterAgent()
                    retrieval_agent = RetrievalAgent()
                    summarizer = SummarizerAgent()
                    quiz_agent = QuizAgent()
                    doubt_agent = DoubtAgent()
                    intent = task.lower().replace(" ", "_")
                    if task == "Auto route":
                        intent = router.classify_intent(query)

                    context = retrieval_agent.search_notes(query, top_k=TOP_K)
                    response = ""
                    if intent == "summary":
                        response = summarizer.summarize(context)
                    elif intent == "quiz":
                        response = quiz_agent.generate_quiz(context)
                    elif intent == "doubt":
                        response = doubt_agent.answer_doubt(query, context)
                    elif intent == "search":
                        response = context
                    elif intent == "exam_prep":
                        prep_prompt = (
                            "Create an exam strategy and revision summary from the following notes. "
                            "Organize topics and study priorities."
                        )
                        response = summarizer.summarize(context + "\n\n" + prep_prompt)
                    else:
                        response = summarizer.summarize(context)

                    st.session_state.memory_agent.add_message("user", query)
                    st.session_state.memory_agent.add_message("assistant", response)
                    st.session_state.last_response = response
                except Exception as e:
                    st.error(f"Task failed: {e}")
                    st.session_state.last_response = ""

        if st.session_state.last_response:
            st.markdown("## Assistant Response")
            st.markdown(st.session_state.last_response)

    with col2:
        st.markdown("## Conversation History")
        for item in st.session_state.memory_agent.get_history():
            if item["role"] == "user":
                st.markdown(f"**You:** {item['content']}")
            else:
                st.markdown(f"**Assistant:** {item['content']}")

    st.markdown("---")
    st.markdown("## Semester & Subject Organizer")
    semester = st.selectbox("Select semester", ["Semester 1", "Semester 2", "Semester 3", "Semester 4"])
    subject = st.text_input("Subject or topic", "Data Structures")
    st.markdown(f"**Current view:** {semester} / {subject}")

    if st.button("Generate Revision Plan"):
        context = retrieval_agent.search_notes(f"Create a revision plan for {subject}", top_k=TOP_K)
        plan = summarizer.summarize(context)
        st.markdown("### Revision Plan")
        st.markdown(plan)


if __name__ == "__main__":
    main()
