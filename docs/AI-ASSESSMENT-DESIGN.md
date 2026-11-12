

**Project:** SkillLoop  
**Version:** 1.0  
**Status:** Draft

---

## 1. Purpose

This document defines how SkillLoop evaluates a user's professional knowledge and understanding using AI.

The assessment system should determine whether a user genuinely understands a competency, can explain relevant concepts, and can identify important technical details.

The goal is not to test memorization alone.

SkillLoop should help users identify knowledge gaps, improve their explanations, and gradually develop the competencies required for their target professional role.

## 2. Assessment Principles

The assessment system must follow these principles:

1. Evaluate understanding, not just memorized definitions.
    
2. Evaluate the technical correctness of explanations.
    
3. Allow users to express knowledge in their own words.
    
4. Ask follow-up questions when an answer is incomplete or ambiguous.
    
5. Distinguish insufficient evidence from demonstrated lack of knowledge.
    
6. Provide constructive and actionable feedback.
    
7. Maintain consistent assessment criteria across sessions.
    
8. Never claim that practical competence has been demonstrated based only on a theoretical explanation.
    
9. Separate technical knowledge evaluation from language quality evaluation.
    
10. Preserve assessment history.
    

## 3. Assessment Dimensions

Each user response is evaluated using four dimensions.

### 3.1 Technical Correctness

Evaluates whether the information provided by the user is technically correct.

Questions to consider:

- Are the technical statements correct?
    
- Are there factual errors?
    
- Does the user confuse related concepts?
    
- Are important technical details misunderstood?
    

### 3.2 Conceptual Understanding

Evaluates whether the user understands how and why something works.

Questions to consider:

- Can the user explain the underlying mechanism?
    
- Does the user understand cause-and-effect relationships?
    
- Can the user distinguish related concepts?
    
- Can the user explain why a particular solution is used?
    

### 3.3 Completeness

Evaluates whether the explanation covers the important aspects of the question.

Questions to consider:

- Are the essential elements included?
    
- Are important steps or conditions missing?
    
- Does the explanation address the actual question?
    
- Is additional clarification necessary?
    

### 3.4 Clarity

Evaluates whether the user can communicate their understanding clearly.

Questions to consider:

- Is the explanation logically structured?
    
- Can another person understand the explanation?
    
- Are technical terms used appropriately?
    
- Is the explanation sufficiently precise?
    

Clarity must not be confused with English language proficiency. When a language assessment is enabled, it must be evaluated separately.

## 4. Assessment Scale

Each assessment dimension uses a score from 0 to 4.

|Score|Meaning|
|---|---|
|0|Incorrect or no relevant understanding demonstrated|
|1|Very limited understanding|
|2|Partial understanding|
|3|Good understanding|
|4|Strong and complete understanding|

The AI must provide a short justification for each dimension score.

An assessment should also include an overall result, but the overall result must not hide significant weaknesses in individual dimensions.

If there is insufficient evidence, the AI must use an `insufficient_evidence` assessment status instead of treating the missing evidence as a score of zero.

## 5. Follow-up Questions

The AI can ask additional questions before completing an assessment.

### 5.1 When to Ask Follow-up Questions

Follow-up questions should be considered when:

- The answer is incomplete.
    
- The explanation is ambiguous.
    
- The user provides a correct definition but does not demonstrate understanding.
    
- The user describes a process without explaining why it works.
    
- The answer contains a possible misconception that needs clarification.
    
- The user provides an example that needs further explanation.
    

### 5.2 Follow-up Question Strategy

The AI should ask targeted questions that help distinguish between different levels of understanding.

Examples:

**Initial question:**

What is Docker image?

**User answer:**

A Docker image is used to create containers.

**Follow-up question:**

What is the difference between a Docker image and a running container?

**User answer:**

An image is a template, and a container is an instance created from that image.

**Possible additional question:**

Can multiple containers be created from the same image?

The AI should stop asking questions when it has enough evidence to evaluate the user's understanding.

### 5.3 Follow-up Limits

To keep learning sessions focused:

- Ask one follow-up question at a time.
    
- Use a maximum of two follow-up questions for a single assessment by default.
    
- Do not ask unnecessary questions when the original answer is already sufficient.
    
- Allow the user to finish the assessment without answering a follow-up question.
    
- If the user does not answer, record insufficient evidence where appropriate.
    

The follow-up limit can be configurable in the future.

## 6. Assessment Workflow

Each assessment follows these stages:

1. Generate or select a question.
    
2. Receive the user's response.
    
3. Analyze the response.
    
4. Determine whether sufficient evidence exists.
    
5. Ask a follow-up question if necessary.
    
6. Evaluate the complete response.
    
7. Generate structured feedback.
    
8. Update the competency assessment profile.
    
9. Recommend the next learning step.
    

The AI should not produce a final proficiency assessment before the follow-up stage is completed or explicitly skipped.

### Assessment States

Suggested assessment statuses:

- `in_progress`
    
- `awaiting_follow_up`
    
- `completed`
    
- `insufficient_evidence`
    

These statuses describe the assessment workflow and should be distinguished from the learning session status.

