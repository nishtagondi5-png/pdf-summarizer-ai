PDF Summarizer AI

AI-Based PDF Summarizer and Question Answering System

About the Project

PDF Summarizer AI is a Python-based web application that helps users understand PDF documents easily. Users can upload a PDF file, generate a summary, and ask questions related to the uploaded document.

Features

- Upload PDF documents.
- Extract text from PDF files.
- Generate AI-based summaries.
- Ask questions from uploaded PDFs.
- Get relevant answers using AI.
- Simple and user-friendly interface.

Technologies Used

- Python
- Streamlit
- Groq API
- Scikit-learn
- PyPDF
- Python-dotenv

Project Structure

- "app.py" – Main application and user interface.
- "ai_engine.py" – AI summary and question-answering logic.
- "pdf_reader.py" – Extracts text from PDF files.
- "requirements.txt" – Contains project dependencies.

Installation

1. Clone the repository.
2. Install the required packages:

pip install -r requirements.txt

3. Configure your Groq API key in the ".env" file using "GROQ_API_KEY".

How to Run

streamlit run app.py

Conclusion

This project makes PDF reading easier by using Artificial Intelligence to summarize documents and answer user questions.
