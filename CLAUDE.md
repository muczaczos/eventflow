# SkillLoop – Project Instructions

## 1. Project Overview

SkillLoop is a Personal Career Knowledge Coach.

The application helps users prepare for professional roles and develop the competencies required for their target career.

Users select one professional goal and seniority level. AI generates an editable competency map, evaluates the user's knowledge, identifies knowledge gaps and recommends what to learn next.

The MVP focuses on a continuous learning cycle:

1. Select a professional goal.
2. Generate and review a competency map.
3. Complete an initial diagnostic assessment.
4. Learn individual competencies through explanations.
5. Receive AI evaluation and feedback.
6. Track competency progress.
7. Receive learning recommendations.

The product must support both text and voice explanations.

## 2. Project Documentation

The `docs/` directory contains the project's product and technical documentation.

Before implementing a feature, review the relevant documents.

Available documentation:

- `docs/PRODUCT-SPEC.md` – product vision and requirements.
- `docs/MVP-SCOPE.md` – MVP scope and deferred features.
- `docs/ARCHITECTURE.md` – system architecture and technology decisions.
- `docs/USER-FLOWS.md` – user journeys and workflows.
- `docs/DATABASE-DESIGN.md` – database structure and data relationships.
- `docs/AI-ASSESSMENT-DESIGN.md` – AI assessment rules and proficiency levels.
- `docs/AI-SERVICE-DESIGN.md` – AI integration architecture.
- `docs/API-DESIGN.md` – REST API contracts.
- `docs/IMPLEMENTATION-PLAN.md` – development phases and implementation order.

**Documentation rules:**

- Treat project documentation as the source of truth for product and architectural decisions.
- Do not silently change approved requirements.
- Do not introduce features outside the MVP scope.
- If documentation is unclear or contradictory, explain the issue and ask for clarification.
- If an implementation requires changing an architectural decision, propose the change before implementing it.
- Update documentation when an approved implementation changes relevant project behavior or architecture.

## 3. Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Responsive web application
- PWA capabilities

### Backend

- Python
- FastAPI
- Pydantic

### Database and Authentication

- Supabase PostgreSQL
- Supabase Auth
- Row Level Security (RLS)

### AI

- OpenAI API
- Backend AI Service abstraction
- Structured AI outputs
- Pydantic validation
- Versioned prompts

### Infrastructure

- Frontend production hosting: Vercel.
- Backend production hosting: AWS (containerized FastAPI application).
- Database: Supabase managed PostgreSQL.
- Authentication: Supabase Auth.
- AI provider: OpenAI API.
- CI/CD: GitHub Actions.

AWS is responsible only for hosting the backend application.
Database hosting and authentication remain managed by Supabase.

Do not migrate PostgreSQL or authentication services to AWS.

The specific AWS hosting service will be selected before production deployment.

## 4. General Development Principles

Follow these principles:

1. Prefer simple, maintainable solutions.
2. Avoid unnecessary abstractions and premature optimization.
3. Keep frontend, backend, database and AI responsibilities separate.
4. Write readable and well-structured code.
5. Use type hints in Python.
6. Use TypeScript types instead of unnecessary `any`.
7. Validate external input.
8. Handle errors explicitly.
9. Write tests for important business logic.
10. Avoid duplicating existing functionality.
11. Do not introduce dependencies without explaining why they are needed.
12. Follow existing project conventions before introducing new ones.

Do not build functionality that is not required by the current implementation task.

## 5. Working with Claude Code

Work incrementally.

### Before implementation

For every significant task:

1. Read the relevant project documentation.
2. Inspect the existing code.
3. Understand the current implementation.
4. Identify files that need to be changed.
5. Explain the proposed solution.
6. Present a short implementation plan.
7. Wait for user approval before making significant changes.

Do not assume that a suggested implementation has been approved.

### During implementation

- Work only on the approved task.
- Keep changes small and focused.
- Do not modify unrelated files.
- Do not rewrite working code without a clear reason.
- Explain important technical decisions.
- Report any deviations from the implementation plan.
- Stop and ask when an important requirement is unclear.

### After implementation

1. Run relevant tests.
2. Check for linting and type errors where configured.
3. Review the changes.
4. Summarize modified files.
5. Explain what was implemented.
6. Report any remaining problems.
7. Suggest a suitable Git commit message.

The user reviews changes and decides when to commit.

## 6. Git Rules

The user manages Git commits and repository history manually through Visual Studio Code.

Claude must follow these rules:

