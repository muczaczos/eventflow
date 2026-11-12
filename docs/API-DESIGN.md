
**Project:** SkillLoop  
**Version:** 1.0  
**Status:** Draft  
**API Style:** REST  
**Backend:** Python + FastAPI  
**Frontend:** Next.js + React + TypeScript  
**API Version:** v1

---

## 1. Purpose

This document defines the REST API contract between the SkillLoop frontend and backend.

It describes:

- Available API endpoints.
    
- HTTP methods.
    
- Request and response structures.
    
- Authentication requirements.
    
- Error handling.
    
- Data validation.
    
- AI operation orchestration.
    

The API must support the complete MVP learning cycle.

## 2. API Principles

The API must follow these principles:

1. Use REST conventions.
    
2. Use JSON for request and response bodies, except file uploads.
    
3. Use consistent naming conventions.
    
4. Validate all incoming data using Pydantic.
    
5. Authenticate protected endpoints using Supabase JWT.
    
6. Enforce user data ownership on the backend.
    
7. Keep AI provider communication inside the backend.
    
8. Return predictable error structures.
    
9. Use UUID identifiers for application entities.
    
10. Version the API using `/api/v1`.
    

Base URL during local development:

```
http://localhost:8000/api/v1
```

Production URL will be configured through environment variables.

## 3. Authentication

Authentication is handled by Supabase Auth.

The frontend obtains an access token after successful authentication and sends it with protected API requests.

Request header:

```
Authorization: Bearer <supabase_access_token>
```

FastAPI must:

1. Extract the JWT.
    
2. Validate its signature and claims.
    
3. Identify the authenticated user.
    
4. Reject invalid or expired tokens.
    
5. Use the authenticated user ID for all ownership checks.
    

The backend must never trust a user ID supplied by the frontend as proof of ownership.

### Authentication Endpoints

Authentication operations are primarily handled directly by Supabase Auth.

FastAPI does not implement its own password management or token generation.

## 4. API Endpoint Overview

|Area|Method|Endpoint|Description|
|---|---|---|---|
|Profile|GET|`/profile`|Get user profile|
|Profile|PATCH|`/profile`|Update user profile|
|Career Goal|POST|`/career-goals`|Create career goal|
|Career Goal|GET|`/career-goals/active`|Get active career goal|
|Career Goal|PATCH|`/career-goals/{id}`|Update career goal|
|Career Goal|POST|`/career-goals/{id}/archive`|Archive career goal|
|Competencies|GET|`/career-goals/{id}/competencies`|List competencies|
|Competencies|POST|`/career-goals/{id}/competencies/generate`|Generate competency map|
|Competencies|POST|`/career-goals/{id}/competencies`|Add competency|
|Competencies|PATCH|`/competencies/{id}`|Update competency|
|Competencies|POST|`/competencies/{id}/archive`|Archive competency|
|Assessment|POST|`/assessments/diagnostic`|Start initial diagnostic|
|Assessment|POST|`/assessments/{id}/items`|Generate next diagnostic question|
|Assessment|GET|`/assessments/{id}`|Get assessment state|
|Assessment|POST|`/assessments/{id}/items/{item_id}/response`|Submit response|
|Assessment|POST|`/assessments/{id}/items/{item_id}/skip`|Skip follow-up question|
|Assessment|GET|`/assessments/{id}/results`|Get diagnostic results|
|Learning|POST|`/learning/sessions`|Start learning session|
|Learning|GET|`/learning/sessions/{id}`|Get learning session|
|Learning|POST|`/learning/sessions/{id}/items`|Generate learning question|
|Learning|POST|`/learning/sessions/{id}/items/{item_id}/response`|Submit learning response|
|Recommendations|GET|`/recommendations`|Get recommendations|
|Recommendations|POST|`/recommendations/generate`|Generate recommendations|
|Recommendations|PATCH|`/recommendations/{id}`|Update recommendation status|
|Progress|GET|`/progress`|Get overall progress|
|Progress|GET|`/progress/competencies`|Get competency progress|
|Speech|POST|`/speech/transcriptions`|Transcribe audio|

This is the proposed MVP endpoint set. Some endpoints may be combined or simplified during implementation if that does not weaken the API contract.

## 5. Profile API

### GET `/profile`

Returns the authenticated user's profile.

Response:

```
{
  "id": "uuid",
  "display_name": "User",
  "preferred_language": "en",
  "created_at": "2026-11-12T10:00:00Z"
}
```

### PATCH `/profile`

Updates the user's profile.

Request:

```
{
  "display_name": "New display name",
  "preferred_language": "en"
}
```

Response:

```
{
  "id": "uuid",
  "display_name": "New display name",
  "preferred_language": "en"
}
```

## 6. Career Goal API

### POST `/career-goals`

Creates a professional development goal.

Request:

```
{
  "target_role": "DevOps Engineer",
  "seniority": "junior",
  "description": "Prepare for a Junior DevOps Engineer position."
}
```

