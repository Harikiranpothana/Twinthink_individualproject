from sentence_transformers import SentenceTransformer
import numpy as np

# =========================
# GLOBAL MODEL CACHE
# =========================
model = None


# =========================
# SAFE MODEL LOADER
# =========================
def load_model():
    global model

    if model is None:
        try:
            print("Loading SentenceTransformer model...")

            model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                cache_folder="./model_cache"
            )

            print("Model loaded successfully.")

        except Exception as e:
            print("Model loading failed:", str(e))
            model = None

    return model


# =========================
# GENERATE EMBEDDINGS (SAFE)
# =========================
def generate_embeddings(chunks):

    if not chunks:
        return np.array([], dtype=np.float32)

    model = load_model()

    if model is None:
        print("WARNING: Embedding model not available.")
        return np.zeros((len(chunks), 384), dtype=np.float32)

    try:
        embeddings = model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return np.array(embeddings, dtype=np.float32)

    except Exception as e:
        print("Embedding generation failed:", str(e))
        return np.zeros((len(chunks), 384), dtype=np.float32)