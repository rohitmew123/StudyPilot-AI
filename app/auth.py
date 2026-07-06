import re
import bcrypt
import sqlite3
from typing import Dict, Any, Optional
from app.database import create_user, get_user_by_username, get_user_by_email

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def validate_email(email: str) -> bool:
    """Basic regex validation for emails."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))

def register_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Validate, hash password, and register a new user.
    Returns a dict with 'success' (bool) and 'message' (str).
    """
    username = username.strip()
    email = email.strip()
    
    if not username:
        return {"success": False, "message": "Username cannot be empty."}
    if len(username) < 3:
        return {"success": False, "message": "Username must be at least 3 characters."}
    if not email:
        return {"success": False, "message": "Email cannot be empty."}
    if not validate_email(email):
        return {"success": False, "message": "Invalid email address format."}
    if not password or len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    # Check if username exists
    if get_user_by_username(username):
        return {"success": False, "message": "Username is already taken."}

    # Check if email exists
    if get_user_by_email(email):
        return {"success": False, "message": "Email is already registered."}

    password_hash = hash_password(password)

    try:
        user_id = create_user(username, email, password_hash)
        return {
            "success": True, 
            "message": "Registration successful!", 
            "user_id": user_id
        }
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": f"Database integrity error: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Registration failed: {str(e)}"}

def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user by username or email and password.
    Returns the user dict if successful, None otherwise.
    """
    val = username_or_email.strip()
    if not val or not password:
        return None

    # Check if email format or username
    user = None
    if "@" in val:
        user = get_user_by_email(val)
    
    if not user:
        user = get_user_by_username(val)

    if user and verify_password(password, user["password_hash"]):
        # Run daily streak check upon successful login
        user = evaluate_streak_on_login(user["id"])
        return user

    return None

def evaluate_streak_on_login(user_id: int) -> Dict[str, Any]:
    """
    Evaluate user streak upon login.
    last_activity_date is defined as the date of the last completed check-in or daily task completion.
    - If last_activity_date was yesterday: they are on track. Streak is maintained.
    - If last_activity_date was 2 days ago: they missed 1 day. Freeze count increments.
    - If last_activity_date was 3 or more days ago: they missed 2 consecutive days. Streak resets to 0.
    """
    import datetime
    from app.database import get_user_by_id, update_streak_state
    
    user = get_user_by_id(user_id)
    if not user:
        return {}
        
    today = datetime.date.today()
    last_act_str = user.get("last_activity_date")
    streak = user.get("streak", 0)
    freeze_count = user.get("freeze_count", 0)
    
    if not last_act_str:
        # First time user login. Set last_activity_date to yesterday so they can start a streak today.
        yesterday = today - datetime.timedelta(days=1)
        update_streak_state(user_id, streak, freeze_count, yesterday.isoformat())
        return get_user_by_id(user_id)
        
    try:
        last_date = datetime.date.fromisoformat(last_act_str)
    except ValueError:
        last_date = today - datetime.timedelta(days=1)
        
    delta = (today - last_date).days
    
    if delta <= 1:
        # User checked in today or yesterday. Streak is safe.
        pass
    elif delta == 2:
        # Missed 1 day (last check-in was 2 days ago). Freeze the streak.
        freeze_count += 1
        # Update last_activity_date to yesterday so we don't double-freeze on subsequent logins today.
        yesterday = today - datetime.timedelta(days=1)
        update_streak_state(user_id, streak, freeze_count, yesterday.isoformat())
    elif delta >= 3:
        # Missed 2 or more consecutive days. Reset streak to 0.
        streak = 0
        yesterday = today - datetime.timedelta(days=1)
        update_streak_state(user_id, streak, freeze_count, yesterday.isoformat())
        
    return get_user_by_id(user_id)

def check_and_update_streak_on_task_completion(user_id: int) -> bool:
    """
    Check if all tasks for today are completed.
    If yes, and they haven't checked in today yet, increment the streak,
    set last_activity_date to today, and return True.
    If not all tasks are completed, and they were checked in today, decrement the streak,
    set last_activity_date to yesterday, and return False.
    """
    import datetime
    from app.database import get_user_by_id, get_tasks, update_streak_state
    
    today_str = datetime.date.today().isoformat()
    yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    user = get_user_by_id(user_id)
    if not user:
        return False
        
    tasks = get_tasks(user_id, today_str)
    if not tasks:
        return False
        
    all_done = all(t["done"] for t in tasks)
    last_act = user.get("last_activity_date")
    streak = user.get("streak", 0)
    freeze_count = user.get("freeze_count", 0)
    
    if all_done and last_act != today_str:
        # Increment streak
        update_streak_state(user_id, streak + 1, freeze_count, today_str)
        return True
    elif not all_done and last_act == today_str:
        # Revert streak
        update_streak_state(user_id, max(0, streak - 1), freeze_count, yesterday_str)
        return False
        
    return False



