# agents/classwork/faculty_timetable_enquiry/constants.py

AGENT_NAME = "classwork_faculty_timetable_enquiry"

ALLOWED_ROLES = {"student", "faculty", "hod", "admin"}

ALLOWED_INTENTS = {
    "faculty_availability",
    "faculty_venue_lookup",
    "faculty_schedule_lookup",
    "section_timetable_lookup",
    "room_timetable_lookup",
    "subject_timetable_lookup",
}

STANDARD_MESSAGES = {
    "access_denied": (
        "You are not authorized to use the Faculty / Timetable Enquiry Agent."
    ),
    "out_of_scope": (
        "I can only help with faculty schedule, faculty venue, availability, section timetable, "
        "room timetable, and subject timetable related queries."
    ),
    "unsafe_language": (
        "Your request cannot be processed because it contains unsafe, manipulative, or policy-violating language."
    ),
    "clarification_prefix": "I need one clarification before answering:",
    "sql_blocked": (
        "I could not execute that request because the generated query did not pass safety validation."
    ),
    "no_results": "No matching timetable or faculty schedule data was found.",
}

READ_ONLY_SQL_KEYWORDS_ALLOWED = {
    "select",
    "from",
    "where",
    "and",
    "or",
    "order",
    "by",
    "group",
    "limit",
    "offset",
    "join",
    "left",
    "inner",
    "on",
    "as",
    "distinct",
    "ilike",
    "like",
    "in",
    "between",
    "is",
    "null",
    "case",
    "when",
    "then",
    "else",
    "end",
    "asc",
    "desc",
}

SQL_FORBIDDEN_PATTERNS = {
    "insert ",
    "update ",
    "delete ",
    "drop ",
    "alter ",
    "truncate ",
    "create ",
    "grant ",
    "revoke ",
    "commit",
    "rollback",
    "execute ",
    "exec ",
    "copy ",
    "call ",
    ";",
    "--",
    "/*",
    "xp_",
    "information_schema",
    "pg_catalog",
}

DB_SCHEMA_HINT = {
    "faculty_profiles": [
        "faculty_id", "faculty_name", "department", "designation", "email"
    ],
    "faculty_timetable": [
        "faculty_id", "day_of_week", "period_no", "start_time", "end_time",
        "section", "subject_code", "subject_name", "room_no", "building"
    ],
    "section_timetable": [
        "section", "department", "semester", "day_of_week", "period_no",
        "start_time", "end_time", "subject_code", "subject_name",
        "faculty_id", "faculty_name", "room_no", "building"
    ],
    "room_schedule": [
        "room_no", "building", "day_of_week", "period_no", "start_time",
        "end_time", "section", "subject_code", "subject_name",
        "faculty_id", "faculty_name"
    ],
}