#### SkillLoop – Product Discovery & MVP Specification

**Version:** 1.0  
**Status:** Initial product specification  
**Product type:** Responsive Web Application / PWA

---

## 1. Product Vision

SkillLoop is a personal career knowledge coach that helps people develop, assess, maintain, and demonstrate professional competencies required for their target roles.

The application helps users understand what they need to know, identify knowledge gaps, practice real-world skills, and learn to explain professional concepts clearly.

SkillLoop combines AI-powered competency assessment, personalized learning recommendations, practical exercises, and spaced repetition.

**Core principle:**

Know it. Explain it. Apply it.

## 2. Problem Statement

People preparing for a new job or developing their professional skills often face several problems:

- They don't know exactly what they should learn for a particular role.
    
- They struggle to identify gaps in their knowledge.
    
- They don't know which topics deserve the most attention.
    
- They consume educational content but rarely verify whether they understand it.
    
- They can recognize concepts but struggle to explain them during interviews.
    
- They forget previously learned information.
    
- They don't know whether they can apply theoretical knowledge in practice.
    

SkillLoop addresses these problems through a structured, personalized learning process.

## 3. Target Users

Primary users:

People who want to:

- Change careers.
    
- Prepare for a new professional role.
    
- Prepare for technical job interviews.
    
- Improve their existing professional competencies.
    
- Maintain and develop their knowledge over time.
    

Initial supported roles should be configurable rather than limited to one profession.

## 4. User Onboarding

During onboarding, the user:

1. Selects a target professional role.
    
2. Selects a target seniority level:
    
    - Junior
        
    - Mid
        
    - Senior
        
3. Describes their current experience.
    
4. Defines their available daily learning time.
    
5. Selects a weekly rest day.
    

### AI-generated competency map

AI generates a competency map based on the selected role and seniority.

For each competency, AI should provide:

- Competency name and description.
    
- Expected proficiency level.
    
- Importance for the selected role.
    
- Explanation of why the competency is required.
    
- Expected knowledge and practical skills.
    
- Recommended assessment method.
    

### Knowledge expectations

Each competency should be classified into three categories:

1. **Know from memory:** Concepts, principles, and essential knowledge that should be recalled without documentation.
    
2. **Know how to apply:** Skills that should be demonstrated through practical tasks.
    
3. **Know where to find:** Information that can reasonably be retrieved from official documentation or other reliable sources.
    

Users can edit the competency map and add missing topics.

## 5. Competency Assessment

SkillLoop conducts an initial competency assessment divided into short stages.

The assessment should not overwhelm the user with one long test.

Assessment methods:

- Theoretical questions.
    
- Open-ended explanations.
    
- Practical exercises.
    
- Explanation of practical solutions.
    

Users can submit explanations in two ways:

- Voice recording.
    
- Text input.
    

AI evaluates knowledge and the ability to explain concepts.

### Competency status

The system distinguishes between:

- Not assessed.
    
- Insufficient knowledge.
    
- Partially understood.
    
- Competency demonstrated.
    
- Well established.
    

An unanswered question must not automatically be treated as proof that the user lacks a competency.

The assessment continues throughout the learning process. New answers and practical results update the competency profile.

## 6. Learning Process

The core learning loop for an individual topic:

1. SkillLoop selects or recommends a topic.
    
2. The system checks what the user already knows.
    
3. The user explains the topic or completes a practical exercise.
    
4. AI identifies knowledge gaps.
    
5. SkillLoop provides explanations and learning materials.
    
6. The user practices again.
    
7. AI evaluates the result.
    
8. The competency profile and repetition schedule are updated.
    

### Two learning methods

**A. Explain a concept**

The user explains a topic in their own words.

AI evaluates:

- Technical correctness.
    
- Understanding of the concept.
    
- Completeness.
    
- Ability to explain it clearly.
    

**B. Practical exercise**

The user performs a task and explains the solution.

AI evaluates:

- Practical solution.
    
- Correctness of the implementation.
    
- Understanding of the approach.
    
- Ability to explain decisions and results.
    

## 7. Practical Exercises

Two exercise sources:

- AI-generated exercises based on the competency map.
    
- User-created exercises.
    

Users can add:

- Exercise descriptions.
    