Response:

```
{
  "id": "uuid",
  "target_role": "DevOps Engineer",
  "seniority": "junior",
  "status": "active"
}
```

A user can have only one active career goal.

### GET `/career-goals/active`

Returns the current active goal and its basic information.

### PATCH `/career-goals/{id}`

Updates an existing career goal.

The endpoint must verify that the goal belongs to the authenticated user.

### POST `/career-goals/{id}/archive`

Archives the active career goal.

Historical sessions, assessments and competencies must remain available.

## 7. Competency API

### POST `/career-goals/{id}/competencies/generate`

Requests an AI-generated competency map.

Request:

```
{
  "additional_context": "I have experience with Linux, Docker and Python."
}
```

Response:

```
{
  "competencies": [
    {
      "name": "Linux",
      "description": "Understanding Linux operating systems.",
      "rationale": "Linux is widely used in server infrastructure.",
      "knowledge_type": "application",
      "importance": "critical",
      "expected_level": "intermediate"
    },
    {
      "name": "Docker",
      "description": "Understanding containerization.",
      "rationale": "Docker is commonly used to package and deploy applications.",
      "knowledge_type": "application",
      "importance": "high",
      "expected_level": "intermediate"
    }
  ]
}
```

The generated map is initially returned as a proposal.

The user must be able to review and edit it before the competencies are saved as their active map.

### POST `/career-goals/{id}/competencies`

Adds a user-approved competency.

Request:

```
{
  "name": "Terraform",
  "description": "Infrastructure as Code.",
  "knowledge_type": "application",
  "importance": "high",
  "expected_level": "intermediate"
}
```

### GET `/career-goals/{id}/competencies`

Returns all competencies belonging to the career goal.

### PATCH `/competencies/{id}`

Updates competency information.

### POST `/competencies/{id}/archive`

Archives a competency without deleting its historical assessment data.

## 8. Assessment API

The assessment API supports the initial diagnostic process.

An assessment is a workflow containing questions, user responses, optional follow-up questions and final results.

### POST `/assessments/diagnostic`

Starts an initial diagnostic for the active career goal.

Request:

```
{
  "career_goal_id": "uuid"
}
```

Response:

```
{
  "id": "uuid",
  "session_type": "initial_diagnostic",
  "status": "in_progress",
  "current_stage": 1
}
```

### POST `/assessments/{id}/items`

Requests the next diagnostic question.

Response:

```
{
  "item_id": "uuid",
  "competency_id": "uuid",
  "question": "Explain the difference between a Docker image and a container.",
  "status": "awaiting_response"
}
```

The backend selects the next competency and generates a relevant question.

### POST `/assessments/{id}/items/{item_id}/response`

Submits a user response.

Request:

```
{
  "response_text": "An image is a template used to create containers.",
  "input_type": "text"
}
```

Response when a follow-up is required:

```
{
  "assessment_status": "awaiting_follow_up",
  "follow_up": {
    "question": "Can multiple containers be created from the same image?"
  }
}
```

Response when assessment is completed:

```
{
  "assessment_status": "completed",
  "evaluation": {
    "technical_correctness": {
      "score": 3,
      "reason": "The explanation is technically correct."
    },
    "conceptual_understanding": {
      "score": 2,
      "reason": "The basic concept is understood."
    },
    "completeness": {
      "score": 2,
      "reason": "Some important details are missing."
    },
    "clarity": {
      "score": 4,
      "reason": "The explanation is clear."
    }
  },
  "feedback": "Good starting explanation. You should explore how containers use images."
}
```

The backend must preserve the complete assessment history, including follow-up questions and answers.

### POST `/assessments/{id}/items/{item_id}/skip`

Allows the user to skip a follow-up question.

The system must preserve the distinction between insufficient evidence and incorrect knowledge.

### GET `/assessments/{id}`

Returns the current assessment state.

This endpoint allows users to continue an unfinished assessment after leaving the application.

### GET `/assessments/{id}/results`

Returns the completed diagnostic results, including:

- Assessed competencies.
    
- Individual assessment results.
    
- Current proficiency levels.
    
- Identified knowledge gaps.
    
- Suggested next steps.
    

## 9. Learning API

The learning API supports the ongoing learning cycle.

### POST `/learning/sessions`

Starts a learning session.

Request:

```
{
  "career_goal_id": "uuid",
  "competency_id": "uuid"
}
```

Response:

```
{
  "id": "uuid",
  "competency_id": "uuid",
  "status": "in_progress"
}
```

### POST `/learning/sessions/{id}/items`

Generates a question or explanation prompt for the selected competency.

Response:

```
{
  "item_id": "uuid",
  "question": "Explain how Docker volumes work and when you would use them."
}
```

### POST `/learning/sessions/{id}/items/{item_id}/response`

Submits the user's explanation.

The response follows the same assessment workflow as the diagnostic process:

- Analyze response.
    
- Request follow-up if necessary.
    
