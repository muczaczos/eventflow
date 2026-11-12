
# SkillLoop – User Flows

**Version:** 1.0  
**Status:** Draft  
**Product:** SkillLoop – Personal Career Knowledge Coach

---

## 1. Overview

This document describes the main user journeys supported by the initial SkillLoop MVP.

It defines how users interact with the application, how the system responds, and how learning data is processed.

The MVP focuses on the following flows:

1. Registration and onboarding.
    
2. Competency map generation.
    
3. Initial competency assessment.
    
4. Selecting a learning topic.
    
5. Learning through explanation.
    
6. Voice and text answer submission.
    
7. AI evaluation and feedback.
    
8. Learning recommendations.
    
9. Progress tracking.
    

## 2. Registration and Onboarding

### Goal

Create a user profile and collect the information required to generate a personalized competency map.

### Flow

1. User opens SkillLoop.
    
2. User creates an account or logs in.
    
3. User enters onboarding.
    
4. User selects a target professional role.
    
5. User selects a target seniority:
    
    - Junior
        
    - Mid
        
    - Senior
        
6. User provides information about current experience.
    
7. User completes the onboarding process.
    
8. SkillLoop saves the profile.
    

### System responsibilities

- Authenticate the user.
    
- Create or update the user profile.
    
- Store target role and seniority.
    
- Start competency map generation.
    

### Result

The user has an initial profile and can proceed to competency map generation.

## 3. Competency Map Generation

### Goal

Generate a personalized competency map based on the user's target role and seniority.

### Flow

1. SkillLoop sends the user's role and seniority to the AI service.
    
2. AI generates a competency map.
    
3. Each competency includes:
    
    - Name.
        
    - Description.
        
    - Importance.
        
    - Expected proficiency.
        
    - Explanation of why it is required.
        
    - Expected knowledge and skills.
        
4. Each competency is classified into one of three knowledge expectations:
    
    - Know from memory.
        
    - Know how to apply.
        
    - Know where to find.
        
5. SkillLoop validates the generated data.
    
6. The application saves the competency map.
    
7. User reviews the generated map.
    
8. User can edit, add, or remove competencies.
    
9. User confirms the map.
    

### Alternative flows

- If AI generation fails, the user can retry.
    
- If generated data is invalid, the backend rejects it and handles the error.
    
- If the user edits the map, changes are saved before proceeding.
    

### Result

The user has a personalized and editable competency map.

## 4. Initial Competency Assessment

### Goal

Identify the user's existing knowledge and competency gaps.

### Flow

1. SkillLoop selects an initial group of competencies.
    
2. The system prepares diagnostic questions.
    
3. User starts the assessment.
    
4. SkillLoop presents one question at a time.
    
5. User submits an answer.
    
6. AI evaluates the answer.
    
7. The system records the result.
    
8. SkillLoop updates the competency status.
    
9. The system decides whether additional assessment is necessary.
    
10. User continues with the next question or completes the current assessment stage.
    
11. SkillLoop generates an initial competency profile.
    

### Assessment principles

- Assessment is divided into short stages.
    
- Questions should match the expected competency level.
    
- Open-ended answers are supported.
    
- An unanswered question must not automatically mean lack of knowledge.
    
- Unverified competencies remain marked as not assessed.
    

### Result

The user receives an initial competency profile with identified knowledge gaps.

## 5. Selecting a Learning Topic

### Goal

Help the user decide what to learn next.

### Flow

1. SkillLoop analyzes the competency profile.
    
2. The system identifies knowledge gaps and priorities.
    
3. AI recommends a learning topic.
    
4. The user sees the recommendation and its justification.
    
5. User can accept the recommendation or select another topic.
    
6. SkillLoop starts a learning session.
    

### Result

A learning session is associated with a selected competency.

## 6. Learning Through Explanation

### Goal

Check whether the user understands a professional concept and can explain it independently.

### Flow

1. SkillLoop presents the selected topic.
    
2. The system asks the user to explain the concept in their own words.
    
3. User chooses an answer method:
    
    - Text.
        
    - Voice.
        
4. User submits the explanation.
    
5. SkillLoop processes the answer.
    
6. AI evaluates the explanation.
    
7. The system presents structured feedback.
    
8. User can review the feedback and improve their understanding.
    
9. The competency profile is updated.
    

### Evaluation dimensions

- Technical correctness.
    
- Understanding of the concept.
    
- Completeness.
    
- Clarity of explanation.
    

### Result

The user receives an evaluation and an updated competency status.

## 7. Voice Answer Submission

### Goal

Allow users to explain concepts verbally.

### Flow

1. User selects voice input.
    
