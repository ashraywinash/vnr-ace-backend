# agents/placements/resume_feedback/constants.py

AGENT_NAME = "placements_resume_feedback"

ALLOWED_ROLES = {"student", "placement_coordinator", "tpo", "admin"}

ALLOWED_INTENTS = {
    "analyze_resume",
    "resume_followup",
    "resume_improve_section",
    "resume_score_explanation",
}

STANDARD_MESSAGES = {
    "access_denied": "You are not authorized to use the Resume Feedback Agent.",
    "out_of_scope": (
        "I can only help with resume analysis, resume feedback, follow-up questions "
        "about resume strengths/weaknesses, and resume improvement suggestions."
    ),
    "unsafe_language": (
        "Your request cannot be processed because it contains unsafe, manipulative, or policy-violating language."
    ),
    "clarification_prefix": "I need one clarification before continuing:",
    "no_resume": "No resume was provided or linked in the current request.",
    "cached_used": "Using previously stored resume analysis for follow-up.",
    "analysis_complete": "Resume analysis completed successfully.",
}

CACHE_TTL_HOURS = 24 * 14  # 14 days
MAX_MEMORY_ITEMS = 20