
import streamlit as st
from pdf_reader import read_pdf
from ai_engine import generate_summary, answer_question

st.set_page_config(
    page_title="AI Smart PDF Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Smart PDF Study Assistant")
st.caption("Upload your PDF, generate summaries and ask questions from your document.")

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(
    "Upload your PDF file",
    type=["pdf"]
)

if uploaded_file:
    if st.button("Read PDF"):
        with st.spinner("Reading your PDF..."):
            st.session_state.pdf_text = read_pdf(uploaded_file)
            st.session_state.summary = ""
            st.session_state.chat_history = []

        st.success("PDF uploaded and read successfully!")

if st.session_state.pdf_text:
    tab1, tab2 = st.tabs(["📖 Summary", "💬 Chat with PDF"])

    with tab1:
        st.subheader("PDF Summary")

        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_summary(
                    st.session_state.pdf_text
                )

        if st.session_state.summary:
            st.markdown(st.session_state.summary)

    with tab2:
        st.subheader("Ask Questions from Your PDF")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask anything about your PDF...")

        if question:
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = answer_question(
                        st.session_state.pdf_text,
                        question,
                        st.session_state.chat_history[:-1]
                    )
                    st.markdown(answer)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer
            })

else:
    st.info("Please upload a PDF and click Read PDF to get started.")
