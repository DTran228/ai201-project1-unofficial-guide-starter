from pathlib import Path
import os

import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "student_housing_chunks"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 4
MAX_DISTANCE = 0.60


SYSTEM_PROMPT = """
You are answering questions for an unofficial guide about student housing options at U.S. universities.

You must answer using ONLY the retrieved context chunks provided.
Do not use outside knowledge.
Do not make unsupported claims.
If the retrieved context does not contain enough information to answer the question, say:
"The available documents do not provide enough information to answer that question."

Keep the answer clear, concise, and grounded in the provided documents.
"""


def load_system():
    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY. Add it to your .env file.")

    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = chroma_client.get_collection(COLLECTION_NAME)

    groq_client = Groq(api_key=groq_api_key)

    return embedding_model, collection, groq_client, groq_model


embedding_model, collection, groq_client, groq_model = load_system()


def retrieve_chunks(question):
    query_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        if distance <= MAX_DISTANCE:
            metadata = results["metadatas"][0][i]

            chunks.append({
                "text": results["documents"][0][i],
                "source": metadata["source"],
                "chunk_id": metadata["chunk_id"],
                "distance": distance
            })

    return chunks


def format_context(chunks):
    context_blocks = []

    for i, chunk in enumerate(chunks, start=1):
        context_blocks.append(
            f"""
[Chunk {i}]
Source: {chunk["source"]}
Chunk ID: {chunk["chunk_id"]}
Distance: {chunk["distance"]:.4f}

Text:
{chunk["text"]}
"""
        )

    return "\n---\n".join(context_blocks)


def ask(question):
    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": []
        }

    chunks = retrieve_chunks(question)

    if not chunks:
        return {
            "answer": "The available documents do not provide enough information to answer that question.",
            "sources": []
        }

    context = format_context(chunks)

    user_prompt = f"""
Retrieved context:

{context}

Question:
{question}

Answer using only the retrieved context.
"""

    response = groq_client.chat.completions.create(
        model=groq_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=600
    )

    answer = response.choices[0].message.content

    sources = []

    for chunk in chunks:
        source_label = (
            f"{chunk['source']} | chunk {chunk['chunk_id']} | "
            f"distance {chunk['distance']:.4f}"
        )

        if source_label not in sources:
            sources.append(source_label)

    return {
        "answer": answer,
        "sources": sources
    }


def handle_query(question):
    result = ask(question)

    sources_text = "\n".join([f"- {source}" for source in result["sources"]])

    if not sources_text:
        sources_text = "No sources retrieved."

    return result["answer"], sources_text


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide: Student Housing in the U.S.")
    gr.Markdown(
        "Ask a question about student housing options at U.S. universities. "
        "The answer is generated only from the retrieved documents."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="Example: What are the benefits of living on campus?"
    )

    btn = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources used", lines=6)

    btn.click(
        handle_query,
        inputs=inp,
        outputs=[answer, sources]
    )

    inp.submit(
        handle_query,
        inputs=inp,
        outputs=[answer, sources]
    )


if __name__ == "__main__":
    demo.launch()