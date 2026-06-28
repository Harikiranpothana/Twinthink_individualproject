import faiss
import numpy as np
import os
import pickle
from services.embedding_service import model

FAISS_FOLDER = "database/faiss_index"


def save_to_faiss(chunks, embeddings):

    os.makedirs(FAISS_FOLDER, exist_ok=True)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(
        index,
        os.path.join(FAISS_FOLDER, "index.faiss")
    )

    with open(
        os.path.join(FAISS_FOLDER, "chunks.pkl"),
        "wb"
    ) as f:
        pickle.dump(chunks, f)


# 🔥 THIS IS THE MISSING FUNCTION (FIX)
def search_similar_chunks(query, top_k=3):

    index_path = os.path.join(FAISS_FOLDER, "index.faiss")
    chunks_path = os.path.join(FAISS_FOLDER, "chunks.pkl")

    if not os.path.exists(index_path):
        return []

    index = faiss.read_index(index_path)

    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding, dtype=np.float32),
        top_k
    )

    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results