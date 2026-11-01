
import os
from groq import Groq
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


def ask_ai(prompt, max_tokens=1500):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful academic study assistant. Explain concepts in clear, simple and professional English."
            },
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=max_tokens
    )

    return response.choices[0].message.content


def split_text(text, max_words=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks


def generate_summary(text):
    chunks = split_text(text)

    summaries = []

    for chunk in chunks:
        prompt = f"""
        Summarize this PDF content in simple professional English.
        Include important concepts, definitions and key points.
        Do not add information that is not in the text.

        PDF CONTENT:
        {chunk}
        """
        summaries.append(ask_ai(prompt, max_tokens=700))

    combined_summary = "\n".join(summaries)

    final_prompt = f"""
    Create a clear study summary from these notes.

    Include:
    1. Main topic
    2. Important concepts
    3. Key definitions
    4. 5 to 8 important points

    Keep it concise and easy to understand.

    NOTES:
    {combined_summary}
    """

    return ask_ai(final_prompt, max_tokens=1500)


def retrieve_context(text, question):
    chunks = split_text(text, max_words=250)

    if not chunks:
        return ""

    if len(chunks) == 1:
        return chunks[0]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(chunks + [question])
        scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

        best_indexes = scores.argsort()[-4:][::-1]

        return "\n\n".join(chunks[i] for i in best_indexes)

    except ValueError:
        return text[:10000]


def answer_question(text, question, chat_history=None):
    context = retrieve_context(text, question)

    history_text = ""

    if chat_history:
        for message in chat_history[-6:]:
            history_text += (
                f"{message['role']}: {message['content']}\n"
            )

    prompt = f"""
    You are an intelligent PDF Study Assistant.

    Answer the user's question using the PDF context.
    Understand follow-up questions using the conversation history.
    Explain answers in simple, professional English.
    Use examples when helpful.
    Do not invent facts.
    If the answer is not available in the PDF, clearly say so.

    CONVERSATION HISTORY:
    {history_text}

    RELEVANT PDF CONTENT:
    {context}

    USER QUESTION:
    {question}
    """

    return ask_ai(prompt, max_tokens=1200)
