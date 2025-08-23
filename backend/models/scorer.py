from typing import List, Dict
from backend.models.embedder import Embedder
from backend.models.extractor import KeyphraseExtractor

class JobScorer:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = KeyphraseExtractor()
        self.weights = {
            'semantic': 0.7,
            'keyphrase_overlap': 0.3
        }

    def keyphrase_overlap(self, jd_keyphrases: List[str], resume_keyphrases: List[str]) -> float:
        set_jd = set(jd_keyphrases)
        set_resume = set(resume_keyphrases)
        if not set_jd or not set_resume:
            return 0.0
        intersection = set_jd.intersection(set_resume)
        union = set_jd.union(set_resume)
        return len(intersection) / len(union)

    def score_resume(self, resume_text: str, jd_text: str) -> Dict:
        jd_keyphrases = self.extractor.extract(jd_text, topk=30)
        resume_keyphrases = self.extractor.extract(resume_text, topk=30)

        semantic_score = self.embedder.compute_similarity(resume_text, jd_text)
        kp_overlap_score = self.keyphrase_overlap(jd_keyphrases, resume_keyphrases)

        final_score = ((self.weights['semantic'] * semantic_score) + (0.5 * self.weights['keyphrase_overlap'] * kp_overlap_score)) / (self.weights['semantic'] + 0.5 * self.weights['keyphrase_overlap'])
        final_score_percent = round(final_score * 100, 2)

        if final_score_percent <= 35:
            status = "Your Resume needs complete reconstruction to better match the Job Description"
        elif final_score_percent <= 65:
            status = "Your Resume needs major changes to better match the Job Description"
        elif final_score_percent <= 80:
            status = "Your Resume Needs some key improvements to better match the Job Description"
        else:
            status = "Your Resume Matches the job description you are Good to go."

        return {
            "final_score": final_score_percent,
            "semantic_score": round(semantic_score * 100, 2),
            "keyphrase_overlap_score": round(kp_overlap_score * 100, 2),
            "status": status
        }
