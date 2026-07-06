# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import List, Optional
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


def generate_daily_study_plan(study_hours: int, subjects: List[str], goals: Optional[str] = None) -> str:
    """Generates a structured hour-by-hour daily study plan based on total study hours, target subjects, and specific goals.

    Args:
        study_hours: Total number of hours available to study in the day.
        subjects: List of subjects or topics to cover.
        goals: Optional specific goals or focus for the day.

    Returns:
        A formatted markdown daily study schedule.
    """
    if study_hours <= 0:
        return "Please specify a positive number of study hours."
    if not subjects:
        return "Please specify at least one subject to study."

    per_subject_time = study_hours / len(subjects)
    
    plan = []
    plan.append(f"## 📅 StudyPilot-AI Daily Study Plan ({study_hours} Hours Total)")
    if goals:
        plan.append(f"**Focus Goal:** {goals}\n")
        
    plan.append("### ⏰ Suggested Schedule")
    
    current_hour = 9  # Start study at 9:00 AM
    for idx, subject in enumerate(subjects):
        duration = per_subject_time
        start_time = f"{current_hour:02d}:00"
        
        end_hour = current_hour + int(duration)
        end_minute = int((duration - int(duration)) * 60)
        end_time = f"{end_hour:02d}:{end_minute:02d}"
        
        plan.append(f"- **{start_time} - {end_time}**: 📚 Study **{subject}** ({duration:.1f} hrs)")
        plan.append(f"  - *Focus*: Core concepts, practice problems, and active recall.")
        
        if idx < len(subjects) - 1:
            plan.append(f"- **{end_time} - {end_hour:02d}:10**: ☕ Short Break & Stretch (10 mins)")
            current_hour = end_hour
        else:
            current_hour = end_hour
            
    plan.append("\n> [!TIP]\n> Use the Pomodoro Technique (25m study, 5m break) within each block to maintain high focus!")
    return "\n".join(plan)





def generate_revision_plan(topics: List[str], available_days: int) -> str:
    """Generates a revision planning schedule using spaced repetition strategies over available days.

    Args:
        topics: A list of topics that need revision.
        available_days: Number of days available until exam/evaluation.

    Returns:
        A markdown-formatted revision schedule.
    """
    if available_days <= 0:
        return "Please specify a positive number of available days."
    if not topics:
        return "Please specify at least one topic to revise."
        
    plan = []
    plan.append(f"## 🔁 Spaced Repetition Revision Plan ({available_days} Days)")
    
    # Distribute topics across the days
    plan.append("### 📅 Daily Focus Schedule")
    for day in range(1, available_days + 1):
        # Pick topic(s) for the day
        topic_idx = (day - 1) % len(topics)
        current_topic = topics[topic_idx]
        
        # Suggest revision mode based on day cycle
        if day <= len(topics):
            mode = "First Review (Active Recall + Summary Cards)"
        elif day <= 2 * len(topics):
            mode = "Second Review (Solve Practice Problems)"
        else:
            mode = "Final Review (Timed Mock Test / Flashcards)"
            
        plan.append(f"- **Day {day}**: 🔍 Revise **{current_topic}**")
        plan.append(f"  - *Mode*: {mode}")
        
    plan.append("\n> [!NOTE]\n> Ensure you spend 70% of revision time practicing active recall (e.g. testing yourself) rather than passive reading.")
    return "\n".join(plan)


def generate_interview_prep_questions(role: str, topics: List[str], difficulty: str = "Medium") -> str:
    """Formulates target interview prep questions, tips, and mock-interview guidelines based on the role and topics.

    Args:
        role: The target job role (e.g. Software Engineer, Frontend Engineer, Data Scientist).
        topics: The technical topics to focus on (e.g. System Design, Recursion, Databases).
        difficulty: The target difficulty level (Easy, Medium, Hard).

    Returns:
        A structured study guide with mock interview questions and advice.
    """
    prep = []
    prep.append(f"## 💼 Interview Prep Guide for **{role}** ({difficulty} Difficulty)")
    
    prep.append("### 🎯 Core Focus Areas")
    for t in topics:
        prep.append(f"- **{t}**")
        
    prep.append("\n### ❓ Sample Mock Interview Questions")
    if "system design" in [t.lower() for t in topics]:
        prep.append("1. *System Design*: How would you design a scalable notification service?")
        prep.append("2. *System Design*: Design a rate limiter for an API gateway.")
    else:
        prep.append(f"1. Explain the internal working of {topics[0] if topics else 'the core tech stack'}.")
        prep.append(f"2. Describe a time you faced a complex technical challenge with {topics[-1] if topics else 'software development'} and how you solved it.")
        
    prep.append("\n### 💡 Preparation Tips")
    prep.append("- **STAR Method**: Use Situation, Task, Action, Result to structure your behavioral answers.")
    prep.append("- **Think Out Loud**: In technical rounds, communicate your thought process constantly to the interviewer.")
    
    return "\n".join(prep)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are StudyPilot-AI, a premium AI Study Companion designed to help students optimize their study habits. "
        "You can assist students with Daily Study Planning, Revision Planning, and Interview Preparation. "
        "Always call the appropriate helper tool to generate structured plans, revision schedules, or interview guides, "
        "and present the output beautifully with modern markdown and tips."
    ),
    tools=[
        generate_daily_study_plan,
        generate_revision_plan,
        generate_interview_prep_questions
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
