# Frontend Changes for New LangGraph Agents

The backend has been updated with new 7 agents using LangGraph for better reasoning, guardrails, and auditing. These agents are available at new endpoints in the `classwork` and `placements` routers.

## 1. Classwork Agents

### Email Automation Agent
**Endpoint**: `POST /classwork/email-automation`
**Role Required**: `admin`
**Request Body**:
```json
{
  "message": "User query here",
  "approval": "approved" // Optional: Send "approved" or "rejected" when approving a draft
}
```
**Response**:
```json
{
  "reply": "AI response or draft",
  "state": {
    "recipients": ["list"],
    "subject": "subject",
    "body": "email body",
    "approval_required": true/false,
    "email_sent": true/false
  }
}
```

### Faculty Enquiry Agent
**Endpoint**: `POST /classwork/faculty-enquiry`
**Role Required**: `student` or `faculty` or `admin`
**Request Body**:
```json
{
  "message": "Where is Dr. ABC right now?"
}
```

### Report Generation Agent
**Endpoint**: `POST /classwork/report-generation`
**Role Required**: `admin`
**Request Body**:
```json
{
  "message": "Generate a report for CSE 4th year attendance."
}
```

---

## 2. Placements Agents

### Chart Generator Agent
**Endpoint**: `POST /placements/chart-generator`
**Role Required**: `admin`
**Request Body**:
```json
{
  "message": "Show me a bar chart of placements by department.",
  "memory": [] // History for multi-turn chat
}
```
**Response Includes**: `chart_path` (relative path to the generated image).

### Live Dashboard Agent
**Endpoint**: `POST /placements/live-dashboard`
**Role Required**: Any logged in user
**Request Body**:
```json
{
  "message": "What is the average package this year?",
  "memory": []
}
```

### Resume Feedback Agent
**Endpoint**: `POST /placements/resume-feedback`
**Role Required**: Any logged in user
**Request Body**:
```json
{
  "message": "Analyze my resume.",
  "resume_text": "Full text of resume here...",
  "resume_id": "optional_id",
  "memory": []
}
```

### Shortlisting Agent
**Endpoint**: `POST /placements/shortlisting-agent`
**Role Required**: `admin`
**Request Body**:
```json
{
  "message": "Shortlist students for Google SDE role.",
  "jd_text": "Full Job Description text here..."
}
```

---

## Important Notes for Frontend Team
1. **Memory**: For agents like `Chart Generator` and `Resume Feedback`, please maintain the `memory` array from the response and send it back in the next request to maintain context.
2. **Approval Flow**: `Email Automation` and `Report Generation` might require human approval. Check `approval_required` or `waiting_for_human` in the response to show the appropriate UI.
3. **Audit Logs**: All queries are now audited automatically in the `audit_logs` table.
