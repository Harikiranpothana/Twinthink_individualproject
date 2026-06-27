import faiss
import numpy as np
import os
import pickle

FAISS_FOLDER = "database/faiss_index"

os.makedirs(FAISS_FOLDER, exist_ok=True)


def save_to_faiss(chunks, embeddings):

    try:

        if len(chunks) == 0 or len(embeddings) == 0:
            raise ValueError("Empty chunks or embeddings")

        # -------------------------
        # Ensure correct format
        # -------------------------
        embeddings = np.array(embeddings, dtype=np.float32)

        # Optional but improves retrieval quality
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        # -------------------------
        # Create FAISS index
        # -------------------------
        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings)

        # -------------------------
        # Save index
        # -------------------------
        faiss.write_index(
            index,
            os.path.join(FAISS_FOLDER, "index.faiss")
        )

        # -------------------------
        # Save chunks
        # -------------------------
        with open(
            os.path.join(FAISS_FOLDER, "chunks.pkl"),
            "wb"
        ) as f:
            pickle.dump(chunks, f)

        print("FAISS index saved successfully")

    except Exception as e:
        print("Error saving FAISS:", str(e))
        raise e