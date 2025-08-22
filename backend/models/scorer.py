from typing import List, Dict
from backend.models.embedder import Embedder
from backend.models.extractor import KeyphraseExtractor

DEFAULT_WEIGHTS = {
    "semantic": 0.6,
    "keyphrase": 0.3,
    "role_alignment": 0.1
}

class JobScorer:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = KeyphraseExtractor(embedding_model=self.embedder.model)

    def keyphrase_overlap(self, jd_kp: List[str], resume_kp: List[str]) -> float:
        set_jd = set([k.lower().strip() for k in jd_kp])
        set_res = set([k.lower().strip() for k in resume_kp])
        if not set_jd or not set_res:
            return 0.0
        return len(set_jd & set_res) / len(set_jd | set_res)

    def role_alignment_score(self, resume_text: str, jd_text: str) -> float:
        jd_kp = self.extractor.extract(jd_text)
        resume_kp = self.extractor.extract(resume_text, top_k=30)
        # Simple overlap
        if not jd_kp or not resume_kp:
            return 0.5
        return len(set(jd_kp) & set(resume_kp)) / len(set(jd_kp))

    def score_resume(self, resume_text: str, jd_text: str) -> Dict:
        semantic = self.embedder.compute_similarity(resume_text, jd_text)
        jd_kp = self.extractor.extract(jd_text)
        resume_kp = self.extractor.extract(resume_text, top_k=30)
        keyphrase_overlap_score = self.keyphrase_overlap(jd_kp, resume_kp)
        role_score = self.role_alignment_score(resume_text, jd_text)

        final_score = (
            semantic * DEFAULT_WEIGHTS["semantic"] +
            keyphrase_overlap_score * DEFAULT_WEIGHTS["keyphrase"] +
            role_score * DEFAULT_WEIGHTS["role_alignment"]
        )

        final_score_percent = round(final_score * 100, 2)

        # Professional message only
        if final_score_percent < 30:
            message = "Your resume needs a complete reconstruction to better match the job description."
        elif final_score_percent <50:
            message = "Your resume needs numerous edits to better match the job description."
        elif final_score_percent <75:
            message = "Your resume needs some improvements to better match the job description."
        else:
            message = "Your resume aligns well with the job description. You are good to go!"

        return {
            "final_score": final_score_percent,
            "message": message
        }
