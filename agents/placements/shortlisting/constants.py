AGENT_NAME = "placements_shortlisting"

ALLOWED_ROLES = {"placement_coordinator", "tpo", "admin"}

ALLOWED_INTENTS = {
    "shortlist_candidates",
    "refine_shortlist",
    "explain_ranking",
}

STANDARD_MESSAGES = {
    "access_denied": "You are not authorized to use the Shortlisting Agent.",
    "out_of_scope": "I only handle candidate shortlisting based on job descriptions.",
    "no_jd": "Please provide a job description.",
    "no_candidates": "No candidates found in the dataset.",
}