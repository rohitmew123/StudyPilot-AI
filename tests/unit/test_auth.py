import os
import pytest
import app.database as db
from app.auth import register_user, authenticate_user, hash_password, verify_password

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    """Fixture to redirect the database to a temporary location for each test."""
    original_db_path = db.DB_PATH
    db.DB_PATH = str(tmp_path / "test_studypilot.db")
    db.init_db()
    yield
    db.DB_PATH = original_db_path

def test_password_hashing():
    password = "SuperSecretPassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_user_registration_success():
    res = register_user("testuser", "test@example.com", "password123")
    assert res["success"] is True
    assert "user_id" in res
    
    # Retrieve user and verify details
    user = db.get_user_by_username("testuser")
    assert user is not None
    assert user["email"] == "test@example.com"
    assert user["streak"] == 0
    assert user["freeze_count"] == 0

def test_user_registration_validation():
    # Empty username
    res = register_user("", "test@example.com", "password123")
    assert res["success"] is False
    assert "Username cannot be empty" in res["message"]

    # Short username
    res = register_user("ab", "test@example.com", "password123")
    assert res["success"] is False
    assert "at least 3 characters" in res["message"]

    # Invalid email
    res = register_user("testuser", "invalid_email", "password123")
    assert res["success"] is False
    assert "Invalid email address format" in res["message"]

    # Short password
    res = register_user("testuser", "test@example.com", "123")
    assert res["success"] is False
    assert "at least 6 characters" in res["message"]

def test_duplicate_registration():
    register_user("testuser", "test@example.com", "password123")
    
    # Duplicate username
    res = register_user("testuser", "other@example.com", "password123")
    assert res["success"] is False
    assert "Username is already taken" in res["message"]

    # Duplicate email
    res = register_user("otheruser", "test@example.com", "password123")
    assert res["success"] is False
    assert "Email is already registered" in res["message"]

def test_authentication():
    register_user("testuser", "test@example.com", "password123")

    # Auth via username
    user = authenticate_user("testuser", "password123")
    assert user is not None
    assert user["username"] == "testuser"

    # Auth via email
    user = authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user["username"] == "testuser"

    # Auth with invalid password
    user = authenticate_user("testuser", "wrong_password")
    assert user is None

    # Auth with non-existent user
    user = authenticate_user("nonexistent", "password123")
    assert user is None

def test_streak_update():
    res = register_user("testuser", "test@example.com", "password123")
    user_id = res["user_id"]

    db.update_streak(user_id, 10)
    user = db.get_user_by_id(user_id)
    assert user["streak"] == 10

def test_tasks_crud():
    res = register_user("taskuser", "task@example.com", "password123")
    user_id = res["user_id"]
    date_str = "2026-07-05"

    # Create
    task_id = db.add_task(user_id, "Solve BFS", date_str)
    tasks = db.get_tasks(user_id, date_str)
    assert len(tasks) == 1
    assert tasks[0]["text"] == "Solve BFS"
    assert tasks[0]["done"] == 0

    # Update completion
    db.update_task_status(task_id, 1)
    tasks = db.get_tasks(user_id, date_str)
    assert tasks[0]["done"] == 1

    # Edit
    db.edit_task(task_id, "Solve DFS instead")
    tasks = db.get_tasks(user_id, date_str)
    assert tasks[0]["text"] == "Solve DFS instead"

    # Delete
    db.delete_task(task_id)
    tasks = db.get_tasks(user_id, date_str)
    assert len(tasks) == 0

def test_streak_evaluation():
    import datetime
    res = register_user("streakuser", "streak@example.com", "password123")
    user_id = res["user_id"]
    
    # Newly registered user: last_activity_date gets initialized to yesterday
    user = db.get_user_by_id(user_id)
    assert user["last_activity_date"] is not None
    
    # 1. Check-In today
    today_str = datetime.date.today().isoformat()
    db.add_task(user_id, "Task 1", today_str, done=1)
    
    from app.auth import check_and_update_streak_on_task_completion, evaluate_streak_on_login
    success = check_and_update_streak_on_task_completion(user_id)
    assert success is True
    
    user = db.get_user_by_id(user_id)
    assert user["streak"] == 1
    assert user["last_activity_date"] == today_str

    # 2. Login next day (yesterday last checked in). Delta == 1. Streak stays 1.
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # Simulate login on tomorrow by manually setting date and evaluating
    # Let's say user has streak=1, freeze=0, last_activity=today.
    # On login tomorrow (delta=1), streak remains 1, freeze remains 0.
    # To mock this, we temporarily override date check or test logic.
    # For now, we can verify that evaluate_streak_on_login doesn't reset streak if delta <= 1.
    user = evaluate_streak_on_login(user_id)
    assert user["streak"] == 1

def test_roadmaps_revision_chat_sessions():
    res = register_user("featuresuser", "features@example.com", "password123")
    user_id = res["user_id"]

    # Revision
    db.save_revision_plan(user_id, "OS", 5, "Content of revision")
    plans = db.get_revision_plans(user_id)
    assert len(plans) == 1
    assert plans[0]["topics"] == "OS"

    # Chat
    db.save_chat_message(user_id, "user", "Hello assistant")
    db.save_chat_message(user_id, "assistant", "Hello user")
    chat = db.get_chat_history(user_id)
    assert len(chat) == 2
    assert chat[0]["sender"] == "user"

    # Sessions
    db.add_study_session(user_id, 120, "DSA", "2026-07-05")
    sessions = db.get_study_sessions(user_id)
    assert len(sessions) == 1
    assert sessions[0]["duration_minutes"] == 120

