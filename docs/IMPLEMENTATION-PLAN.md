

**Project:** SkillLoop  
**Version:** 1.0  
**Status:** Draft  
**Goal:** Build a functional MVP using an iterative development workflow.

---

## 1. Implementation Principles

Development must follow these principles:

1. Implement the smallest working version of each feature.
    
2. Work in small, clearly defined tasks.
    
3. Understand the implementation before accepting changes.
    
4. Write tests alongside application code.
    
5. Keep frontend and backend responsibilities separate.
    
6. Validate all AI-generated data.
    
7. Use Git commits to preserve working milestones.
    
8. Do not introduce technologies without a clear requirement.
    
9. Avoid unnecessary cloud infrastructure and costs.
    
10. Require human approval before accepting implementation changes.
    

Claude Code should propose a plan before making significant changes.

## 2. Development Workflow

Each implementation task follows this workflow:

```
Understand the requirement
          |
          v
Review relevant documentation
          |
          v
Create implementation plan
          |
          v
Human approval
          |
          v
Implement changes
          |
          v
Run automated tests
          |
          v
Review code and changes
          |
          v
Human approval
          |
          v
Git commit
```

If tests fail, investigate and correct the implementation before moving forward.

Claude Code must not silently expand the MVP scope.

## 3. Development Phases

### Phase 0 – Project Foundation

**Goal:** Prepare the development environment and project structure.

Tasks:

- Create the Git repository.
    
- Create the frontend application using Next.js, React and TypeScript.
    
- Create the backend application using Python and FastAPI.
    
- Configure Docker Compose.
    
- Configure environment variables.
    
- Add `.env.example`.
    
- Configure `.gitignore`.
    
- Add basic health endpoints.
    
- Verify that frontend and backend run locally.
    

Expected result:

- Frontend starts successfully.
    
- Backend starts successfully.
    
- Docker Compose runs both services.
    
- Backend health endpoint responds successfully.
    

Tests:

- Backend health endpoint test.
    
- Basic frontend startup verification.
    
- Docker Compose startup verification.
    

### Phase 1 – Database and Authentication

**Goal:** Establish persistent storage and secure user authentication.

Tasks:

- Configure Supabase project.
    
- Configure Supabase Auth.
    
- Create database migrations.
    
- Implement `profiles`.
    
- Implement `career_goals`.
    
- Implement initial database constraints.
    
- Configure Row Level Security.
    
- Implement FastAPI JWT validation.
    
- Implement profile endpoints.
    
- Implement career goal endpoints.
    

Expected result:

- Users can register and authenticate.
    
- Users can create and retrieve their career goal.
    
- User data is isolated.
    
- Data persists between sessions.
    

Tests:

- Authentication validation.
    
- Database integration tests.
    
- User ownership tests.
    
- RLS verification.
    
- Career goal constraint tests.
    

### Phase 2 – Competency Map

**Goal:** Generate and manage the user's competency map.

Tasks:

- Implement the AI provider abstraction.
    
- Configure OpenAI API integration.
    
- Implement prompt management.
    
- Implement competency map generation.
    
- Validate structured AI output.
    
- Implement competency persistence.
    
- Implement competency CRUD endpoints.
    
- Build frontend competency map view.
    
- Allow users to edit, add and archive competencies.
    

Expected result:

- User selects a professional role and seniority.
    
- AI generates a competency map.
    
- User can review and modify the proposed map.
    
- Approved competencies are saved in PostgreSQL.
    

Tests:

- AI provider integration tests.
    
- Structured output validation tests.
    
- Competency CRUD tests.
    
- User ownership tests.
    
- Frontend component tests.
    

### Phase 3 – Initial Diagnostic Assessment

**Goal:** Evaluate the user's existing knowledge.

Tasks:

- Implement diagnostic session management.
    
- Implement diagnostic question generation.
    
- Implement assessment state management.
    
- Implement answer submission.
    
- Implement follow-up question generation.
    
