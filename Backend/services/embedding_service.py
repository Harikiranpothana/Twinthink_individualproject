from sentence_transformers import SentenceTransformer
import numpy as np

# Load model only once
model = SentenceTransformer('all-MiniLM-L6-v2')


def generate_embeddings(chunks):
    """
    Converts text chunks into FAISS-ready embeddings
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,   # IMPORTANT FIX
        normalize_embeddings=True  # improves cosine similarity quality
    )

    return np.array(embeddings, dtype=np.float32)