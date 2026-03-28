INTENT_PROMPT = """
Classify:
- shortlist_candidates
- refine_shortlist
- explain_ranking
"""

SHORTLIST_PROMPT = """
Given:
- job description
- candidate profiles

Return ranked candidates with:
- score (0-10)
- reasoning

Do not hallucinate.
"""