- Implement follow-up limits.
    
- Implement assessment evaluation.
    
- Store assessment history.
    
- Build diagnostic frontend workflow.
    

Expected result:

- User can start an initial diagnostic.
    
- AI generates questions related to selected competencies.
    
- User submits explanations.
    
- AI asks follow-up questions when necessary.
    
- AI evaluates answers and identifies knowledge gaps.
    
- Results are stored.
    

Tests:

- Assessment state transition tests.
    
- Follow-up workflow tests.
    
- AI response validation tests.
    
- Assessment persistence tests.
    
- Insufficient evidence handling tests.
    

### Phase 4 – Learning Loop

**Goal:** Allow users to continuously develop individual competencies.

Tasks:

- Implement learning sessions.
    
- Implement learning question generation.
    
- Implement text-based explanations.
    
- Implement AI evaluation.
    
- Implement structured feedback.
    
- Implement competency proficiency calculation.
    
- Implement learning history.
    
- Build frontend learning interface.
    

Expected result:

- User selects a competency.
    
- AI generates a learning question.
    
- User explains the topic.
    
- AI evaluates the explanation.
    
- Competency proficiency is updated based on assessment history.
    
- User can review previous learning sessions.
    

Tests:

- Learning session tests.
    
- Assessment calculation tests.
    
- Historical assessment tests.
    
- Feedback validation tests.
    
- Frontend workflow tests.
    

### Phase 5 – Voice Input

**Goal:** Allow users to explain competencies using their voice.

Tasks:

- Implement browser audio recording.
    
- Implement audio upload endpoint.
    
- Validate audio files.
    
- Integrate OpenAI Speech-to-Text.
    
- Pass transcriptions into the existing assessment workflow.
    
- Handle transcription errors.
    
- Build frontend recording controls.
    

Expected result:

- User can record an explanation.
    
- Backend transcribes the audio.
    
- The transcript follows the same assessment process as text input.
    
- Original audio is not permanently stored by default.
    

Tests:

- Audio validation tests.
    
- Transcription integration tests.
    
- Error handling tests.
    
- Voice-to-assessment workflow tests.
    

### Phase 6 – Recommendations and Progress

**Goal:** Help users decide what to learn next and understand their progress.

Tasks:

- Implement recommendation generation.
    
- Implement recommendation persistence.
    
- Implement recommendation status updates.
    
- Implement competency progress endpoints.
    
- Implement overall progress endpoints.
    
- Build progress dashboard.
    
- Build recommendation interface.
    

Expected result:

- User sees current competency levels.
    
- User can compare current and expected proficiency.
    
- AI recommends relevant competencies.
    
- User can accept or dismiss recommendations.
    
- Learning history remains accessible.
    

Tests:

- Recommendation logic tests.
    
- Progress calculation tests.
    
- API integration tests.
    
- User ownership tests.
    

### Phase 7 – Integration and MVP Stabilization

**Goal:** Verify that the complete MVP works reliably.

Tasks:

- Test complete registration and onboarding flow.
    
- Test competency map generation.
    
- Test initial diagnostic.
    
- Test text learning workflow.
    
- Test voice learning workflow.
    
- Test AI follow-up questions.
    
- Test recommendations.
    
- Test persistence across sessions.
    
- Verify responsive layouts.
    
- Improve loading and error states.
    
- Review security configuration.
    
- Fix identified defects.
    

Expected result:

A functional SkillLoop MVP that supports the complete learning cycle.

## 4. Frontend Development Principles

The frontend uses:

- Next.js.
    
- React.
    
- TypeScript.
    
- Responsive design.
    
- PWA capabilities.
    

Main application areas:

1. Authentication.
    
2. Onboarding.
    
3. Career goal selection.
    
4. Competency map.
    
5. Initial diagnostic.
    
6. Learning interface.
    
7. Progress dashboard.
    
8. Recommendations.
    
9. User settings.
    