- Source code files.
    
- Technical documentation.
    

AI analyzes submitted materials and the user's explanation.

PDF files and screenshots are outside the initial MVP scope.

## 8. AI Career Coach

SkillLoop should actively guide the user.

The system recommends:

- What to learn next.
    
- Which knowledge gaps have the highest priority.
    
- Which topics need revision.
    
- Which practical exercises should be completed.
    
- Which competencies need further assessment.
    

AI recommendations should include explanations.

The user retains control over the learning plan and competency map.

## 9. Spaced Repetition

SkillLoop includes an Anki-inspired repetition system.

Repetition scheduling uses four criteria:

1. AI assessment.
    
2. User self-assessment.
    
3. Answer correctness.
    
4. Practical exercise performance, when applicable.
    

The system adjusts repetition intervals according to demonstrated knowledge.

Repetition activities can include:

- Explaining a concept again.
    
- Answering a question.
    
- Solving a new practical exercise.
    

Not every repetition requires a practical exercise.

## 10. Competency Profile and Knowledge Graph

SkillLoop maintains an evolving competency profile.

The knowledge graph visualizes:

- Competencies and related topics.
    
- Relationships between topics.
    
- Current proficiency.
    
- Practical achievements.
    
- Demonstrated competencies.
    

Practical achievements should be linked to relevant competencies.

The system must distinguish between theoretical knowledge and practical skills demonstrated through completed exercises.

## 11. Progress and Gamification

The MVP includes lightweight gamification:

- Experience points (XP).
    
- User levels.
    
- Consecutive learning-day streaks.
    
- Achievement badges.
    
- Weekly rest day.
    

The user selects one weekly rest day. This day does not break the learning streak.

XP should reward meaningful learning activities rather than simple clicks or passive activity.

## 12. Learning Schedule

The user defines their available daily learning time.

SkillLoop creates a personalized daily learning plan based on:

- Available time.
    
- Repetitions due.
    
- Knowledge gaps.
    
- Learning priorities.
    
- Previous results.
    

The user can modify the plan.

## 13. Platform

Initial platform: responsive web application with PWA support.

The same account and learning progress should be available on desktop and mobile devices.

### Desktop priorities

- Practical exercises.
    
- Code and documentation uploads.
    
- Competency map editing.
    
- Knowledge graph.
    
- Detailed progress reports.
    

### Mobile priorities

- Voice-based explanations.
    
- Text-based answers.
    
- Knowledge repetitions.
    
- Daily learning plan.
    
- Progress overview.
    

A learning session should be accessible across devices.

Example: the user performs a task on their computer and later explains the solution using their phone.

## 14. Out of Scope for Initial MVP

The following features are postponed:

- Job offer import and automatic job requirement analysis.
    
- PDF analysis.
    
- Screenshot analysis.
    
- Screen recording analysis.
    
- Separate native iOS and Android applications.
    
- Real-time conversational AI tutor.
    
- Complex social and competitive gamification.
    

## 15. MVP Success Criteria

The MVP should demonstrate that a user can:

1. Create an account and select a target professional role.
    
2. Generate and edit an AI competency map.
    
3. Complete an initial competency assessment.
    
4. Receive a personalized learning recommendation.
    
5. Learn by explaining concepts using voice or text.
    
6. Complete practical exercises.
    
7. Upload code and technical documentation.
    
8. Receive structured AI feedback.
    
9. Schedule and complete knowledge repetitions.
    
10. Track competency development.
    
11. View a knowledge graph.
    
12. Earn XP, levels, and badges.
    
13. Continue learning across desktop and mobile devices.
    

### Primary product success indicator

The user regularly returns to SkillLoop, completes learning activities, and demonstrates measurable improvement in professional competencies.

---

## 16. Product Principles

1. AI guides the user but does not take away their control.
    
2. Practical ability matters as much as theoretical knowledge.
    
3. The ability to explain knowledge is a core competency.
    
4. Learning should adapt to the user's actual skill level.
    
5. Repetition should be based on demonstrated knowledge.
    
6. The competency map should evolve with the user.
    
7. The product should distinguish between knowledge that must be memorized and information that can be retrieved when needed.
    
8. The interface should support short, focused learning sessions.
    

**End of specification – Version 1.0**