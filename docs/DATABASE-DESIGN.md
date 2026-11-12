

**Project:** SkillLoop  
**Version:** 1.1  
**Status:** Draft  
**Database:** Supabase PostgreSQL

---

## 1. Database Design Goals

The database must support the core SkillLoop learning cycle:

1. A user creates an account.
    
2. The user selects one professional goal and seniority level.
    
3. AI generates a competency map.
    
4. The user reviews and edits the map.
    
5. The user completes an initial diagnostic assessment.
    
6. The user learns individual competencies by explaining topics in their own words.
    
7. AI evaluates explanations and provides feedback.
    
8. AI recommends what the user should learn next.
    
9. The user can review their progress and learning history.
    

The database must preserve historical assessment results even when the user modifies their competency map.

## 2. Technology

- **Database:** PostgreSQL
    
- **Hosting:** Supabase
    
- **Authentication:** Supabase Auth
    
- **Authorization:** PostgreSQL Row Level Security (RLS)
    
- **Backend:** FastAPI
    

Supabase Auth manages authentication and user identities. Application data is stored in PostgreSQL.

FastAPI is responsible for validating authenticated requests, enforcing business rules, and communicating with AI services.

## 3. Core Data Model

The MVP uses the following main entities:

|Entity|Responsibility|
|---|---|
|profiles|Additional user information|
|career_goals|User's professional development goal|
|competencies|Competency map belonging to a goal|
|learning_sessions|Diagnostic or learning sessions|
|session_items|Questions, user responses and AI evaluations|
|recommendations|AI-generated learning recommendations|

### Entity relationships

- One user has one profile.
    
- One user can have one active career goal.
    
- One career goal contains many competencies.
    
- One career goal can have many learning sessions.
    
- One learning session contains one or more session items.
    
- Each session item can be associated with a competency.
    
- One user can have many learning recommendations.
    

A user has one active career goal in the MVP. Multiple competencies can be developed simultaneously within that goal.

## 4. Tables

### 4.1 profiles

Stores additional information about the user.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key; references auth.users.id|
|display_name|TEXT|Optional display name|
|preferred_language|TEXT|Preferred application language|
|created_at|TIMESTAMPTZ|Creation timestamp|
|updated_at|TIMESTAMPTZ|Last update timestamp|

The profile is created when the user registers or during initial onboarding.

### 4.2 career_goals

Stores the user's professional development goal.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key|
|user_id|UUID|Owner; references auth.users.id|
|target_role|TEXT|Target professional role|
|seniority|TEXT|junior, mid or senior|
|description|TEXT|Optional goal description|
|status|TEXT|active or archived|
|created_at|TIMESTAMPTZ|Creation timestamp|
|updated_at|TIMESTAMPTZ|Last update timestamp|

**Business rules:**

- A user can have only one active career goal.
    
- A user can archive an existing goal.
    
- An archived goal and its learning history remain stored.
    
- Creating a new active goal should not silently delete the previous goal.
    

### 4.3 competencies

Stores the competency map generated for a career goal.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key|
|career_goal_id|UUID|Parent career goal|
|name|TEXT|Competency name|
|description|TEXT|Competency description|
|rationale|TEXT|Why this competency matters for the selected role|
|knowledge_type|TEXT|memory, application or documentation|
|importance|TEXT|critical, high, medium or low|
|expected_level|TEXT|Expected proficiency: beginner, intermediate or advanced|
|current_level|TEXT|Current assessed proficiency|
|display_order|INTEGER|Position in the competency list|
|status|TEXT|active or archived|
|source|TEXT|ai_generated or user_added|
|created_at|TIMESTAMPTZ|Creation timestamp|
|updated_at|TIMESTAMPTZ|Last update timestamp|

**Knowledge types:**

- `memory` — knowledge the user should understand and recall without documentation.
    
- `application` — knowledge the user should be able to apply in practice.
    
- `documentation` — knowledge the user should know how to find and use in documentation.
    