The interface must work on desktop and mobile devices.

Desktop and mobile users share the same account and synchronized learning data.

## 5. Backend Development Principles

The backend uses:

- Python.
    
- FastAPI.
    
- Pydantic.
    
- Supabase PostgreSQL.
    
- Supabase Auth.
    
- OpenAI API.
    

Backend responsibilities:

- Authentication and authorization.
    
- Business logic.
    
- Database access.
    
- AI orchestration.
    
- Speech-to-Text integration.
    
- Input validation.
    
- Error handling.
    
- Logging.
    

AI provider communication must remain inside the backend.

## 6. Testing Strategy

Testing should be introduced from the beginning rather than postponed until the end.

### Backend

- Unit tests with pytest.
    
- API tests.
    
- Database integration tests.
    
- Authentication tests.
    
- AI response validation tests.
    
- Assessment workflow tests.
    

### Frontend

- Component tests.
    
- Form validation tests.
    
- User interaction tests.
    
- Critical workflow tests.
    

### End-to-End

Verify the complete user journey:

1. Register.
    
2. Select a professional role.
    
3. Generate competency map.
    
4. Edit and approve the map.
    
5. Complete diagnostic assessment.
    
6. Select a competency.
    
7. Explain a topic.
    
8. Receive AI feedback.
    
9. Review progress.
    
10. Follow a recommendation.
    

AI tests should use deterministic mocked responses for most automated tests. Real provider integration tests should be limited and controlled to manage cost.

## 7. CI/CD and Deployment

Production architecture:

- **Frontend:** Vercel.
    
- **Backend:** AWS container hosting.
    
- **Database and authentication:** Supabase.
    
- **AI provider:** OpenAI API.
    
- **CI/CD:** GitHub Actions.
    

AWS hosting service will be selected before production deployment.

### CI Pipeline

GitHub Actions should:

1. Install dependencies.
    
2. Run backend tests.
    
3. Run frontend tests.
    
4. Run linting and type checks.
    
5. Build frontend.
    
6. Build backend Docker image.
    

### CD Pipeline

Deployment should be introduced after the application passes CI.

Tasks:

- Configure production environment variables.
    
- Configure backend hosting on AWS.
    
- Configure frontend deployment on Vercel.
    
- Configure production Supabase access.
    
- Configure secrets securely.
    
- Verify health endpoints.
    
- Test production authentication and API communication.
    

## 8. Cost Control

The MVP should minimize unnecessary cloud expenses.

Principles:

- Use local Docker Compose for development.
    
- Use Supabase Free plan initially.
    
- Avoid unnecessary AWS resources during local development.
    
- Keep AI requests controlled.
    
- Use mocked AI responses in automated tests.
    
- Track actual AI usage.
    
- Deploy production infrastructure only when needed.
    

Cloud resources must be monitored to prevent unexpected costs.

## 9. Definition of Done

An implementation task is complete when:

- Requirements are satisfied.
    
- Code follows the project architecture.
    
- Relevant tests pass.
    
- No known critical errors remain.
    
- Changes have been reviewed.
    
- Documentation is updated when necessary.
    
- The user has approved the result.
    
- A Git commit records the completed milestone.
    

## 10. MVP Completion Criteria

SkillLoop MVP is considered complete when a user can:

1. Register and log in.
    
2. Select one professional goal and seniority level.
    
3. Generate and edit a competency map.
    
4. Complete an initial diagnostic assessment.
    
5. Learn a competency using text explanations.
    
6. Learn a competency using voice explanations.
    
7. Receive AI evaluation and feedback.
    
8. See current competency proficiency.
    
9. Review learning history.
    
10. Receive and manage AI learning recommendations.
    
11. Continue learning across desktop and mobile devices.
    

All core data must persist between sessions.

The application must enforce user data ownership and pass its critical automated tests.

---

**Document status:** Draft v1.0

**Next step:** Review the implementation plan and prepare the project repository for Phase 0.