# Makes Alembic detect the models
from core.db import Base
from models.user import User
from models.role import Role
from models.job_notification import JobNotification
from models.company_prep import CompanyPrepQuestion
from models.audit_log import AuditLog
