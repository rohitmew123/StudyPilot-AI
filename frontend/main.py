import sys
import os
# Force resolving local app imports from workspace root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from app.database import (
    init_db, update_streak_state, update_streak, update_freeze_count,
    get_tasks, add_task, update_task_status, delete_task, edit_task,
    get_revision_plans, save_revision_plan,
    get_chat_history, save_chat_message,
    get_study_sessions, add_study_session,
    get_user_by_id
)
from app.auth import register_user, authenticate_user, check_and_update_streak_on_task_completion, evaluate_streak_on_login
from app.agent import (
    generate_daily_study_plan,
    generate_revision_plan,
    generate_interview_prep_questions,
    root_agent
)

# Set page config for a premium and modern look
st.set_page_config(
    page_title="StudyPilot AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (custom student-friendly fonts, glassmorphism card layouts, smooth transitions)

st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Set main font family & base styling */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC;
    }
    
    /* Header Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
    }
    
    /* Premium Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar Navigation Items */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: transparent;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s ease;
        margin-bottom: 4px;
        border: 1px solid transparent;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #1E293B;
        color: #F8FAFC !important;
    }
    
    /* Gradient Headings */
    .gradient-text {
        background: linear-gradient(135deg, #6366F1 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Premium Glassmorphism Stats Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.04), 0 1px 1px 0 rgba(255, 255, 255, 0.8) inset;
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366F1, #10B981);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -15px rgba(99, 102, 241, 0.15), 0 1px 1px 0 rgba(255, 255, 255, 0.8) inset;
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* Metric Card Internal Titles & Values */
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        font-family: 'Outfit', sans-serif;
        line-height: 1.1;
    }
    
    /* Modern Card Container */
    .premium-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .premium-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
        border-color: #CBD5E1;
    }
    
    /* Info Banners / Tip Box */
    .tip-box {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 5px solid #6366F1;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px -5px rgba(99, 102, 241, 0.1);
        color: #3730A3;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Sidebar Logout Button */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.02em;
        width: 100% !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.3) !important;
    }
    
    /* Primary buttons in application */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35) !important;
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
    }

    /* Form Fields and Inputs Styling */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox select {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease !important;
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }
    
    /* Modern Chat Bubble UI */
    .chat-bubble {
        padding: 16px 20px;
        border-radius: 16px;
        margin-bottom: 12px;
        line-height: 1.5;
        font-size: 0.95rem;
        max-width: 85%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .chat-user {
        background-color: #6366F1;
        color: #FFFFFF;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    .chat-assistant {
        background-color: #F1F5F9;
        color: #0F172A;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #E2E8F0;
    }
    
    /* Streak visual badge */
    .streak-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        border: 1px solid #F59E0B;
        color: #B45309;
        padding: 6px 14px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        gap: 6px;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
    }

    /* Custom alert box */
    .modern-alert {
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #10B981;
        background-color: #ECFDF5;
        color: #065F46;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Custom spacing and margins */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database and authenticate user
init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# If authenticated, retrieve latest stats and tasks from DB to replace mock values
if st.session_state.authenticated and st.session_state.user:
    st.session_state.user = get_user_by_id(st.session_state.user["id"])
    st.session_state.streak = st.session_state.user["streak"]
    
    today_str = datetime.date.today().isoformat()
    st.session_state.tasks = get_tasks(st.session_state.user["id"], today_str)
    st.session_state.checked_in_today = (st.session_state.user.get("last_activity_date") == today_str)
else:
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "checked_in_today" not in st.session_state:
        st.session_state.checked_in_today = False
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

# If not authenticated, show authentication pages (Login / Sign Up)
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'><span class='gradient-text'>StudyPilot AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.15rem; color: #64748B; font-weight: 500;'>Plan • Learn • Track • Achieve</p>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        auth_mode = st.tabs(["🔑 Login", "📝 Sign Up"])
        
        with auth_mode[0]:
            st.markdown("### Welcome Back")
            username_email = st.text_input("Username or Email", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Log In", type="primary", use_container_width=True):
                user = authenticate_user(username_email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.streak = user["streak"]
                    st.success(f"Welcome back, {user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid username/email or password.")
                    
        with auth_mode[1]:
            st.markdown("### Create an Account")
            new_user = st.text_input("Choose Username", key="reg_user")
            new_email = st.text_input("Email Address", key="reg_email")
            new_pass = st.text_input("Password (min 6 chars)", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", type="primary", use_container_width=True):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    res = register_user(new_user, new_email, new_pass)
                    if res["success"]:
                        st.success(res["message"] + " You can now log in.")
                    else:
                        st.error(res["message"])
    st.stop()

# Header section
col_logo, col_title = st.columns([1, 12])
with col_title:
    st.markdown("<h1 style='margin-bottom: 0px;'><span class='gradient-text'>StudyPilot AI</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.15rem; color: #64748B; font-weight: 500;'>Plan • Learn • Track • Achieve</p>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("<h2 style='text-align: center; font-size: 1.6rem;'>🚀 Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Choose a workspace",
    [
        "Dashboard",
        "Daily Planner",
        "Revision Planner",
        "Interview Preparation",
        "AI Study Assistant",
        "Daily Tasks",
        "Streak Tracker",
        "Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='background-color: #1E293B; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #334155; margin-bottom: 10px;'>
    <div style='display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 8px;'>
        <div style='width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981;'></div>
        <span style='color: #10B981; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>Active Now</span>
    </div>
    <span style='color: #94A3B8; font-size: 0.85rem;'>Logged in as</span><br/>
    <strong style='color: #F8FAFC; font-size: 1.05rem; font-family: "Outfit", sans-serif;'>{st.session_state.user["username"]} 🎓</strong>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


# --- 1. Dashboard View ---
if page == "Dashboard":
    st.subheader(f"👋 Welcome back, {st.session_state.user['username']}!")
    st.write("Here is your study overview for today. Stay focused and keep the streak alive!")
    
    # Calculate real today's study hours from sessions
    today_str = datetime.date.today().isoformat()
    sessions = get_study_sessions(st.session_state.user["id"])
    today_sessions = [s for s in sessions if s["study_date"] == today_str]
    today_hours = sum(s["duration_minutes"] for s in today_sessions) / 60.0
    
    # Calculate weekly progress (Target: 20 hours)
    weekly_minutes = 0
    for s in sessions:
        try:
            s_date = datetime.date.fromisoformat(s["study_date"])
            if (datetime.date.today() - s_date).days < 7:
                weekly_minutes += s["duration_minutes"]
        except Exception:
            pass
    weekly_hours = weekly_minutes / 60.0
    progress_pct = min(int((weekly_hours / 20.0) * 100), 100)
    
    # Grid of Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current Streak</div>
            <div class="metric-value" style="color: #EF4444;">🔥 {st.session_state.streak} Days</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        completed = sum(1 for t in st.session_state.tasks if t["done"])
        total = len(st.session_state.tasks)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Tasks Completed</div>
            <div class="metric-value" style="color: #10B981;">✅ {completed}/{total}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Today's Study Time</div>
            <div class="metric-value" style="color: #3B82F6;">⏱️ {today_hours:.1f} hrs</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        # Dynamic data-driven focus score
        task_ratio = completed / total if total > 0 else 0.0
        hours_ratio = min(today_hours / 6.0, 1.0)
        focus_score = int(40 + (task_ratio * 40) + (hours_ratio * 20)) if (total > 0 or today_hours > 0) else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Focus Score</div>
            <div class="metric-value" style="color: #8B5CF6;">🎯 {focus_score}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activities & Motivation
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("### 📝 High Priority Tasks for Today")
        if not st.session_state.tasks:
            st.info("No tasks scheduled for today. Add tasks in the Daily Planner or Daily Tasks tab.")
        else:
            for t in st.session_state.tasks[:3]:
                status = "✅" if t["done"] else "⏳"
                st.markdown(f"- {status} **{t['text']}**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tip-box">
            <h4>💡 Student Tip of the Day</h4>
            <p><strong>Spaced Repetition:</strong> Don't try to cram everything at once. Revisit challenging DSA concepts at intervals of 1, 3, and 7 days to solidify memory encoding!</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_side:
        st.markdown("### ⏱️ Recent Activity")
        if not sessions:
            st.info("No recent study sessions logged. Start logging sessions in the Analytics tab!")
        else:
            for s in sessions[:3]:
                st.write(f"📚 **{s['subject']}**: {s['duration_minutes']} mins on {s['study_date']}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.progress(progress_pct / 100.0, text=f"Weekly goal progress: {progress_pct}% ({weekly_hours:.1f}/20 hrs)")


# --- 2. Daily Planner View ---
elif page == "Daily Planner":
    st.markdown("<h2 style='font-family: Outfit; font-weight: 700; color: #0F172A;'>📅 Daily Study Planner</h2>", unsafe_allow_html=True)
    st.write("Structure your day logically, generate smart schedules, and manage your tasks.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1, 1])
    with col_input:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ Plan Generator")
        study_hours = st.slider("Total Study Hours Available Today", 1, 16, 6)
        subjects = st.multiselect(
            "Select Subjects to Focus On",
            ["Data Structures", "Operating Systems", "Computer Networks", "Database Management", "System Design", "General Aptitude"],
            default=["Data Structures", "Operating Systems"]
        )
        goals = st.text_area("What is your primary goal for today?", placeholder="e.g. Solve dynamic programming basics and review CPU scheduling.")
        
        btn_generate = st.button("Generate Smart Study Plan", type="primary")
        
        if btn_generate:
            if not subjects:
                st.error("Please select at least one subject.")
            else:
                st.session_state.last_generated_plan = generate_daily_study_plan(study_hours, subjects, goals)
                st.success("Plan generated successfully!")
        
        if "last_generated_plan" in st.session_state:
            st.markdown("### ⏰ Generated Schedule")
            st.markdown(st.session_state.last_generated_plan)
            if st.button("➕ Save Schedule to Today's Tasks"):
                today_date = datetime.date.today().isoformat()
                for sub in subjects:
                    per_subject = study_hours / len(subjects)
                    add_task(st.session_state.user["id"], f"Study {sub} ({per_subject:.1f} hrs)", today_date)
                st.toast("Tasks added to your daily list!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_result:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Manage Today's Tasks")
        
        # Add new task form
        with st.form("new_task_form_planner", clear_on_submit=True):
            new_task_text = st.text_input("Add a custom task:")
            submit_task = st.form_submit_button("Add Task")
            if submit_task and new_task_text:
                today_date = datetime.date.today().isoformat()
                add_task(st.session_state.user["id"], new_task_text, today_date)
                st.toast("Task added!")
                st.rerun()
                
        # Tasks List
        today_date = datetime.date.today().isoformat()
        current_tasks = get_tasks(st.session_state.user["id"], today_date)
        
        if not current_tasks:
            st.info("No tasks scheduled for today yet. Use the generator on the left or add a custom task.")
        else:
            for t in current_tasks:
                task_col_check, task_col_text, task_col_actions = st.columns([1, 6, 3])
                with task_col_check:
                    done_val = bool(t["done"])
                    checked = st.checkbox("", value=done_val, key=f"plan_check_{t['id']}")
                    if checked != done_val:
                        update_task_status(t["id"], 1 if checked else 0)
                        streak_increased = check_and_update_streak_on_task_completion(st.session_state.user["id"])
                        if streak_increased:
                            st.toast("🔥 Awesome! All tasks completed today, streak increased!")
                        st.rerun()
                with task_col_text:
                    st.write(t["text"])
                with task_col_actions:
                    col_edit, col_del = st.columns(2)
                    with col_edit:
                        if st.button("✏️", key=f"edit_btn_{t['id']}"):
                            st.session_state.editing_task_id = t["id"]
                            st.session_state.editing_task_text = t["text"]
                    with col_del:
                        if st.button("🗑️", key=f"del_btn_{t['id']}"):
                            delete_task(t["id"])
                            st.toast("Task deleted!")
                            st.rerun()
            
            # Show Edit Dialog if editing
            if "editing_task_id" in st.session_state:
                st.markdown("---")
                st.markdown("#### Edit Task")
                new_edit_text = st.text_input("Update task description:", value=st.session_state.editing_task_text)
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("Save Changes"):
                        edit_task(st.session_state.editing_task_id, new_edit_text)
                        del st.session_state["editing_task_id"]
                        del st.session_state["editing_task_text"]
                        st.toast("Task updated!")
                        st.rerun()
                with col_cancel:
                    if st.button("Cancel"):
                        del st.session_state["editing_task_id"]
                        del st.session_state["editing_task_text"]
                        st.rerun()


        st.markdown('</div>', unsafe_allow_html=True)


# --- 4. Revision Planner View ---
elif page == "Revision Planner":
    st.markdown("<h2 style='font-family: Outfit; font-weight: 700; color: #0F172A;'>🔁 Spaced Repetition Revision Planner</h2>", unsafe_allow_html=True)
    st.write("Schedule revision cycles to avoid the forgetting curve, and save schedules to database.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1, 1])
    with col_input:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🗓️ Revision Settings")
        topics_to_revise = st.text_area("Enter topics to revise (comma separated)", placeholder="e.g. Memory Management, Dijkstra's Algorithm, SQL Joins")
        days = st.number_input("Days available before examination/evaluation", min_value=1, max_value=60, value=7)
        
        btn_revision = st.button("Schedule Revision Cycles", type="primary")
        
        if btn_revision:
            if not topics_to_revise:
                st.error("Please enter at least one topic.")
            else:
                topic_list = [t.strip() for t in topics_to_revise.split(",") if t.strip()]
                plan_content = generate_revision_plan(topic_list, days)
                save_revision_plan(st.session_state.user["id"], topics_to_revise, days, plan_content)
                st.success("Revision schedule constructed and saved!")
                st.session_state.active_revision_plan = plan_content
        st.markdown('</div>', unsafe_allow_html=True)
                
    with col_result:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 📅 Smart Revision Schedule")
        
        # Display history of saved plans
        saved_plans = get_revision_plans(st.session_state.user["id"])
        if saved_plans:
            st.markdown("#### 📂 Saved Schedules History")
            selected_plan = st.selectbox(
                "Choose a saved revision plan to view:",
                options=range(len(saved_plans)),
                format_func=lambda i: f"Revision plan ({saved_plans[i]['available_days']} days) - {saved_plans[i]['created_at']}"
            )
            if st.button("Load Selected Plan"):
                st.session_state.active_revision_plan = saved_plans[selected_plan]["plan_content"]
                st.rerun()
                
        if "active_revision_plan" in st.session_state:
            st.markdown("---")
            st.markdown(st.session_state.active_revision_plan)
        else:
            st.info("Specify your revision topics and the timeline to get a spaced schedule, or load a saved one.")
        st.markdown('</div>', unsafe_allow_html=True)


# --- 5. Interview Preparation View ---
elif page == "Interview Preparation":
    st.markdown("<h2 style='font-family: Outfit; font-weight: 700; color: #0F172A;'>💼 Interview Prep Guide</h2>", unsafe_allow_html=True)
    st.write("Configure role-based mock interview preparation material and sample questions.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([1, 1])
    with col_input:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Interview Focus")
        role = st.text_input("Target Job Role", value="Software Engineer")
        topics = st.multiselect(
            "Select Technical Domains",
            ["System Design", "Algorithms & DSA", "Database Internals", "Object Oriented Design", "Behavioral (STAR Method)"],
            default=["Algorithms & DSA", "System Design"]
        )
        difficulty = st.select_slider("Target Difficulty", ["Junior", "Mid-Level", "Senior/Staff"])
        
        btn_prep = st.button("Generate Prep Blueprint", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_result:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🛡️ Preparation Blueprint")
        if btn_prep:
            st.success(f"Blueprint generated for {role} ({difficulty})")
            
            st.markdown("#### 🎯 Focus Domains")
            for t in topics:
                st.markdown(f"- **{t}**")
                
            st.markdown("#### ❓ Sample Mock Interview Questions")
            st.markdown("1. Explain the differences between SQL and NoSQL databases. When would you choose which?")
            st.markdown("2. How would you design a scalable URL shortener service (like Bitly)?")
            st.markdown("3. Implement a function to find the lowest common ancestor in a binary tree.")
            
            st.markdown("#### 💡 Pro Tip")
            st.info("When practicing system design questions, always start by scoping functional and non-functional requirements before proposing the high-level architecture.")
        else:
            st.info("Provide your target job role and interview domains, then click 'Generate Prep Blueprint'.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. AI Study Assistant View ---
elif page == "AI Study Assistant":
    st.markdown("<h2 style='font-family: Outfit; font-weight: 700; color: #0F172A;'>🤖 AI Study Assistant Chat</h2>", unsafe_allow_html=True)
    st.write("Ask StudyPilot AI any questions regarding DSA, System Design, OS, or revision techniques.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Helper to get response from Gemini Agent or rule-based fallback
    def get_ai_assistant_response(query: str) -> str:
        try:
            response = root_agent.run(query)
            if hasattr(response, "text"):
                return response.text
            return str(response)
        except Exception:
            # Resilient fallback answers
            query_lower = query.lower()
            if "dsa" in query_lower or "data structure" in query_lower or "algorithm" in query_lower:
                return "Start by mastering Arrays and Hashing, then move to Trees, BSTs, Graphs, and Dynamic Programming. Practicing actively and explaining space-time complexity analysis is key to cracking technical interviews!"
            elif "system design" in query_lower:
                return "For System Design prep, key concepts include: scalability, load balancers, caching (Redis/Memcached), CDNs, SQL vs NoSQL, database partitioning, and asynchronous processing using Kafka or RabbitMQ."
            elif "revision" in query_lower or "study" in query_lower or "learn" in query_lower:
                return "I recommend Spaced Repetition (revising at 1, 3, and 7-day intervals) and the Feynman Technique (explaining concepts in simple terms to verify your understanding)."
            else:
                return "Interesting question! As your StudyPilot AI companion, I recommend structuring your daily planner, generating roadmaps, and tracking your revision sessions to stay organized."

    # Load and display chat history
    chat_history = get_chat_history(st.session_state.user["id"])
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    chat_container = st.container(border=False, height=420)
    with chat_container:
        if not chat_history:
            st.chat_message("assistant").write("Hello! I am StudyPilot AI. How can I assist you with your studies today? You can ask me to explain algorithms, suggest revisions, or conduct a quick quiz!")
        else:
            for msg in chat_history:
                st.chat_message(msg["sender"]).write(msg["message"])
                
    user_query = st.chat_input("Ask a question...")
    if user_query:
        # Save user message to database
        save_chat_message(st.session_state.user["id"], "user", user_query)
        # Get AI response
        with st.spinner("Thinking..."):
            reply = get_ai_assistant_response(user_query)
        # Save assistant response to database
        save_chat_message(st.session_state.user["id"], "assistant", reply)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# --- 7. Daily Tasks View ---
elif page == "Daily Tasks":
    st.subheader("📝 Daily Tasks Checklist")
    st.write("Manage your tasks dynamically to stay organized.")
    
    today_date = datetime.date.today().isoformat()
    col_t_input, col_t_list = st.columns([1, 2])
    with col_t_input:
        st.markdown("### ➕ Add New Task")
        new_task = st.text_input("Task Description", placeholder="e.g. Revise Computer Networks chapter 1")
        if st.button("Add Task", type="primary") and new_task:
            add_task(st.session_state.user["id"], new_task, today_date)
            st.toast("Task added successfully!")
            st.rerun()
            
    with col_t_list:
        st.markdown("### 📋 Active Tasks")
        current_tasks = get_tasks(st.session_state.user["id"], today_date)
        if not current_tasks:
            st.info("All caught up! Add a new task on the left.")
        else:
            for task in current_tasks:
                checked = st.checkbox(task["text"], value=bool(task["done"]), key=f"dt_task_{task['id']}")
                if checked != bool(task["done"]):
                    update_task_status(task["id"], 1 if checked else 0)
                    streak_increased = check_and_update_streak_on_task_completion(st.session_state.user["id"])
                    if streak_increased:
                        st.toast("🔥 Awesome! All tasks completed today, streak increased!")
                    st.rerun()
            
            if st.button("Clear Completed Tasks"):
                for task in current_tasks:
                    if task["done"]:
                        delete_task(task["id"])
                st.toast("Cleared completed tasks!")
                st.rerun()


# --- 8. Streak Tracker View ---
elif page == "Streak Tracker":
    st.subheader("🔥 Streak Tracker")
    st.write("Study every day to build a habit and maintain your study streak!")
    
    col_streak_stats, col_streak_action = st.columns(2)
    with col_streak_stats:
        st.markdown(f"""
        <div style="background-color: #FEF2F2; padding: 30px; border-radius: 16px; text-align: center; border: 2px solid #FCA5A5;">
            <h3 style="color: #991B1B; margin: 0;">Your Streak</h3>
            <h1 style="font-size: 5rem; color: #DC2626; margin: 10px 0;">🔥 {st.session_state.streak}</h1>
            <p style="color: #7F1D1D; font-weight: 600; margin: 0;">Days in a Row!</p>
            <p style="color: #7F1D1D; font-size: 0.95rem; margin-top: 5px;">Freezes Available / Used: {st.session_state.user.get("freeze_count", 0)}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_streak_action:
        st.markdown("### 📅 Daily Check-In")
        st.write("Complete all tasks for today to automatically check-in, or use the manual check-in button below.")
        
        if st.session_state.checked_in_today:
            st.success("🎉 You are all checked in for today! See you tomorrow!")
        else:
            if st.button("Check-In for Today 🚀", type="primary"):
                today_str = datetime.date.today().isoformat()
                new_streak = st.session_state.streak + 1
                update_streak_state(
                    st.session_state.user["id"], 
                    new_streak, 
                    st.session_state.user.get("freeze_count", 0), 
                    today_str
                )
                st.toast("Streak checked in successfully!")
                st.rerun()

# --- 9. Analytics View ---
elif page == "Analytics":
    st.subheader("📊 Study Analytics")
    st.write("Visualize your study performance and subject distribution based on real logged sessions.")
    
    col_log, col_charts = st.columns([1, 2])
    
    with col_log:
        st.markdown("### ⏱️ Log Study Session")
        with st.form("log_session_form", clear_on_submit=True):
            log_subject = st.selectbox("Subject:", ["DSA", "OS", "DBMS", "System Design", "Computer Networks", "General Aptitude"])
            log_duration = st.number_input("Duration (minutes):", min_value=5, max_value=480, value=60, step=5)
            log_date = st.date_input("Session Date:", datetime.date.today())
            submit_log = st.form_submit_button("Log Session")
            
            if submit_log:
                add_study_session(
                    st.session_state.user["id"],
                    int(log_duration),
                    log_subject,
                    log_date.isoformat()
                )
                st.success(f"Logged {log_duration} mins of {log_subject}!")
                st.rerun()
                
    with col_charts:
        st.markdown("### 📈 Visualizations")
        sessions = get_study_sessions(st.session_state.user["id"])
        
        if not sessions:
            st.info("No study sessions recorded yet.")
        else:
            df = pd.DataFrame(sessions)
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown("#### Study Hours per Day")
                # Group by date
                df['Hours'] = df['duration_minutes'] / 60.0
                daily_hours = df.groupby('study_date')['Hours'].sum().reset_index()
                daily_hours = daily_hours.sort_values('study_date').tail(7)
                daily_hours.set_index('study_date', inplace=True)
                st.bar_chart(daily_hours)
                
            with col_c2:
                st.markdown("#### Subject Time Distribution (minutes)")
                subject_dist = df.groupby('subject')['duration_minutes'].sum().reset_index()
                subject_dist.set_index('subject', inplace=True)
                st.bar_chart(subject_dist)


