 ### **SkillLoop – MVP Scope**

**Version:** 1.0  
**Status:** Draft  
**Product:** SkillLoop – Personal Career Knowledge Coach  
**Platform:** Responsive Web Application / PWA

---

## 1. MVP Objective

The goal of the first SkillLoop MVP is to validate whether an AI-powered career knowledge coach can help users:

- Understand what they need to know for a selected professional role.
    
- Assess their current knowledge and identify competency gaps.
    
- Learn by explaining professional concepts in their own words.
    
- Receive meaningful AI-powered feedback.
    
- Get recommendations about what to learn next.
    

The first version focuses on the core learning and assessment experience.

The MVP will initially be tested by its creator as the primary user.

## 2. Target User

A person who wants to develop professional competencies or prepare for a new career role.

The user selects:

- Target professional role.
    
- Target seniority: Junior, Mid or Senior.
    
- Current experience and knowledge level.
    

Initial testing will use the DevOps Engineer role.

The application must not be limited to DevOps.

## 3. Core Features – In Scope

### 3.1 User Profile and Onboarding

The user can:

- Create an account and log in.
    
- Select a target professional role.
    
- Select a target seniority level.
    
- Provide basic information about current experience.
    

The application stores the user's profile and learning progress.

### 3.2 AI-Generated Competency Map

AI generates a competency map based on the selected role and seniority.

Each competency contains:

- Name.
    
- Description.
    
- Importance for the selected role.
    
- Expected proficiency level.
    
- Explanation of why it is required.
    
- Expected knowledge and skills.
    

Competencies are classified into:

1. Knowledge required from memory.
    
2. Skills that must be demonstrated in practice.
    
3. Information that can be retrieved from documentation.
    

The user can:

- View the competency map.
    
- Edit competency names and descriptions.
    
- Add missing competencies.
    
- Remove irrelevant competencies.
    

### 3.3 Initial Competency Assessment

SkillLoop conducts a short, staged assessment.

The assessment includes:

- Knowledge questions.
    
- Open-ended explanations.
    
- Questions adapted to the user's previous answers.
    

The assessment should identify:

- Existing knowledge.
    
- Knowledge gaps.
    
- Topics requiring further assessment.
    
- Competencies not yet verified.
    

The application must distinguish between missing knowledge and knowledge that has not yet been assessed.

### 3.4 Learning by Explanation

The user selects a topic and explains it in their own words.

Two input methods are supported:

**Text input**

- The user writes an explanation.
    
- AI analyzes the submitted text.
    

**Voice input**

- The user records an explanation.
    
- Speech is converted into text.
    
- AI analyzes the transcribed answer.
    

The application does not include real-time voice conversations with AI.

AI evaluates:

- Technical correctness.
    
- Understanding of the concept.
    
- Completeness.
    
- Clarity of explanation.
    

### 3.5 AI Feedback

After each assessment, SkillLoop provides structured feedback.

The feedback includes:

- What the user explained correctly.
    
- What is missing or incorrect.
    
- Which concepts require clarification.
    
- Recommended next steps.
    

The application updates the user's competency profile based on assessment results.

### 3.6 AI Learning Recommendations

SkillLoop recommends the next learning activity based on:

- Competency gaps.
    
- Assessment results.
    
- Importance of competencies for the selected role.
    
- Previously completed learning activities.
    

The user can accept a recommendation or select another topic from the competency map.

Recommendations must include a short explanation of why a topic is recommended.

### 3.7 Basic Learning Progress

The user can view:

- Current competency status.
    
- Completed assessments.
    
- Learning history.
    
- Topics that need improvement.
    

The application provides a basic overview of learning progress.

## 4. Basic Platform Requirements

The MVP is a responsive web application with PWA support.

It must work on:

- Desktop browsers.
    
- Mobile browsers.
    

The application must provide:

- One user account across devices.
    
- Persistent user data.
    
- Synchronized learning progress.
    
- Responsive interface.
    
- Voice and text input for explanations.
    

The user must be able to start learning on one device and continue on another.

## 5. Deferred Features – Not Included in Initial MVP

The following features are part of the product vision but are not required for the first working version.

### Practical Exercises

- AI-generated practical tasks.
    
- User-created practical tasks.
    
- Uploading source code.
    
- Uploading technical documentation.
    
- AI analysis of practical solutions.
    
- Linking practical achievements to competencies.
    

### Spaced Repetition

- Anki-inspired repetition scheduling.
    
- Adaptive repetition intervals.
    
- Four-factor assessment:
    
    - AI assessment.
        
    - User self-assessment.
        
    - Answer correctness.
        
    - Practical exercise performance, when applicable.
        

### Learning Schedule

- User-defined daily learning time.
    
- Personalized daily learning plans.
    
- Weekly rest day.
    
- Automatic prioritization of repetitions and new topics.
    

### Knowledge Graph

- Interactive knowledge graph.
    
- Relationships between competencies.
    
- Visualization of theoretical and practical achievements.
    

### Gamification

- Experience points (XP).
    
- User levels.
    
- Learning streaks.
    
- Weekly rest day support for streaks.
    
- Achievement badges.
    

### Additional Features

- Job offer import and analysis.
    
- PDF analysis.
    
- Screenshot analysis.
    
- Real-time conversational AI tutor.
    
- Native Android and iOS applications.
    
- Social features and leaderboards.
    

## 6. MVP User Journey

The first MVP must support the following complete user journey:

1. The user creates an account.
    
2. The user selects a professional role and target seniority.
    
3. AI generates a competency map.
    
4. The user reviews and edits the map.
    
5. SkillLoop starts the initial competency assessment.
    
6. The user answers questions.
    
7. The user receives an assessment and competency profile.
    
8. SkillLoop recommends a topic to learn.
    
9. The user studies the topic and explains it using voice or text.
    
10. AI evaluates the explanation and provides feedback.
    
11. SkillLoop updates the competency profile.
    
12. SkillLoop recommends the next learning activity.
    

## 7. MVP Acceptance Criteria

The MVP is considered functional when:

- A user can create an account and log in.
    
- A user can select a target role and seniority.
    
- AI can generate a competency map.
    
- The user can edit the generated map.
    
- The user can complete a staged assessment.
    
- AI can evaluate open-ended answers.
    
- The user can submit explanations using text.
    
- The user can submit explanations using voice.
    
- AI can provide structured feedback.
    
- Competency statuses are updated after assessments.
    
- SkillLoop can recommend the next topic.
    
- User data and learning progress persist across sessions.
    
- The application works on desktop and mobile browsers.
    

## 8. MVP Validation

The first validation phase is based on personal use.

The primary test scenario is learning DevOps competencies.

The MVP should answer the following questions:

1. Does AI generate a useful competency map?
    
2. Are the competency expectations appropriate for the selected seniority?
    
3. Does the assessment identify actual knowledge gaps?
    
4. Is AI feedback useful and technically accurate?
    
5. Does explaining concepts improve understanding?
    
6. Are learning recommendations relevant?
    
7. Is the learning process easy to use on both desktop and mobile?
    

The MVP should be evaluated based on actual learning usefulness, not the number of implemented features.

## 9. Scope Principles

1. Build the smallest complete learning experience.
    
2. Prioritize reliable AI assessment over the number of AI features.
    
3. Keep the user in control of the competency map and learning decisions.
    
4. Avoid building features that do not support the core learning loop.
    
5. Keep the architecture extensible for practical exercises, spaced repetition, knowledge graphs and gamification.
    
6. Prefer simple, maintainable implementations.
    
7. Avoid unnecessary infrastructure and cloud costs.
    

---

**End of MVP Scope – Version 1.0**