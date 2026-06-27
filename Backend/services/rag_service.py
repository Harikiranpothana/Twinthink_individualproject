import os
import pickle
import faiss
import numpy as np

from services.embedding_service import model

FAISS_FOLDER = "database/faiss_index"


def retrieve_context(query, top_k=3):

    index_path = os.path.join(
        FAISS_FOLDER,
        "index.faiss"
    )

    chunks_path = os.path.join(
        FAISS_FOLDER,
        "chunks.pkl"
    )

    # Check whether FAISS files exist
    if not os.path.exists(index_path):
        return []

    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load stored chunks
    with open(chunks_path, "rb") as file:
        chunks = pickle.load(file)

    # Convert question into embedding
    query_embedding = model.encode([query])

    # Search similar chunks
    distances, indices = index.search(
        np.array(query_embedding, dtype=np.float32),
        top_k
    )

    # Retrieve chunks
    retrieved_chunks = []

    for idx in indices[0]:
        if idx < len(chunks):
            retrieved_chunks.append(chunks[idx])

    return retrieved_chunks