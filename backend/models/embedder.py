from sentence_transformers import SentenceTransformer
import torch

class Embedder:
    def __init__(self, modelname: str = "princeton-nlp/sup-simcse-bert-base-uncased"):
        self.model = SentenceTransformer(modelname)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)

    def encode_text(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, convert_to_tensor=True, show_progress_bar=False, device=self.device, normalize_embeddings=True)

    def compute_similarity(self, text1, text2):
        embeddings = self.encode_text([text1, text2])
        cos_sim = torch.nn.functional.cosine_similarity(embeddings[0], embeddings[1], dim=0)
        return float(cos_sim.clamp(0, 1).item())
