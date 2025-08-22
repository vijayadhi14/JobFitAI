import re
from typing import List

try:
    from keybert import KeyBERT
except ImportError:
    KeyBERT = None

try:
    import spacy
    SPACY_OK = True
except ImportError:
    SPACY_OK = False

class KeyphraseExtractor:
    def __init__(self, embedding_model=None):
        self.kb = KeyBERT(model=embedding_model) if KeyBERT and embedding_model else None
        if SPACY_OK:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                self.nlp = spacy.blank("en")
        else:
            self.nlp = None

    def extract(self, text: str, top_k: int = 15) -> List[str]:
        text = text.replace("\u00a0", " ").strip()
        if not text:
            return []

        # Very short text: use fallback
        if len(text.split()) < 10:
            return self.fallback_extraction(text, top_k)

        # Use KeyBERT if available
        if self.kb:
            try:
                kws = self.kb.extract_keywords(
                    text,
                    keyphrase_ngram_range=(1, 3),
                    stop_words="english",
                    use_maxsum=True,
                    top_n=min(top_k, max(1, len(text.split())))
                )
                if kws:
                    return [kw for kw, score in kws]
                else:
                    return self.fallback_extraction(text, top_k)
            except Exception:
                return self.fallback_extraction(text, top_k)

        # Default fallback
        return self.fallback_extraction(text, top_k)

    def fallback_extraction(self, text: str, top_k: int = 15) -> List[str]:
        """Fallback: spaCy noun chunks or comma/semicolon split"""
        if self.nlp:
            doc = self.nlp(text)
            cands = [chunk.text.lower().strip() for chunk in getattr(doc, "noun_chunks", [])]
            seen = set()
            uniq = []
            for c in cands:
                if c not in seen and len(c) > 2:
                    seen.add(c)
                    uniq.append(c)
            if uniq:
                return uniq[:top_k]
        # Last resort
        cands = re.split(r"[,;]", text)
        return [c.strip().lower() for c in cands if c.strip()]
