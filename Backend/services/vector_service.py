import faiss
import numpy as np
import os
import pickle

FAISS_FOLDER = "database/faiss_index"

os.makedirs(FAISS_FOLDER, exist_ok=True)


def save_to_faiss(chunks, embeddings):

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