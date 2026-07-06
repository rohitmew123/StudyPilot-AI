import os
import sqlite3
from typing import Dict, Any, List, Optional

# Database file location (root of the workspace)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "studypilot.db")

def get_db_connection() -> sqlite3.Connection:
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize the database and create the tables if they don't exist."""
    with get_db_connection() as conn:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                freeze_count INTEGER DEFAULT 0,
                last_activity_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check if last_activity_date column is missing from an existing users table
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        if columns and "last_activity_date" not in columns:
            try:
                conn.execute("ALTER TABLE users ADD COLUMN last_activity_date TEXT")
                conn.commit()
            except Exception:
                pass

        # Create tasks table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create dsa_roadmaps table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dsa_roadmaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                roadmap_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create revision_plans table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS revision_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topics TEXT NOT NULL,
                available_days INTEGER NOT NULL,
                plan_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create chat_messages table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create study_sessions table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                duration_minutes INTEGER NOT NULL,
                subject TEXT NOT NULL,
                study_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

def create_user(username: str, email: str, password_hash: str) -> int:
    """Create a new user. Returns the newly created user's ID."""
    import datetime
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, streak, freeze_count, last_activity_date) VALUES (?, ?, ?, 0, 0, ?)",
            (username.strip(), email.strip().lower(), password_hash, yesterday)
        )
        conn.commit()
        return cursor.lastrowid


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve user details by username."""
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE LOWER(username) = LOWER(?)",
            (username.strip(),)
        ).fetchone()
        return dict(row) if row else None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieve user details by email."""
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.strip().lower(),)
        ).fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve user details by ID."""
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        return dict(row) if row else None

def update_streak_state(user_id: int, streak: int, freeze_count: int, last_activity_date: Optional[str]) -> None:
    """Update streak, freeze count, and last activity date for a user."""
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE users SET streak = ?, freeze_count = ?, last_activity_date = ? WHERE id = ?",
            (streak, freeze_count, last_activity_date, user_id)
        )
        conn.commit()

def update_streak(user_id: int, streak: int) -> None:
    """Legacy helper to update only the streak."""
    with get_db_connection() as conn:
        conn.execute("UPDATE users SET streak = ? WHERE id = ?", (streak, user_id))
        conn.commit()

def update_freeze_count(user_id: int, freeze_count: int) -> None:
    """Legacy helper to update only the freeze count."""
    with get_db_connection() as conn:
        conn.execute("UPDATE users SET freeze_count = ? WHERE id = ?", (freeze_count, user_id))
        conn.commit()

# --- Tasks Helpers ---
def get_tasks(user_id: int, date: str) -> List[Dict[str, Any]]:
    """Get all tasks for a specific user and date."""
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND date = ? ORDER BY id ASC",
            (user_id, date)
        ).fetchall()
        return [dict(r) for r in rows]

def add_task(user_id: int, text: str, date: str, done: int = 0) -> int:
    """Add a new task for a user and date."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, text, done, date) VALUES (?, ?, ?, ?)",
            (user_id, text.strip(), done, date)
        )
        conn.commit()
        return cursor.lastrowid

def update_task_status(task_id: int, done: int) -> None:
    """Update task completion status."""
    with get_db_connection() as conn:
        conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (done, task_id))
        conn.commit()

def delete_task(task_id: int) -> None:
    """Delete a task."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def edit_task(task_id: int, text: str) -> None:
    """Edit the text of a task."""
    with get_db_connection() as conn:
        conn.execute("UPDATE tasks SET text = ? WHERE id = ?", (text.strip(), task_id))
        conn.commit()


# --- Revision Plans Helpers ---
def get_revision_plans(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve saved revision plans for a user."""
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM revision_plans WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

def save_revision_plan(user_id: int, topics: str, available_days: int, plan_content: str) -> int:
    """Save a generated revision plan."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO revision_plans (user_id, topics, available_days, plan_content) VALUES (?, ?, ?, ?)",
            (user_id, topics.strip(), available_days, plan_content)
        )
        conn.commit()
        return cursor.lastrowid

# --- Chat Messages Helpers ---
def get_chat_history(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve chat message history for a user."""
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM chat_messages WHERE user_id = ? ORDER BY id ASC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

def save_chat_message(user_id: int, sender: str, message: str) -> int:
    """Save a chat message."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_messages (user_id, sender, message) VALUES (?, ?, ?)",
            (user_id, sender, message)
        )
        conn.commit()
        return cursor.lastrowid

# --- Study Sessions Helpers ---
def get_study_sessions(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve study sessions for a user."""
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM study_sessions WHERE user_id = ? ORDER BY study_date DESC, id DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

def add_study_session(user_id: int, duration_minutes: int, subject: str, study_date: str) -> int:
    """Add a new study session entry."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO study_sessions (user_id, duration_minutes, subject, study_date) VALUES (?, ?, ?, ?)",
            (user_id, duration_minutes, subject, study_date)
        )
        conn.commit()
        return cursor.lastrowid