## 7. Voice and Text Assessment

SkillLoop supports two response methods:

### Text

The user writes an explanation directly in the application.

### Voice

The user records an explanation using a microphone.

The voice workflow:

1. The browser records the user's audio.
    
2. The frontend sends the recording to FastAPI.
    
3. FastAPI sends the audio to the Speech-to-Text service.
    
4. The transcription is returned to the backend.
    
5. The transcript is evaluated using the same AI assessment process as text responses.
    

The original audio is not permanently stored by default.

Both input methods must use the same assessment criteria.

The AI must not penalize users for spoken-language disfluencies, pauses or minor grammatical mistakes when evaluating technical knowledge.

## 8. Structured AI Evaluation

The AI Service must return structured evaluation data.

Suggested response structure:

```
{
  "assessment_status": "completed",
  "dimension_scores": {
    "technical_correctness": {
      "score": 3,
      "reason": "The explanation is technically correct."
    },
    "conceptual_understanding": {
      "score": 2,
      "reason": "The user understands the basic concept but does not explain the underlying mechanism."
    },
    "completeness": {
      "score": 2,
      "reason": "One important aspect is missing."
    },
    "clarity": {
      "score": 4,
      "reason": "The explanation is clear and logically structured."
    }
  },
  "strengths": [
    "Correctly identifies the main purpose of Docker images."
  ],
  "knowledge_gaps": [
    "Does not fully explain the relationship between images and containers."
  ],
  "feedback": "Good starting explanation. You understand the basic purpose, but you should improve your understanding of how images and containers relate to each other.",
  "suggested_next_steps": [
    "Review Docker image layers.",
    "Learn how containers are created from images."
  ],
  "follow_up_required": false
}
```

This is a proposed schema. The final API contract will be defined in `AI-SERVICE-DESIGN.md`.

The backend must validate all AI responses before storing them.

## 9. Competency Proficiency Calculation

SkillLoop uses four proficiency states:

|Level|Description|
|---|---|
|not_assessed|Insufficient assessment data|
|beginner|Basic concepts are partially understood|
|intermediate|The user understands the topic and can explain it|
|advanced|The user demonstrates deep and consistent understanding|

The system must distinguish between:

- Individual assessment scores.
    
- Current competency proficiency.
    
- Expected proficiency for the selected role.
    

### Calculation Principles

Current proficiency should be based on multiple pieces of assessment evidence when available.

The calculation should consider:

- Technical correctness.
    
- Conceptual understanding.
    
- Completeness.
    
- Assessment history.
    
- Consistency across different questions.
    
- Recency of assessments.
    

A single excellent answer should not automatically establish advanced proficiency.

Likewise, one weak answer should not automatically reduce a previously established level.

The exact calculation algorithm will be designed separately and must be tested before implementation.

## 10. Assessment History

Every completed assessment should be preserved.

Historical records should include:

- Original question.
    
- User response.
    
- Follow-up questions and answers.
    
- Individual dimension scores.
    
- AI feedback.
    
- AI model identifier.
    
- Prompt version.
    
- Assessment timestamp.
    

New assessments must not overwrite previous results.

This allows SkillLoop to show how the user's knowledge changes over time.

## 11. AI Feedback

Feedback should be:

- Specific.
    
- Constructive.
    
- Technically accurate.
    
- Easy to understand.
    
- Focused on improvement.
    

Avoid generic feedback such as:

"Good job!"

Instead, explain:

- What the user understands correctly.
    
- What is missing.
    
- Which misconceptions need correction.
    
- What the user should learn next.
    

The AI should not overwhelm the user with too much information at once.

## 12. Recommendations

After an assessment, SkillLoop can recommend:

- Continuing with the same competency.
    
- Reviewing a knowledge gap.
    
- Moving to a related competency.
    
- Attempting another explanation question.
    

Recommendations should consider:

- Competency importance.
    
- Expected proficiency.
    
- Current proficiency.
    
- Previous assessment results.
    
- Identified knowledge gaps.
    

The user remains in control of the learning process.

## 13. Reliability and Safety

The assessment system must:

- Validate AI-generated structured responses.
    
- Handle invalid or incomplete AI output.
    
- Avoid inventing technical facts.
    
- Distinguish uncertain conclusions from established facts.
    
- Use prompt versioning.
    
- Preserve historical assessment results.
    
- Avoid treating AI scores as absolute truth.
    
- Allow reassessment when the user disagrees with an evaluation.
    

AI evaluation is an estimate of demonstrated knowledge, not a formal professional certification.

## 14. Out of Scope for MVP

The following features are postponed:

- Practical coding exercises.
    
- Automatic code execution.
    
- Uploaded code and documentation analysis.
    
- Real-time AI voice conversations.
    
- English speaking proficiency scoring.
    
- Advanced adaptive testing algorithms.
    
- Spaced repetition scheduling.
    
- External professional certification.
    

These features may be introduced in later development stages.

---

**Document status:** Draft v1.0

**Next step:** Define the AI Service architecture, including prompt management, structured outputs, model selection, validation and error handling.