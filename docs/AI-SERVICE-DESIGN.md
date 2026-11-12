

**Project:** SkillLoop  
**Version:** 1.0  
**Status:** Draft  
**AI Provider:** OpenAI API  
**Backend:** Python + FastAPI

---

## 1. Purpose

This document defines the architecture and responsibilities of the AI Service in SkillLoop.

The AI Service is responsible for intelligent features that support the user's professional development.

Its main responsibilities are:

1. Generating competency maps.
    
2. Generating diagnostic questions.
    
3. Evaluating user explanations.
    
4. Generating follow-up questions.
    
5. Producing structured feedback.
    
6. Recommending the next learning activity.
    
7. Transcribing voice responses through Speech-to-Text.
    

The AI Service must be independent of the frontend and must expose its functionality through the backend application.

## 2. Architectural Principles

The AI integration must follow these principles:

- Keep AI logic separate from business logic and API endpoints.
    
- Communicate with AI providers only from the backend.
    
- Use structured outputs wherever predictable data is required.
    
- Validate every AI response before using or storing it.
    
- Keep prompts separate from application code.
    
- Version prompts to make AI behavior traceable.
    
- Centralize model configuration.
    
- Handle provider errors and timeouts.
    
- Minimize unnecessary API calls and token usage.
    
- Avoid permanently storing voice recordings by default.
    
- Make it possible to introduce another AI provider in the future.
    

The application must not depend directly on a specific OpenAI model.

## 3. High-Level Architecture

The AI Service is a backend module inside the FastAPI application.

```
Frontend (Next.js)
       |
       v
FastAPI Application
       |
       v
Business Logic
       |
       v
AI Service
       |
       +--------------------+
       |                    |
       v                    v
Prompt Manager         AI Provider
                            |
                            v
                       OpenAI API
                            |
                            v
                    Structured Response
                            |
                            v
                    Response Validation
                            |
                            v
                    Business Logic
                            |
                            v
                    Supabase PostgreSQL
```

The AI Service does not communicate directly with the frontend.

The frontend communicates with FastAPI, which handles authentication, business rules, AI requests and database operations.

## 4. AI Service Modules

The AI Service should be divided into logical modules.

### 4.1 Competency Map Generator

**Responsibility:** Generate a competency map based on the user's target professional role and seniority.

Input:

- Target role.
    
- Seniority level.
    
- Optional user context.
    

Output:

A structured competency list containing:

- Competency name.
    
- Description.
    
- Why the competency matters.
    
- Knowledge type.
    
- Importance.
    
- Expected proficiency.
    

The generated map must be editable by the user before it becomes their active learning map.

The AI should explain why each competency is relevant to the selected role and seniority.

### 4.2 Diagnostic Question Generator

**Responsibility:** Generate questions used to evaluate the user's initial knowledge.

Input:

- Selected competency.
    
- Target role.
    
- Seniority level.
    
- Expected proficiency.
    

Output:

- Question.
    
- Question purpose.
    
- Expected knowledge areas.
    
- Relevant competency.
    

Questions should evaluate understanding rather than memorization alone.

The diagnostic process should be divided into manageable stages instead of generating one excessively long test.

### 4.3 Assessment Engine

**Responsibility:** Evaluate the user's explanations.

Input:

- Original question.
    
- Competency context.
    
- Target role and seniority.
    
- User response.
    
- Previous answers in the current assessment, when applicable.
    

Output:

- Assessment status.
    
- Scores for individual assessment dimensions.
    
- Reasons for the scores.
    
- Identified strengths.
    
- Knowledge gaps.
    
- Feedback.
    
- Follow-up decision.
    

The assessment dimensions are defined in `AI-ASSESSMENT-DESIGN.md`:

1. Technical correctness.
    
2. Conceptual understanding.
    
3. Completeness.
    
4. Clarity.
    

The engine must distinguish between insufficient evidence and demonstrated lack of knowledge.

### 4.4 Follow-up Question Generator

**Responsibility:** Generate targeted questions when the initial explanation does not provide sufficient evidence.

Input:

- Original question.
    
- User's previous response.
    
- Identified ambiguity or knowledge gap.
    
- Competency context.
    
- Previous follow-up questions, if any.
    

Output:

- One follow-up question.
    
- Reason for asking it.
    
- Knowledge area being investigated.
    

Rules:

- Ask one question at a time.
    
- Ask no more than two follow-up questions by default.
    
- Do not ask unnecessary questions when the evidence is sufficient.
    
- Stop when enough information has been collected.
    
- If the user skips a follow-up, preserve the distinction between insufficient evidence and incorrect knowledge.
    

The assessment process must maintain its context across multiple requests.

### 4.5 Feedback Generator

**Responsibility:** Produce useful and understandable feedback after assessment.

Output should include:

- What the user understands correctly.
    
- What is missing.
    
- Which misconceptions need correction.
    
- What the user should learn next.
    

Feedback should be specific, constructive and focused on improvement.

Avoid generic messages without useful explanations.

### 4.6 Recommendation Engine

