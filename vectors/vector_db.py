import os
import json
import chromadb

from processing.ocr import extract_text
from processing.cleaner import clean_text
from processing.chunker import chunk_text
from vectors.embedding import create_embeddings

client = chromadb.PersistentClient(path="./chroma_db")
STATE_FILE = "document_state.json"

def get_collection():
    return client.get_or_create_collection(name="documents")

def get_document_state(folder):
    state = {}
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        stat = os.stat(path)
        state[filename] = {"size": stat.st_size, "modified": stat.st_mtime}

    return state

def process_documents(folder):
    current_state = get_document_state(folder)

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            old_state = json.load(file)

        if current_state == old_state:
            print("Documents unchanged. Using existing database.")
            return

    print("Processing documents...")

    try:
        client.delete_collection("documents")
    except Exception:
        pass

    collection = get_collection()
    all_chunks = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if not os.path.isfile(path):
            continue

        print(f"Processing: {filename}")
        text = extract_text(path)
        text = clean_text(text)
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("No documents found.")
        return

    print("Creating embeddings...")
    embeddings = create_embeddings(all_chunks)

    for i, (chunk, embedding) in enumerate(zip(all_chunks, embeddings)    ):
        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embedding.tolist()]
        )

    with open(STATE_FILE, "w") as file:
        json.dump(current_state, file)

    print(f"Processed {len(all_chunks)} chunks.")