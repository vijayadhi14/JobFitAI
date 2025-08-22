from sentence_transformers import SentenceTransformer, util

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        """
        Load the embedding model.
        """
        print(f"Loading embedding model: {model_name} ...")
        self.model = SentenceTransformer(model_name)

    def encode_text(self, texts):
        """
        Encode a single string or list of strings into embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)

    def compute_similarity(self, text1, text2) -> float:
        """
        Compute cosine similarity between two texts.
        Returns value in [0,1].
        """
        emb1 = self.encode_text(text1)
        emb2 = self.encode_text(text2)
        sim = util.cos_sim(emb1, emb2).item()
        return max(0.0, min(1.0, sim))
