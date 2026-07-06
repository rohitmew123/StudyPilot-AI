# 🚀 StudyPilot AI

> **An AI-powered Student Productivity Platform built using Python, Streamlit, SQLite, Google ADK, and AI Agents.**

StudyPilot AI is an intelligent student productivity platform designed to help students organize their studies, generate personalized study plans, prepare for interviews, revise efficiently, and track their learning progress using AI-powered agents.

This project was developed as the capstone project for the **Kaggle 5-Day AI Agents: Intensive Vibe Coding Course with Google**.

---

# 🌟 Features

## 📊 Dashboard
- Personalized dashboard
- Study statistics
- Daily progress
- Focus score
- Streak tracking
- Recent activity

---

## 📅 Daily Planner

Generate AI-powered daily study plans based on:

- Available study hours
- Subjects
- Priorities
- Goals

Users can edit and manage their daily schedule.

---

## 📚 Revision Planner

Generate personalized revision schedules.

Features include:

- Topic-based revision
- Multi-day planning
- Saved revision plans
- SQLite persistence

---

## 🤖 AI Study Assistant

An AI-powered study companion capable of:

- Answering study questions
- Providing explanations
- Helping with concepts
- Learning guidance

(Currently uses a fallback assistant and is designed for future Gemini API integration.)

---

## 💼 Interview Preparation

Prepare for technical interviews using AI assistance.

Supports preparation for:

- DSA
- DBMS
- Operating Systems
- Computer Networks
- HR Interview Questions

---

## ✅ Daily Task Manager

Manage study tasks with:

- Add tasks
- Edit tasks
- Delete tasks
- Complete tasks
- Daily progress tracking

---

## 🔥 Streak Tracking

Track study consistency through:

- Daily streaks
- Focus score
- Progress statistics

---

## 📈 Analytics

Visualize study progress using charts:

- Study hours
- Subject distribution
- Weekly progress
- Performance insights

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
         Google ADK AI Agent
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
 Daily Planner  AI Assistant  Revision Planner
      │           │            │
      └───────────┼────────────┘
                  ▼
            SQLite Database
```

---

# 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Database
- SQLite

### AI & Agent Framework
- Google ADK
- Agents CLI
- Antigravity IDE

### Deployment Ready
- FastAPI
- Docker

---

# 📂 Project Structure

```
StudyPilot-AI/

├── app/
│   ├── agent.py
│   ├── auth.py
│   ├── database.py
│   ├── planner.py
│   └── helpers/
│
├── frontend/
│   └── main.py
│
├── tests/
│
├── deployment/
│
├── README.md
│
└── pyproject.toml
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/rohitmew123/StudyPilot-AI.git
```

Move into the project

```bash
cd StudyPilot-AI
```

Install dependencies

```bash
uv sync
```

Run the application

```bash
streamlit run frontend/main.py
```

---

# 🤖 AI Agent Concepts Used

This project demonstrates multiple concepts from Google's AI Agents course:

- ✅ Google ADK Agent
- ✅ Agent Skills
- ✅ Antigravity IDE
- ✅ AI-assisted Development
- ✅ Deployable Agent Architecture

---

# 📸 Screenshots

Add screenshots of:

- Login
- Dashboard
- Daily Planner
- Revision Planner
- AI Study Assistant
- Interview Preparation
- Analytics

---

# 🎯 Future Improvements

- Gemini API Integration
- Multi-Agent Collaboration
- Cloud Database
- Notifications
- Mobile Application
- AI Voice Assistant
- Calendar Sync
- PDF Report Generation

---

# 👨‍💻 Author

**Rohit Mewada**

Student Developer

Built for the **Kaggle AI Agents: Intensive Vibe Coding Capstone Project**.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