**Responsibility:** Recommend the next learning activity.

Input:

- Career goal.
    
- Competency map.
    
- Expected proficiency.
    
- Current proficiency.
    
- Assessment history.
    
- Identified knowledge gaps.
    
- Previous recommendations.
    

Output:

- Recommended competency.
    
- Priority.
    
- Reason for recommendation.
    
- Suggested learning activity.
    

The recommendation engine should consider the importance of competencies for the selected role.

The user must remain in control of the learning process.

### 4.7 Speech-to-Text Service

**Responsibility:** Convert voice responses into text.

Workflow:

1. Frontend records the user's voice.
    
2. Frontend sends the audio file to FastAPI.
    
3. Backend validates the file.
    
4. Backend sends audio to the OpenAI Speech-to-Text service.
    
5. Backend receives the transcription.
    
6. Transcription is passed to the Assessment Engine.
    
7. The result follows the same assessment process as a text response.
    

The original audio is not permanently stored by default.

Text and voice responses must use the same assessment criteria.

## 5. AI Provider Abstraction

The application must not couple business logic directly to OpenAI SDK calls.

Introduce a provider abstraction.

Example conceptual interface:

```
class AIProvider:
    async def generate_structured_output(
        self,
        prompt: str,
        response_schema: dict
    ) -> dict:
        raise NotImplementedError
```

An OpenAI implementation will provide the actual API communication.

Future providers can implement the same interface.

The provider abstraction should handle:

- API communication.
    
- Model selection.
    
- Structured output configuration.
    
- Timeouts.
    
- Provider-specific errors.
    
- Usage metadata when available.
    

Business logic must use the abstraction rather than calling the OpenAI SDK directly.

## 6. Prompt Management

Prompts must be stored separately from business logic.

Suggested structure:

```
backend/
└── app/
    └── ai/
        ├── providers/
        │   ├── base.py
        │   └── openai_provider.py
        │
        ├── services/
        │   ├── competency_generator.py
        │   ├── diagnostic_generator.py
        │   ├── assessment_engine.py
        │   ├── followup_generator.py
        │   ├── feedback_generator.py
        │   ├── recommendation_engine.py
        │   └── speech_to_text.py
        │
        ├── prompts/
        │   ├── competency_map.md
        │   ├── diagnostic_questions.md
        │   ├── assessment.md
        │   ├── follow_up.md
        │   ├── feedback.md
        │   └── recommendations.md
        │
        ├── schemas/
        │   ├── competency_map.py
        │   ├── assessment.py
        │   └── recommendations.py
        │
        └── config.py
```

This is a logical organization proposal. The final implementation may adjust file boundaries when necessary.

### Prompt Versioning

Each prompt must have a version identifier.

For example:

- `assessment_v1`
    
- `follow_up_v1`
    
- `competency_map_v1`
    

The prompt version used for an assessment must be stored with the assessment result.

This makes it possible to understand how an evaluation was generated and compare behavior across prompt changes.

## 7. Structured Outputs and Validation

Whenever an AI operation requires predictable data, the model should return structured output.

Use Pydantic models to validate responses.

Example conceptual model:

```
from pydantic import BaseModel, Field
from typing import Literal


class DimensionScore(BaseModel):
    score: int = Field(ge=0, le=4)
    reason: str


class AssessmentResult(BaseModel):
    assessment_status: Literal[
        "completed",
        "insufficient_evidence",
        "awaiting_follow_up"
    ]

    technical_correctness: DimensionScore
    conceptual_understanding: DimensionScore
    completeness: DimensionScore
    clarity: DimensionScore

    feedback: str
    follow_up_question: str | None = None
```

The actual schema must be aligned with `AI-ASSESSMENT-DESIGN.md`.

Validation rules:

- Reject invalid score ranges.
    
- Reject missing required fields.
    
- Validate allowed status values.
    
- Validate follow-up decisions.
    
- Do not store malformed AI responses as completed assessments.
    

If validation fails, the backend should handle the error rather than passing invalid data to the frontend.

## 8. Assessment Orchestration

The assessment workflow requires multiple interactions between the user and AI.

It must be orchestrated by the backend rather than implemented as an uncontrolled conversation.

Suggested workflow:

```
User submits explanation
          |
          v
Assessment Engine
          |
          v
Analyze response
          |
          v
Is evidence sufficient?
       /       \
     No         Yes
     |           |
     v           v
Generate       Finalize
follow-up      assessment
     |
     v
User answers
     |
     v
Analyze again
     |
     v
Enough evidence or follow-up limit reached?
     |
     v
Finalize assessment
     |
     v
Store result
     |
     v
Update competency profile
     |
     v
Generate recommendation
```

The backend must retain the assessment state between requests.

The frontend should receive a clear next action:

- Submit a follow-up answer.
    
- Display final feedback.
    
- Indicate insufficient evidence.
    
- Allow the user to finish the assessment.
    

The system should not require one long-lived AI conversation to preserve assessment context. Relevant context should be managed by the application.

## 9. Model Configuration