- Do not create Git commits unless explicitly requested.
- Do not push changes to remote repositories.
- Do not switch branches without approval.
- Do not reset, rebase or rewrite Git history without explicit approval.
- Do not discard user changes.
- Do not run destructive Git commands.
- Never overwrite uncommitted user work.

Before modifying files, inspect the relevant existing code and respect the current working tree.

Suggest commit messages using conventional commit style when appropriate.

Example:

`feat: implement competency map generation`

## 7. Architecture Rules

### Frontend

- Frontend communicates with the backend through the REST API.
- Do not call OpenAI directly from the browser.
- Keep API communication separate from UI components.
- Use TypeScript types for API requests and responses.
- Support responsive desktop and mobile layouts.

### Backend

- Use FastAPI routers for API endpoints.
- Keep business logic separate from route handlers.
- Use Pydantic for request and response validation.
- Keep database access separate from business logic.
- Keep AI provider communication inside the AI Service.
- Validate authentication and resource ownership.
- FastAPI runs on AWS in production.

- FastAPI connects to Supabase PostgreSQL as an external managed database.

- Supabase Auth handles user registration, login and token issuance.

- FastAPI validates Supabase JWTs before processing protected requests.
- Database access must respect user ownership and Row Level Security.

### Database

- Use Supabase PostgreSQL.
- Follow the approved database design.
- Use migrations for schema changes.
- Preserve historical assessment data.
- Enforce user data ownership.
- Apply Row Level Security to user-owned data.

- Supabase is responsible for hosting and managing PostgreSQL and Supabase Auth.

- AWS must not be used as a replacement for Supabase database or authentication services.

### AI Service

- Keep AI prompts separate from business logic.
- Use structured outputs when predictable data is required.
- Validate AI responses before storing or using them.
- Centralize model configuration.
- Version prompts.
- Handle provider errors and timeouts.
- Do not assume AI output is always correct.

## 8. Security Rules

- Never expose API keys or secrets in frontend code.
- Never commit `.env` files.
- Maintain `.env.example` without real credentials.
- Validate all user input.
- Verify Supabase JWTs on protected backend endpoints.
- Never trust a frontend-supplied user ID as proof of ownership.
- Protect user data using authorization checks and RLS.
- Avoid logging sensitive user information.
- Do not expose internal stack traces to frontend users.

## 9. Testing Rules

Testing is part of implementation, not a separate final phase.

- Write unit tests for important business logic.
- Write API tests for backend endpoints.
- Test database ownership and authorization.
- Test AI response validation.
- Use mocked AI responses for deterministic automated tests.
- Keep real AI integration tests controlled to avoid unnecessary API costs.
- Do not claim that tests pass unless they have actually been executed.

When a test fails, investigate the cause rather than modifying the test simply to make it pass.

## 10. Cost Control

Avoid unnecessary costs during development.

- Prefer local Docker Compose.
- Use mocked AI responses during most automated tests.
- Avoid unnecessary OpenAI API requests.
- Do not create AWS resources without explicit approval.
- Do not deploy to production without explicit approval.
- Never run expensive cloud operations without explaining their expected cost.

## 11. Language and Communication

- Discuss implementation and technical decisions with the user in Polish.
- Write source code, comments, identifiers, API fields and technical documentation in English.
- Use clear and understandable technical explanations.
- Explain why a solution is needed, not only how to implement it.
- Avoid unnecessary technical complexity.
- Prefer short, focused implementation steps.

The user wants to understand the architecture and implementation rather than blindly accept generated code.

## 12. Scope Control

The MVP scope is defined in `docs/MVP-SCOPE.md`.

Do not implement deferred features unless explicitly requested.

Examples of deferred features:

- Practical coding exercises.
- Code execution.
- Uploaded code and document analysis.
- Spaced repetition.
- Gamification.
- Knowledge graph.
- Job offer import.
- Native mobile applications.
- Real-time AI voice conversations.

If a proposed solution requires a deferred feature, explain the dependency and suggest an MVP-compatible alternative.

## 13. Definition of Done

A task is complete when:

- The approved requirements are implemented.
- The code follows the project architecture.
- Relevant tests pass.
- No known critical errors remain.
- Changes have been reviewed.
- The user understands what was changed.
- Any necessary documentation updates are identified.

The user makes the final decision to accept the changes and create a Git commit.

---

**Project:** SkillLoop  
**Primary objective:** Build a maintainable MVP while learning a repeatable AI Engineering workflow.