**Proficiency levels:**

|Level|Meaning|
|---|---|
|not_assessed|Insufficient assessment data to determine the user's proficiency|
|beginner|Basic concepts are partially understood|
|intermediate|The user understands the topic and can explain it|
|advanced|The user demonstrates deep and consistent understanding|

**Important distinction:**

- `expected_level` describes the proficiency required for the selected role and seniority.
    
- `current_level` describes the user's currently assessed proficiency.
    
- `not_assessed` is a valid state for `current_level`, but not for `expected_level`.
    

**Business rules:**

- Users can edit, add and archive competencies.
    
- Archiving a competency must not delete its historical assessments.
    
- Each competency belongs to exactly one career goal.
    
- Expected proficiency is not the same as the user's current proficiency.
    
- Current proficiency is calculated from assessment history, not manually entered by the user.
    
- New assessments can update current proficiency over time.
    

### 4.4 learning_sessions

Represents a diagnostic or learning session.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key|
|user_id|UUID|Session owner|
|career_goal_id|UUID|Related career goal|
|session_type|TEXT|initial_diagnostic or learning|
|status|TEXT|in_progress, completed or abandoned|
|started_at|TIMESTAMPTZ|Session start|
|completed_at|TIMESTAMPTZ|Session completion|
|created_at|TIMESTAMPTZ|Creation timestamp|

**Business rules:**

- An initial diagnostic can be divided into multiple stages.
    
- A user can leave a session and continue later.
    
- Abandoned sessions remain in the database.
    
- A learning session can focus on one competency.
    

### 4.5 session_items

Stores individual questions, user explanations and AI evaluations.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key|
|learning_session_id|UUID|Parent session|
|competency_id|UUID|Related competency|
|question|TEXT|Question or explanation prompt|
|response_text|TEXT|User's answer or transcribed explanation|
|input_type|TEXT|text or voice|
|assessment_status|TEXT|assessed or not_assessed|
|evaluation|JSONB|Structured AI evaluation|
|score|SMALLINT|Optional overall score, 0–100|
|ai_model|TEXT|Model used for evaluation|
|prompt_version|TEXT|Evaluation prompt version|
|created_at|TIMESTAMPTZ|Creation timestamp|
|evaluated_at|TIMESTAMPTZ|Evaluation timestamp|

**Evaluation structure:**

The `evaluation` JSONB column stores structured feedback, for example:

- `technical_correctness`
    
- `conceptual_understanding`
    
- `completeness`
    
- `clarity`
    
- `strengths`
    
- `knowledge_gaps`
    
- `feedback`
    
- `suggested_next_steps`
    

The exact JSON schema will be defined separately in the AI Service specification.

**Important rules:**

- Text and voice responses use the same evaluation structure.
    
- Voice recordings are not permanently stored by default.
    
- The transcribed text is stored as the user's response.
    
- An unanswered question must not automatically be treated as incorrect.
    
- `not_assessed` means there is insufficient information to evaluate the user's knowledge.
    
- AI evaluation results should be retained as historical records rather than overwritten by future evaluations.
    

### 4.6 recommendations

Stores learning recommendations generated by AI.

|Column|Type|Description|
|---|---|---|
|id|UUID|Primary key|
|user_id|UUID|Recommendation owner|
|career_goal_id|UUID|Related career goal|
|competency_id|UUID|Recommended competency|
|reason|TEXT|Why this competency is recommended|
|priority|TEXT|high, medium or low|
|status|TEXT|pending, accepted, completed or dismissed|
|created_at|TIMESTAMPTZ|Creation timestamp|
|updated_at|TIMESTAMPTZ|Last update timestamp|

Recommendations should consider:

- Importance of the competency for the selected role.
    
- Expected proficiency.
    
- Previous diagnostic results.
    
- Recent learning session evaluations.
    
- Existing knowledge gaps.
    

The user remains in control and can choose a different competency.

