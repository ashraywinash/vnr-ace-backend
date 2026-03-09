# API Documentation for Frontend Integration

## 1. Authentication

### Login
**Endpoint:** `POST /auth/login`
**Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
- `username`: (string) Email address (e.g., `student@vnr.edu.in`)
- `password`: (string) Password (e.g., `student123`)

### 10. Multiple Offers Stats
- **URL**: `/api/charts/multiple-offers`
- **Method**: `GET`
- **Description**: Returns the count of students holding more than one job offer.
- **Response**:
```json
{
  "students_with_multiple_offers": 45
}
```

### 11. AI Dynamic Chart Routing
- **URL**: `/api/charts/dynamic`
- **Method**: `POST`
- **Description**: Accepts a natural language query and uses an LLM to automatically run and return data for the correct chart endpoint.
- **Request Body**:
```json
{
  "query": "Can you show me the branch wise placement statistics?"
}
```
- **Response**: (Varies based on identified chart)
```json
{
  "chart": "branch-wise",
  "data": [
    {
      "branch": "CSE",
      "total": 240,
      "placed": 200,
      "percentage": 83.33
    }
  ]
}
```
*Note: If the chart is unrecognized, it returns `{"error": "...", "chart": "unknown"}`.*
**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 3,
    "email": "student@vnr.edu.in",
    "role": "student"
  }
}
```

**Frontend Implementation Note:**
Store the `access_token` in `localStorage` or `cookies`. You will need to send this token in the `Authorization` header for protected routes.

---

## 2. Classwork (Student)

### Student Chat 
**Endpoint:** `POST /classwork/student/chat`
**Headers:**
- `Authorization`: `Bearer <access_token>`
- `Content-Type`: `application/json`

**Request Body:**
```json
{
  "message": "Where is Dr. Ravi Kumar?"
}
```

**Response:**
```json
{
  "reply": "Dr. Ravi Kumar is in cabin C-201.",
  "metadata": {
    "query": "Where is Dr. Ravi Kumar?"
  }
}
```

## 3. Test Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Student** | `student@vnr.edu.in` | `student123` |
| **Faculty** | `faculty@vnr.edu.in` | `faculty123` |
| **Admin** | `admin@vnr.edu.in` | `admin` |
