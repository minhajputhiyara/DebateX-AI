# DebateX AI - Intelligent Debate System

**DebateX AI** is a debate system powered by advanced AI models. It allows users to engage in structured debates with intelligent debaters and a moderator. This system is designed to simulate engaging and informative discussions on various topics, making it an excellent tool for education, research, and entertainment.

---

## Features

### 1. Dynamic Moderation
- The **Moderator AI** ensures smooth transitions between speakers and keeps the debate engaging and structured.
- It introduces the debate, frames sub-questions, and provides a concluding summary.
- Enhances user experience by maintaining a lively and interactive debate environment.

### 2. Intelligent Debaters
- **Nexia**: A logical thinker focused on Supportive statements, clarity, and evidence-based arguments.
- **Orion**: A creative visionary who presents imaginative, thought-provoking and opposing perspectives.
- Both debaters are designed with opposite views, making every session unique.

### 3. Fact-Checking Integration
- Incorporates a **LangChain Wikipedia tool** to validate claims and ensure factual accuracy.
- Provides real-time corrections to maintain credibility in the debate.

### 4. Customizable Debate Settings
- Users can define:
  - **Debate topic**.
  - **Total debate duration**.
  - **Time limit per turn** for each debater.

---

## Implementation Details

### Technologies Used
- **LLM**: `llama-3.1-70b-versatile` by Groq, for generating intelligent and contextually aware responses.
- **LangChain Framework**: For modular AI system design and integration of tools like the Wikipedia fact-checker.
- **Streamlit**: Powers the user interface, offering a seamless interactive experience.
- **Groq Platform**: Used to run the `llama-3.1-70b-versatile` model efficiently.

---

## Core Components

### 1. Moderator AI
- Frames sub-questions from the input topic to structure the debate.
- Ensures time management and smooth transitions between debaters.
- Provides a concluding summary highlighting key arguments and insights.

### 2. Nexia - Supportive
- Specializes in presenting well-reasoned, evidence-based arguments.
- Aims to build a strong logical foundation for its stance.

### 3. Orion - Opposing
- Offers imaginative and unconventional perspectives.
- Challenges traditional ideas and introduces innovative arguments.

### 4. Fact-Checking Tool
- Uses the LangChain Wikipedia tool to verify key facts presented during the debate.
- Corrects inaccuracies in real-time to enhance the reliability of the discussion.

---

## How It Works

1. **Input Phase**:
   - The user specifies the **debate topic**, **total duration**, and **time per turn**.

2. **Sub-Question Generation**:
   - The Moderator AI generates sub-questions from the topic for structured discussion.

3. **Debate Execution**:
   - Nexia and Orion alternate turns, presenting arguments within the defined time limits.
   - The Moderator AI ensures smooth flow and contextual continuity.

4. **Fact Verification**:
   - Key arguments are validated using the LangChain Wikipedia tool.

5. **Conclusion**:
   - The debate ends with a summary from the Moderator AI, outlining key takeaways and insights.

---------------------------------------------------------------------------------------------------------------------------------------------