## 5. Proficiency and Assessment Principles

SkillLoop distinguishes between three concepts:

1. **Expected proficiency** — what is required for the selected role and seniority.
    
2. **Current proficiency** — what the system has evidence the user currently understands.
    
3. **Assessment status** — whether sufficient evidence exists to determine current proficiency.
    

The current proficiency scale consists of four states:

- `not_assessed` — insufficient assessment data.
    
- `beginner` — basic concepts are partially understood.
    
- `intermediate` — the user understands the topic and can explain it.
    
- `advanced` — the user demonstrates deep and consistent understanding.
    

**Assessment rules:**

- Current proficiency is calculated from the user's assessment history.
    
- Each AI evaluation is stored as a historical record.
    
- New evaluations can change the current proficiency level.
    
- Missing answers do not automatically lower proficiency.
    
- The system must distinguish between insufficient evidence and demonstrated knowledge gaps.
    
- The user should be able to see their current level and historical progress.
    

The exact proficiency calculation algorithm will be specified separately. It should consider assessment quality and history rather than relying on a single answer.

## 6. Data Ownership and Security

Every user must have access only to their own application data.

**Required security rules:**

- Enable Row Level Security on all user-owned tables.
    
- Use `auth.uid()` to verify ownership.
    
- Users must not be able to access another user's goals, competencies, sessions, responses or recommendations.
    
- FastAPI must validate Supabase JWTs on authenticated endpoints.
    
- Never expose the Supabase service role key in frontend code.
    
- AI API keys must remain on the backend.
    

Ownership should be verified through the relationship between the record and its owning user, not simply by trusting a user ID supplied by the frontend.

## 7. Indexes and Constraints

Recommended indexes:

|Table|Index|
|---|---|
|career_goals|user_id, status|
|competencies|career_goal_id, status|
|learning_sessions|user_id, created_at|
|learning_sessions|career_goal_id, session_type|
|session_items|learning_session_id|
|session_items|competency_id, created_at|
|recommendations|user_id, status, created_at|

Recommended constraints:

- Foreign keys for all entity relationships.
    
- `expected_level` restricted to beginner, intermediate or advanced.
    
- `current_level` restricted to not_assessed, beginner, intermediate or advanced.
    
- `score` between 0 and 100.
    
- Unique active career goal per user.
    
- Controlled values for status, session type and knowledge type.
    

A partial unique index can enforce the active-goal rule:

```
CREATE UNIQUE INDEX one_active_goal_per_user
ON career_goals (user_id)
WHERE status = 'active';
```

## 8. Data Lifecycle

The MVP should preserve learning history.

- Archiving a career goal does not delete its competencies or sessions.
    
- Archiving a competency does not delete previous assessments.
    
- New evaluations create new historical records.
    
- Recommendations can be dismissed or completed without deleting them.
    
- Deleting a user account must follow an explicit data deletion policy.
    

## 9. Future Extensions

The database design should leave room for future features without implementing them in the MVP.

Potential extensions:

- Practical exercises and submitted solutions.
    
- Code and technical documentation uploads.
    
- Spaced repetition and review scheduling.
    
- XP, levels, streaks and badges.
    
- Knowledge graph and competency relationships.
    
- Daily learning plans and weekly rest days.
    
- Multiple career goals.
    
- Job offer analysis.
    

These features should be introduced only when their requirements are defined.

## 10. Implementation Order

Suggested implementation sequence:

1. Create Supabase project and configure authentication.
    
2. Create `profiles`.
    
3. Create `career_goals`.
    
4. Create `competencies`.
    
5. Create `learning_sessions`.
    
6. Create `session_items`.
    
7. Create `recommendations`.
    
8. Add foreign keys, constraints and indexes.
    
9. Enable and test Row Level Security.
    
10. Connect FastAPI to Supabase.
    

---

**Document status:** Draft v1.1

**Next step:** Review the data model and clarify how AI assessment results translate into current proficiency before creating SQL migrations.