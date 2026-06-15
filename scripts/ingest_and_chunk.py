from pathlib import Path
from pypdf import PdfReader
import re
import json

DOCUMENTS_DIR = Path("documents")
OUTPUT_DIR = Path("processed")
OUTPUT_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 400      # about 400 words/tokens
CHUNK_OVERLAP = 75    # about 75 words/tokens overlap


def load_txt(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")

    # Remove common junk lines from web/PDF exports
    junk_patterns = [
        "advertisement",
        "register free",
        "sign up",
        "subscribe",
        "newsletter",
        "cookie",
        "privacy policy",
        "terms and conditions",
        "terms & conditions",
        "share this",
        "related articles",
        "you may also like",
        "latest posts",
        "read more",
        "follow us",
        "contact",
        "about us",
        "copyright",
        "all rights reserved",
        "facebook",
        "instagram",
        "linkedin",
        "twitter",
        "tiktok",
        "youtube",
        "sponsored",
        "shop",
        "cart",
        "apply now",
        "free evaluation",
        "our programs",
        "offerings",
        "resources",
        "we value your privacy",
        "accept all",
        "reject all",
        "customize",
    ]

    cleaned_lines = []

    for line in text.splitlines():
        line_clean = line.strip()

        if not line_clean:
            continue

        lower_line = line_clean.lower()

        # Skip lines that are likely website boilerplate
        if any(pattern in lower_line for pattern in junk_patterns):
            continue

        # Skip very short navigation-like lines
        if len(line_clean) < 3:
            continue

        cleaned_lines.append(line_clean)

    text = "\n".join(cleaned_lines)

    # Remove repeated spaces and excessive blank lines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():
        if file_path.suffix.lower() == ".txt":
            raw_text = load_txt(file_path)
        elif file_path.suffix.lower() == ".pdf":
            raw_text = load_pdf(file_path)
        else:
            continue

        cleaned = clean_text(raw_text)

        documents.append({
            "source": file_path.name,
            "text": cleaned
        })

    return documents


def main():
    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })
            
    # Remove bad/noisy chunks after inspection
    bad_chunks = {
        ("source10_illustrarch.txt", 5),
        ("source2_study_in_usa.txt", 2),
        ("source3_iefa.pdf", 6),
        ("source3_iefa.pdf", 7),
        ("source5_college_raptor.pdf", 5),
        ("source6_onlinemacha_forum.pdf", 9),
        ("source9_keystone_sports.pdf", 2),
        ("source9_keystone_sports.pdf", 3),
    }

    all_chunks = [
        chunk for chunk in all_chunks
        if (chunk["source"], chunk["chunk_id"]) not in bad_chunks
    ]

    # Re-number chunk_id within each source after filtering
    source_counters = {}

    for chunk in all_chunks:
        source = chunk["source"]

        if source not in source_counters:
            source_counters[source] = 0

        chunk["chunk_id"] = source_counters[source]
        source_counters[source] += 1        

    output_path = OUTPUT_DIR / "chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved chunks to: {output_path}")

    print("\n--- 5 Representative Chunks ---\n")

    for chunk in all_chunks[:5]:
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"][:1000])
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()