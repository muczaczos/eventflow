# SkillLoop – Architecture

**Version:** 1.0  
**Status:** Draft  
**Product:** SkillLoop – Personal Career Knowledge Coach

---

## 1. Architecture Overview

SkillLoop is a responsive web application designed to help users develop, assess, and maintain professional competencies.

The system follows a client-server architecture.

The frontend is responsible for user interaction and presentation. The backend handles business logic, competency assessment, learning processes, and communication with AI services.

The application uses Supabase for authentication and PostgreSQL database services, while OpenAI provides language model and speech-to-text capabilities.

### Main Components

- Frontend: Next.js, React, TypeScript.
    
- Backend: Python, FastAPI.
    
- Authentication: Supabase Auth.
    
- Database: Supabase PostgreSQL.
    
- AI: OpenAI API.
    
- Speech processing: OpenAI Speech-to-Text.
    
- Containerization: Docker.
    
- Frontend hosting: Vercel.
    
- Backend hosting: AWS.
    
- CI/CD: GitHub Actions.
    

## 2. High-Level System Architecture

```
flowchart TB
    USER["User - Desktop / Mobile"]
    FRONTEND["Next.js / React / PWA"]
    BACKEND["FastAPI Backend"]
    AUTH["Supabase Auth"]
    DB[("Supabase PostgreSQL")]
    AI["OpenAI API"]
    STT["OpenAI Speech-to-Text"]

    USER --> FRONTEND
    FRONTEND --> AUTH
    FRONTEND --> BACKEND

    BACKEND --> DB
    BACKEND --> AI
    BACKEND --> STT
```

## 3. Frontend

**Technology:** Next.js, React, TypeScript.

The frontend provides the user interface for desktop and mobile devices.

Responsibilities:

- User registration and login.
    
- User profile management.
    
- Competency map visualization and editing.
    
- Competency assessment interface.
    
- Text-based explanations.
    
- Voice recording.
    
- Learning recommendations.
    
- Progress visualization.
    

The frontend communicates with FastAPI for application operations.

Supabase Auth is used for authentication and session management.

The application should support installation as a Progressive Web App (PWA).

## 4. Backend

**Technology:** Python, FastAPI.

The backend is responsible for the application's business logic.

Responsibilities:

- User and profile data access.
    
- Competency map management.
    
- Competency assessment.
    
- Learning session management.
    
- AI service integration.
    
- Evaluation of user explanations.
    
- Learning recommendations.
    
- Progress tracking.
    

The backend acts as the main application API.

AI-related operations should be separated from the core business logic.

## 5. Authentication

**Technology:** Supabase Auth.

Supabase Auth handles:

- User registration.
    
- User login.
    
- Session management.
    
- Password reset.
    
- Authentication tokens.
    

FastAPI validates access tokens before processing protected operations.

The OpenAI API key must remain on the backend and must never be exposed to the frontend.

## 6. Database

**Technology:** Supabase PostgreSQL.

PostgreSQL stores the application's persistent data.

Main data domains:

- Users and profiles.
    
- Professional roles and seniority levels.
    
- Competency maps.
    
- Competencies and relationships.
    
- Assessment questions.
    
- User answers.
    
- AI evaluation results.
    
- Learning sessions.
    
- Learning progress.
    

The database should support future extensions such as practical exercises, spaced repetition, gamification, and knowledge graph visualization.

A separate graph database is not required for the initial architecture.

## 7. AI Service

**Technology:** OpenAI API.

AI functionality is accessed through a dedicated backend service layer.

Responsibilities:

- Generating competency maps.
    
- Generating diagnostic questions.
    
- Evaluating open-ended answers.
    
- Identifying knowledge gaps.
    
- Producing structured feedback.
    
- Recommending learning activities.
    

AI responses should use structured output formats where appropriate.

The backend must validate AI responses before saving or using them.

Model selection and prompt configuration should be centralized to make future changes easier.

## 8. Speech Processing

**Technology:** Browser audio recording and OpenAI Speech-to-Text.

Voice explanation workflow:

1. The user records an explanation in the browser.
    
2. The frontend sends the audio file to FastAPI.
    
3. FastAPI sends the audio to the speech-to-text service.
    
4. The service returns a text transcription.
    
5. The backend passes the transcription to the AI evaluation service.
    
6. The evaluation result and transcription are saved.
    
7. The frontend displays the feedback.
    

Original audio recordings are not stored permanently by default.

Text input and voice input should use the same evaluation process after transcription.

## 9. External Services

Initial external dependencies:

|Service|Responsibility|
|---|---|
|Supabase|Authentication and database|
|OpenAI|Language models and speech-to-text|
|Vercel|Frontend hosting|
|AWS|Backend hosting|
|GitHub|Source code and version control|
|GitHub Actions|CI/CD|

## 10. Deployment Architecture

### Local Development

Docker Compose is used to provide a repeatable development environment.

The local environment includes:

- Next.js frontend.
    
- FastAPI backend.
    

Supabase cloud services and OpenAI API are accessed externally during development.

### Production

- Next.js frontend deployed on Vercel.
    
- FastAPI backend deployed on AWS using Docker.
    
- PostgreSQL hosted by Supabase.
    
- Authentication managed by Supabase Auth.
    
- AI requests processed through OpenAI API.
    

GitHub Actions handles automated testing and deployment workflows.

## 11. Security Principles

- OpenAI API keys are stored only on the backend.
    
- Supabase credentials are configured using environment variables.
    
- FastAPI validates authentication tokens.
    
- Database access must enforce user ownership.
    
- User data must not be accessible to other users.
    
- File and request sizes must be limited.
    
- Input validation is required for all API operations.
    
- Sensitive data must not be written to application logs.
    

## 12. Architecture Principles

1. Keep frontend and backend responsibilities separate.
    
2. Keep AI integration isolated from business logic.
    
3. Use PostgreSQL as the main source of persistent application data.
    
4. Keep authentication delegated to Supabase.
    
5. Prefer simple infrastructure for the initial MVP.
    
6. Avoid unnecessary services and infrastructure costs.
    
7. Design the system so future features can be added without major architectural changes.
    



sequenceDiagram
    actor User
    participant FE as Next.js
    participant API as FastAPI
    participant DB as Supabase PostgreSQL
    participant AI as OpenAI

    User->>FE: Explain a topic
    FE->>API: Submit answer
    API->>AI: Evaluate explanation
    AI-->>API: Structured evaluation
    API->>DB: Save answer and evaluation
    API-->>FE: Feedback and progress
    FE-->>User: Display results

---
Dokument jest dobrym punktem wyjścia, ale nie traktujmy jeszcze wszystkich szczegółów jako ostatecznych.

1. Supabase Security: musimy dokładnie zaprojektować weryfikację JWT i uprawnienia do danych użytkownika.
    
2. AI Service: musimy określić format odpowiedzi AI, walidację i sposób oceniania wiedzy.
    
3. AWS: wybierzemy konkretną usługę do uruchamiania FastAPI, uwzględniając koszty.



**End of Architecture – Version 1.0**