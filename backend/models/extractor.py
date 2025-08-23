import spacy
from typing import List

class KeyphraseExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text: str, topk: int = 15) -> List[str]:
        if not text or not text.strip():
            return []

        doc = self.nlp(text)
        keyphrases = set()

        for ent in doc.ents:
            if ent.label_ in {"ORG", "PERSON", "GPE", "NORP", "PRODUCT", "WORK_OF_ART", "LANGUAGE", "EVENT"}:
                phrase = ent.text.strip().lower()
                if phrase:
                    keyphrases.add(phrase)

        for chunk in doc.noun_chunks:
            phrase = chunk.text.strip().lower()
            if phrase and phrase not in keyphrases and len(phrase.split()) <= 4:
                keyphrases.add(phrase)

        return list(keyphrases)[:topk]