Model selection must be centralized.

Configuration should allow separate model settings for different AI operations.

Example:

```
OPENAI_API_KEY=your_api_key

OPENAI_MODEL_COMPETENCY=...
OPENAI_MODEL_ASSESSMENT=...
OPENAI_MODEL_RECOMMENDATION=...
OPENAI_MODEL_TRANSCRIPTION=...
```

Actual model identifiers must be selected and verified during implementation.

The application should allow model changes without modifying business logic.

Model configuration must remain on the backend.

## 10. Error Handling

The AI Service must handle common failures.

|Error|Expected behavior|
|---|---|
|API timeout|Return a controlled error and allow retry|
|Provider unavailable|Report temporary service unavailability|
|Rate limit|Retry according to a controlled policy|
|Invalid structured output|Validate and handle the failure|
|Empty AI response|Treat as an unsuccessful operation|
|Invalid audio file|Reject before sending to provider|
|Transcription failure|Ask the user to retry or use text input|
|Insufficient context|Request the missing information|

Retry rules:

- Use limited retries for temporary failures.
    
- Use exponential backoff where appropriate.
    
- Avoid retrying permanent validation errors.
    
- Avoid duplicate database records when retrying requests.
    
- Do not retry indefinitely.
    

## 11. Cost and Performance Control

AI requests can become a significant operating cost.

The MVP should include basic cost-control mechanisms:

- Use separate model configuration for different operations.
    
- Avoid unnecessary repeated AI calls.
    
- Limit the size of conversation context.
    
- Limit audio file size and duration.
    
- Avoid generating excessive diagnostic questions.
    
- Store completed results to avoid unnecessary re-evaluation.
    
- Track token usage and provider usage metadata when available.
    

The application should not automatically re-evaluate an unchanged response every time a user opens a page.

More advanced cost optimization can be introduced after usage patterns are understood.

## 12. Logging and Observability

The backend should log AI operations without exposing sensitive user content unnecessarily.

Recommended metadata:

- Operation type.
    
- User ID or internal request identifier.
    
- AI provider.
    
- Model identifier.
    
- Prompt version.
    
- Request duration.
    
- Success or failure.
    
- Token usage when available.
    
- Error category.
    

Avoid logging:

- API keys.
    
- Authentication tokens.
    
- Full audio recordings.
    
- Unnecessary personal information.
    

AI operations should be traceable through a request identifier.

## 13. Testing Strategy

The AI Service requires several types of tests.

### Unit Tests

Test individual components:

- Prompt construction.
    
- Pydantic validation.
    
- Assessment state transitions.
    
- Error handling.
    
- Recommendation rules.
    

### Integration Tests

Test communication between:

- FastAPI and AI Service.
    
- AI Service and provider implementation.
    
- AI Service and database persistence.
    
- Speech-to-Text and Assessment Engine.
    

### AI Evaluation Tests

Maintain a small dataset of representative questions and expected evaluation characteristics.

Test cases should include:

- Correct and complete explanations.
    
- Partially correct explanations.
    
- Incorrect technical statements.
    
- Ambiguous explanations.
    
- Answers that require follow-up.
    
- Answers with insufficient evidence.
    
- Answers containing correct technical knowledge expressed with language mistakes.
    

AI evaluation tests should verify expected behavior and consistency, not require identical wording or scores from every model run.

## 14. Security and Privacy

- OpenAI API keys must never be exposed to the frontend.
    
- All provider requests must originate from the backend.
    
- User data must be handled according to the application's data ownership rules.
    
- Audio should be processed without permanent storage by default.
    
- Logs must not contain secrets or unnecessary personal data.
    
- Requests must be authenticated and authorized before accessing user-specific data.
    
- Input files must be validated before processing.
    

## 15. Out of Scope for MVP

The following are postponed:

- Multiple AI providers running simultaneously.
    
- Automatic model routing based on complex optimization.
    
- Fine-tuning custom models.
    
- Retrieval-Augmented Generation (RAG).
    
- Vector databases.
    
- Autonomous AI agents.
    
- Multi-agent orchestration.
    
- Real-time conversational voice tutor.
    
- Advanced AI analytics dashboards.
    

These capabilities should only be introduced when a concrete product requirement justifies them.

## 16. Implementation Order

Suggested implementation sequence:

1. Create the AI module structure.
    
2. Implement centralized AI configuration.
    
3. Implement the AI provider abstraction.
    
4. Integrate the OpenAI provider.
    
5. Implement prompt management and versioning.
    
6. Implement Pydantic response schemas.
    
7. Implement competency map generation.
    
8. Implement diagnostic question generation.
    
9. Implement the assessment engine.
    
10. Implement follow-up orchestration.
    
11. Implement feedback generation.
    
12. Implement recommendations.
    
13. Implement Speech-to-Text integration.
    
14. Add unit and integration tests.
    
15. Add logging, error handling and cost controls.
    

---

**Document status:** Draft v1.0

**Next step:** Define `API-DESIGN.md`, including the FastAPI endpoints and request/response contracts required by the frontend.