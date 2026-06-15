from pathlib import Path
import json

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = BASE_DIR / "processed" / "chunks.json"
CHROMA_DIR = BASE_DIR / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "student_housing_chunks"

TOP_K = 4


def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    return chunks


def build_vector_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete old collection so reruns do not create duplicate or stale results
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted old collection.")
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        source = chunk["source"]
        chunk_id = chunk["chunk_id"]
        text = chunk["text"]

        ids.append(f"{source}__chunk_{chunk_id}")
        documents.append(text)
        metadatas.append({
            "source": source,
            "chunk_id": chunk_id
        })

    print(f"Embedding {len(documents)} chunks...")
    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        show_progress_bar=True
    ).tolist()

    print("Adding chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Stored {collection.count()} chunks in ChromaDB.")

    return model, collection


def retrieve(query, model, collection, top_k=TOP_K):
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []

    for i in range(len(results["documents"][0])):
        retrieved.append({
            "rank": i + 1,
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved


def print_retrieval_results(query, results):
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    for result in results:
        source = result["metadata"]["source"]
        chunk_id = result["metadata"]["chunk_id"]
        distance = result["distance"]
        text = result["text"]

        print(f"\nRank: {result['rank']}")
        print(f"Source: {source}")
        print(f"Chunk ID: {chunk_id}")
        print(f"Distance: {distance:.4f}")
        print("\nRetrieved chunk:")
        print(text)
        print("-" * 100)


def main():
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    model, collection = build_vector_store(chunks)

    test_questions = [
        "What are the main housing options for students at U.S. universities?",
        "What are the main benefits of living on campus?",
        "What extra costs should students consider before choosing off-campus housing?",
        "Why might an international student choose a homestay?",
        "What should students compare before choosing a housing option?"
    ]

    for question in test_questions:
        results = retrieve(question, model, collection, top_k=TOP_K)
        print_retrieval_results(question, results)


if __name__ == "__main__":
    main()