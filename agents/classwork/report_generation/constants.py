# agents/classwork/report_generation/constants.py

from pathlib import Path

AGENT_NAME = "classwork_report_generation"

ALLOWED_ROLES = {"faculty", "hod"}

ALLOWED_REPORT_TYPES = {
    "student_list",
    "attendance_report",
    "performance_report",
    "defaulter_report",
    "subject_summary",
    "section_summary",
}

ALLOWED_EXPORT_FORMATS = {"csv", "xlsx"}

DEFAULT_EXPORT_FORMAT = "xlsx"
DEFAULT_PREVIEW_LIMIT = 20

DATASET_REGISTRY = {
    "students": str(Path("data/classwork/students.csv")),
    "attendance": str(Path("data/classwork/attendance.csv")),
    "marks": str(Path("data/classwork/marks.csv")),
}

DATASET_ALLOWED_COLUMNS = {
    "students": {
        "student_id",
        "name",
        "department",
        "section",
        "semester",
        "regulation",
        "batch",
        "gender",
    },
    "attendance": {
        "student_id",
        "subject_code",
        "subject_name",
        "attendance_percent",
        "classes_conducted",
        "classes_attended",
        "faculty_name",
    },
    "marks": {
        "student_id",
        "subject_code",
        "subject_name",
        "internal_1",
        "internal_2",
        "assignment_marks",
        "avg_marks",
        "grade",
        "faculty_name",
    },
}

STANDARD_MESSAGES = {
    "access_denied": (
        "You are not authorized to use the Report Generation Agent. "
        "This feature is restricted to faculty and HOD users only."
    ),
    "out_of_scope": (
        "I can only help with classwork report generation, student list generation, "
        "attendance summaries, marks/performance reports, section summaries, and related academic reporting."
    ),
    "unsafe_language": (
        "Your request cannot be processed because it contains unsafe, manipulative, "
        "or policy-violating language."
    ),
    "clarification_prefix": "I need one clarification before generating the report:",
    "approval_prefix": "Preview is ready and awaiting approval.",
    "validation_failed": "The report could not be generated because validation failed.",
}