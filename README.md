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
- <img width="1897" height="871" alt="image" src="https://github.com/user-attachments/assets/8f5a7477-dc87-4ff1-a699-21d82fd161d2" />

- Dashboard
- <img width="1827" height="900" alt="image" src="https://github.com/user-attachments/assets/115efd07-4dda-4bcf-9e13-84bf5ff42af5" />

- Daily Planner
- <img width="1895" height="893" alt="image" src="https://github.com/user-attachments/assets/98cd8dd4-4ab3-49af-958b-3f4d496ca5f2" />

- Revision Planner
- <img width="1897" height="895" alt="image" src="https://github.com/user-attachments/assets/91475877-5f21-4b01-ad42-f4afb9e69bf6" />

- AI Study Assistant
- <img width="1912" height="891" alt="image" src="https://github.com/user-attachments/assets/9bacaa06-9f83-4659-b0bc-065cc2fe4f9e" />

- Interview Preparation
- <img width="1912" height="917" alt="image" src="https://github.com/user-attachments/assets/6adb3e4e-7bc5-4b60-902a-e5b912cb79fc" />

- Analytics
- <img width="1905" height="910" alt="image" src="https://github.com/user-attachments/assets/694789d5-f401-46f7-94bc-e80087c5e2fa" />

- Daily Tasks
- <img width="1911" height="892" alt="image" src="https://github.com/user-attachments/assets/7ed39cfb-304b-465e-9392-71fc267c2e0c" />

- Streak Tracker
- <img width="1907" height="890" alt="image" src="https://github.com/user-attachments/assets/ad281a60-4eeb-4825-be67-3d6ea7e8afd8" />


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

