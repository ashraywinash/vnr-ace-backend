# agents/classwork/mail_automation/services.py

class LLMService:
    def invoke_structured(self, system_prompt, user_prompt, schema):
        raise NotImplementedError

class EmailService:
    def send_email(self, recipients, subject, body):
        """
        Implement using SMTP / SendGrid / AWS SES
        """
        raise NotImplementedError

class AuditRepo:
    def persist(self, events):
        pass