- Evaluate the explanation.
    
- Store assessment history.
    
- Update competency proficiency.
    
- Generate recommendations when appropriate.
    

### GET `/learning/sessions/{id}`

Returns the learning session and its current state.

## 10. Recommendation API

### GET `/recommendations`

Returns recommendations for the authenticated user.

Optional query parameters:

- `status`
    
- `limit`
    
- `offset`
    

Response:

```
{
  "items": [
    {
      "id": "uuid",
      "competency_id": "uuid",
      "competency_name": "Docker",
      "reason": "Your recent explanations show gaps in understanding Docker networking.",
      "priority": "high",
      "status": "pending"
    }
  ],
  "total": 1
}
```

### POST `/recommendations/generate`

Requests updated recommendations based on current competency data and assessment history.

### PATCH `/recommendations/{id}`

Updates recommendation status.

Request:

```
{
  "status": "accepted"
}
```

Allowed statuses:

- `pending`
    
- `accepted`
    
- `completed`
    
- `dismissed`
    

## 11. Progress API

### GET `/progress`

Returns an overview of the user's learning progress.

Response:

```
{
  "career_goal": {
    "target_role": "DevOps Engineer",
    "seniority": "junior"
  },
  "competencies_total": 10,
  "competencies_assessed": 7,
  "competency_levels": {
    "not_assessed": 3,
    "beginner": 2,
    "intermediate": 4,
    "advanced": 1
  },
  "completed_sessions": 12
}
```

### GET `/progress/competencies`

Returns detailed competency progress.

Response:

```
{
  "items": [
    {
      "competency_id": "uuid",
      "name": "Docker",
      "expected_level": "intermediate",
      "current_level": "beginner",
      "last_assessed_at": "2026-11-12T10:00:00Z"
    }
  ]
}
```

Current proficiency must be calculated from assessment history according to the rules defined in `AI-ASSESSMENT-DESIGN.md`.

## 12. Speech API

### POST `/speech/transcriptions`

Accepts an audio file and returns its transcription.

Content type:

```
Content-Type: multipart/form-data
```

Form field:

- `file` — audio recording.
    

Response:

```
{
  "transcription": "Explain how Docker containers work.",
  "language": "en"
}
```

The transcription is then submitted through the normal assessment workflow.

The backend must validate file size, format and duration before processing.

Audio is not permanently stored by default.

## 13. Error Handling

All API errors must use a consistent response structure.

Example:

```
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The submitted data is invalid.",
    "details": [
      {
        "field": "seniority",
        "message": "Unsupported seniority level."
      }
    ],
    "request_id": "uuid"
  }
}
```

Recommended HTTP status codes:

|Status|Meaning|
|---|---|
|200|Successful request|
|201|Resource created|
|204|Successful request without response body|
|400|Invalid operation|
|401|Authentication required|
|403|Insufficient permissions|
|404|Resource not found|
|409|Resource conflict|
|422|Request validation error|
|429|Rate limit exceeded|
|500|Internal server error|
|502|AI provider returned an invalid or unsuccessful response|
|503|External service temporarily unavailable|
|504|External service timeout|

Error messages must not expose API keys, internal stack traces or sensitive information.

## 14. Security

All protected endpoints must:

- Require a valid Supabase JWT.
    
- Verify resource ownership.
    
- Validate request payloads.
    
- Apply appropriate rate limits.
    
- Avoid exposing internal AI provider details.
    
- Protect sensitive application data.
    

The frontend must never communicate directly with OpenAI using a secret API key.

The backend must never trust a user ID supplied in the request body.

## 15. API Documentation

FastAPI should generate OpenAPI documentation automatically.

Development documentation:

```
http://localhost:8000/docs
```

Alternative documentation:

```
http://localhost:8000/redoc
```

All endpoint request and response models should be defined using Pydantic.

The OpenAPI specification should remain synchronized with the actual implementation.

## 16. Out of Scope for MVP

The following API capabilities are postponed:

- Practical exercise submission.
    
- Code execution.
    
- File and document uploads for competency analysis.
    
- Job offer import.
    
- Spaced repetition scheduling.
    
- Gamification.
    
- Knowledge graph queries.
    
- Social features.
    
- Real-time voice conversations.
    

## 17. Implementation Order

Suggested implementation sequence:

1. Configure API versioning and common response models.
    
2. Implement authentication and authorization dependencies.
    
3. Implement profile endpoints.
    
4. Implement career goal endpoints.
    
5. Implement competency endpoints.
    
6. Implement diagnostic assessment endpoints.
    
7. Implement learning session endpoints.
    
8. Implement recommendation endpoints.
    
9. Implement progress endpoints.
    
10. Implement Speech-to-Text endpoint.
    
11. Add endpoint tests.
    
12. Verify generated OpenAPI documentation.
    

---

**Document status:** Draft v1.0

**Next step:** Define the implementation plan, including development phases, dependencies, testing and deployment milestones.