# API Documentation for Frontend Integration

## 1. Authentication

### Login
**Endpoint:** `POST /auth/login`
**Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
- `username`: (string) Email address (e.g., `student@vnr.edu.in`)
- `password`: (string) Password (e.g., `student123`)

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
