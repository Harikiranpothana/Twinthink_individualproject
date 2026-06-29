import faiss
import numpy as np
import os
import pickle

from services.embedding_service import generate_embeddings


# =========================
# PATH SETUP
# =========================
FAISS_FOLDER = "database/faiss_index"
INDEX_PATH = os.path.join(FAISS_FOLDER, "index.faiss")
CHUNKS_PATH = os.path.join(FAISS_FOLDER, "chunks.pkl")


# =========================
# SAVE TO FAISS
# =========================
def save_to_faiss(chunks, embeddings):

    os.makedirs(FAISS_FOLDER, exist_ok=True)

    embeddings = np.array(embeddings, dtype=np.float32)

    if len(embeddings) == 0:
        return

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)


# =========================
# LOAD FAISS SAFE
# =========================
def load_faiss_index():

    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        return None, None

    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


# =========================
# SEARCH FUNCTION (FIXED + SAFE)
# =========================
def search_similar_chunks(query, top_k=3):

    index, chunks = load_faiss_index()

    if index is None or chunks is None:
        return []

    # generate query embedding safely
    query_embedding = generate_embeddings([query])

    query_embedding = np.array(query_embedding, dtype=np.float32)

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if 0 <= idx < len(chunks):
            results.append(chunks[idx])

    return results