2. Browser requests microphone permission if necessary.
    
3. User starts recording.
    
4. User explains the topic.
    
5. User stops recording.
    
6. Frontend sends the audio file to FastAPI.
    
7. Backend sends the audio to OpenAI Speech-to-Text.
    
8. The service returns a transcription.
    
9. Backend sends the transcription for AI evaluation.
    
10. The evaluation result is saved.
    
11. Frontend displays the transcription and feedback.
    

### Alternative flows

- If microphone permission is denied, the user can switch to text input.
    
- If recording fails, the user can try again.
    
- If transcription fails, the system displays an error and allows another attempt.
    
- Original audio recordings are not permanently stored by default.
    

### Result

The user's spoken explanation is converted into text and evaluated using the same process as a text answer.

## 8. Text Answer Submission

### Goal

Allow users to explain concepts without speaking aloud.

### Flow

1. User selects text input.
    
2. SkillLoop displays a text editor.
    
3. User writes an explanation.
    
4. User submits the answer.
    
5. Backend sends the text for AI evaluation.
    
6. AI returns a structured evaluation.
    
7. SkillLoop saves the answer and evaluation.
    
8. Frontend displays feedback.
    

### Result

The user's written explanation is evaluated and stored.

## 9. AI Evaluation and Feedback

### Goal

Provide useful feedback that helps users improve their knowledge.

### Flow

1. Backend receives the user's answer or transcription.
    
2. AI analyzes the content against the selected competency.
    
3. AI evaluates the answer.
    
4. AI identifies correct information.
    
5. AI identifies missing or incorrect information.
    
6. AI generates improvement recommendations.
    
7. Backend validates the structured response.
    
8. Backend saves the evaluation.
    
9. Frontend presents the feedback.
    

### Feedback structure

- Overall assessment.
    
- Correctly explained concepts.
    
- Missing information.
    
- Incorrect statements.
    
- Recommended improvements.
    
- Suggested next activity.
    

AI must evaluate subject knowledge separately from the quality of explanation.

For English-language assessments, language quality should also be evaluated separately.

### Result

The user understands what they know, what they misunderstand, and what to improve.

## 10. Learning Recommendations

### Goal

Guide the user toward the most valuable next learning activity.

### Flow

1. SkillLoop retrieves the latest competency profile.
    
2. The system identifies the most important gaps.
    
3. AI considers role requirements and previous assessment results.
    
4. The system selects a recommended topic.
    
5. AI generates a short explanation of the recommendation.
    
6. User accepts the recommendation or chooses another topic.
    

### Result

The user receives a personalized next step instead of having to plan the entire learning process independently.

## 11. Progress Tracking

### Goal

Make competency development visible over time.

### Flow

1. User completes an assessment or learning activity.
    
2. SkillLoop saves the result.
    
3. The system updates the relevant competency status.
    
4. The application updates the user's progress overview.
    
5. User can review previous assessments and feedback.
    

### Progress information

- Competency status.
    
- Assessment history.
    
- Learning activity history.
    
- Identified knowledge gaps.
    
- Improvements over time.
    

### Result

The user can observe how their professional knowledge develops.

## 12. Error Handling Principles

The application should handle the following situations:

- Authentication failure.
    
- AI service unavailable.
    
- Invalid AI response.
    
- Competency map generation failure.
    
- Speech transcription failure.
    
- Microphone permission denied.
    
- Network interruption.
    
- Invalid user input.
    

Errors should be understandable to users and should not expose internal technical details.

The application should avoid losing submitted answers when an operation fails.

## 13. Cross-Device Continuity

The user can access SkillLoop from desktop and mobile devices.

Examples:

- Start a learning session on desktop and continue on mobile.
    
- Submit a voice explanation from a phone.
    
- Review previous feedback on a computer.
    

Learning sessions, answers, and progress must be synchronized through the backend and database.


flowchart TD
    A["Registration / Login"]
    B["Onboarding"]
    C["Select Role and Seniority"]
    D["Generate Competency Map"]
    E["Review and Edit Map"]
    F["Initial Assessment"]
    G["Competency Profile"]
    H["AI Recommends Topic"]
    I["Learning Session"]
    J{"Answer Method"}
    K["Text Explanation"]
    L["Voice Recording"]
    M["Speech-to-Text"]
    N["AI Evaluation"]
    O["Feedback"]
    P["Update Competency Profile"]
    Q["Recommend Next Activity"]

    A --> B --> C --> D --> E --> F --> G
    G --> H --> I --> J
    J --> K --> N
    J --> L --> M --> N
    N --> O --> P --> Q
    Q --> H

---

**End of User Flows – Version 1.0**