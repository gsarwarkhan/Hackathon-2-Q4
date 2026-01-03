"""
Evolution of Todo - Final Polish (The Web Interface)
Production Streamlit Application with Secure Auth, Multi-Tenancy, and Admin Features.
Built by Khizr for Ghulam Sarwar Khan for GIAIC Hackathon II.
"""

import streamlit as st
import json
import hashlib
import os
from pathlib import Path
from main import TodoManager, StorageManager, Priority

# --- Constants & Config ---
USER_DB = Path("users.json")
STATS_DB = Path("stats.json")
ADMIN_EMAIL = "admin@evolution.com"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest() # Default admin password

st.set_page_config(
    page_title="Evolution of Todo",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Utils ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def hash_password(password: str) -> str:
    """Consistently hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def update_visitor_count():
    """Increments visitor count in a persistent JSON."""
    if 'visitor_counted' not in st.session_state:
        stats = {}
        if STATS_DB.exists():
            try:
                with open(STATS_DB, "r") as f:
                    stats = json.load(f)
            except: pass
        
        current = stats.get("visitors", 0)
        stats["visitors"] = current + 1
        
        with open(STATS_DB, "w") as f:
            json.dump(stats, f)
        
        st.session_state.visitor_counted = True

def get_stats():
    """Reads stats from disk."""
    if STATS_DB.exists():
        try:
            with open(STATS_DB, "r") as f:
                return json.load(f)
        except: pass
    return {"visitors": 0}

def load_users() -> dict:
    """Loads the user registry from disk."""
    if not USER_DB.exists():
        return {}
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_user(email: str, hashed_pw: str, security_answer: str) -> bool:
    """Registers a new user."""
    users = load_users()
    if email in users:
        return False
    users[email] = {
        "password": hashed_pw,
        "security_answer": security_answer.lower().strip()
    }
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)
    return True

def update_password(email: str, new_hashed_pw: str):
    """Updates password for an existing user."""
    users = load_users()
    if email in users:
        users[email]["password"] = new_hashed_pw
        with open(USER_DB, "w") as f:
            json.dump(users, f, indent=4)
        return True
    return False

# --- Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = None
    st.session_state.is_admin = False

# Load Custom Styles
try:
    load_css("assets/style.css")
except FileNotFoundError:
    pass # Fallback to default if css missing

update_visitor_count()

# --- Auth UI ---
def show_auth_page():
    st.markdown("<h1 style='text-align: center; color: #4f46e5;'>🌳 Evolution of Todo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #6b7280;'>Professional Task Management for High Achievers</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

        with tab1:
            with st.form("login_form"):
                st.subheader("Welcome Back")
                email = st.text_input("Email Address").strip().lower()
                pw = st.text_input("Password", type="password")
                login_btn = st.form_submit_button("Log In")

                if login_btn:
                    if email == ADMIN_EMAIL and hash_password(pw) == ADMIN_PASSWORD_HASH:
                        st.session_state.logged_in = True
                        st.session_state.email = email
                        st.session_state.is_admin = True
                        st.success("Admin Access Granted.")
                        st.rerun()
                    
                    users = load_users()
                    user_data = users.get(email)
                    
                    # Backward compatibility for old simple string format, though we prefer dict now
                    stored_pw = user_data if isinstance(user_data, str) else user_data.get("password") if isinstance(user_data, dict) else None

                    if stored_pw and stored_pw == hash_password(pw):
                        st.session_state.logged_in = True
                        st.session_state.email = email
                        st.session_state.is_admin = False
                        st.success(f"Welcome back!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        with tab2:
            with st.form("register_form"):
                st.subheader("Create Account")
                new_email = st.text_input("Email Address").strip().lower()
                new_pw = st.text_input("Password", type="password")
                confirm_pw = st.text_input("Confirm Password", type="password")
                sec_q = st.text_input("Security Question: What is your favorite color?")
                reg_btn = st.form_submit_button("Sign Up")

                if reg_btn:
                    if not new_email or not new_pw:
                        st.warning("All fields are required.")
                    elif new_pw != confirm_pw:
                        st.error("Passwords do not match.")
                    elif not sec_q:
                        st.error("Security answer is required for account recovery.")
                    else:
                        if save_user(new_email, hash_password(new_pw), sec_q):
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Email already registered.")

        with tab3:
            with st.form("recovery_form"):
                st.subheader("Reset Password")
                rec_email = st.text_input("Registered Email").strip().lower()
                rec_ans = st.text_input("Answer: What is your favorite color?", type="password").strip().lower()
                new_rec_pw = st.text_input("New Password", type="password")
                rec_btn = st.form_submit_button("Reset Password")
                
                if rec_btn:
                    users = load_users()
                    user_data = users.get(rec_email)
                    
                    if not user_data or isinstance(user_data, str): # Handle legacy users who don't have security answers
                        st.error("User not found or account strictly legacy (no security setup).")
                    elif user_data.get("security_answer") == rec_ans:
                        update_password(rec_email, hash_password(new_rec_pw))
                        st.success("Password reset! You can now login.")
                    else:
                        st.error("Incorrect security answer.")

# --- Admin View ---
def show_admin_view():
    st.sidebar.title("Admin Panel")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("📊 Admin Dashboard")
    
    users = load_users()
    stats = get_stats()
    
    # Calculate stats
    total_users = len(users)
    total_visitors = stats.get("visitors", 0)
    
    # Count total tasks across all user files
    total_tasks_global = 0
    repo_path = Path(".")
    for file in repo_path.glob("tasks_*.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                total_tasks_global += len(data)
        except: pass

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_visitors}</div><div class="metric-label">Site Visitors</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_users}</div><div class="metric-label">Registered Users</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{total_tasks_global}</div><div class="metric-label">Global Tasks</div></div>""", unsafe_allow_html=True)

    st.markdown("### User Registry")
    st.json(list(users.keys()))

# --- User Dashboard ---
def show_dashboard():
    user_email = st.session_state.email
    
    # Instructions Expander
    with st.expander("📝 User Instructions - How to use"):
        st.markdown("""
        **Welcome to Evolution Todo!**
        1. **Sidebar**: Use the sidebar to 'Seed' (create) new tasks. You can set titles, details, tags, and priority.
        2. **Dashboard**: View your list of tasks. 
           - **Filter**: Use the search bar to find tasks by tag.
           - **Complete**: Check the box to mark a task as done.
           - **Delete**: Remove tasks you no longer need.
        3. **Cleanup**: Use 'Clear Completed Tasks' in the sidebar to remove finished items in bulk.
        4. **Logout**: Securely exit your session from the sidebar.
        """)

    # Initialize manager
    if 'manager' not in st.session_state:
        # Sanitize email to filename
        safe_name = "".join(c for c in user_email if c.isalnum())
        filename = f"tasks_{safe_name}.json"
        storage = StorageManager(filename)
        st.session_state.manager = TodoManager(storage)

    manager = st.session_state.manager

    # --- Sidebar ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/906/906334.png", width=50)
        st.header(f"My Forest")
        st.caption(f"Logged in as: {user_email}")
        
        st.subheader("🌱 Seed New Task")
        with st.form("add_task_form", clear_on_submit=True):
            new_title = st.text_input("Task Title")
            new_desc = st.text_area("Details")
            new_tags = st.text_input("Tags (comma separated)")
            new_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=1)
            submit = st.form_submit_button("Add Task")

            if submit:
                if new_title:
                    tag_list = [t.strip() for t in new_tags.split(",") if t.strip()]
                    p_map = {"Low": Priority.LOW, "Medium": Priority.MEDIUM, "High": Priority.HIGH}
                    manager.add_task(new_title, new_desc, tag_list, p_map[new_priority])
                    st.toast("Task added successfully!", icon="✅")
                    st.rerun()
                else:
                    st.warning("Title is required.")

        st.markdown("---")
        if st.button("🧹 Clear Done"):
            count = manager.clear_completed()
            if count > 0:
                st.toast(f"Cleared {count} tasks.", icon="🧹")
                st.rerun()
            else:
                st.toast("Nothing to clear.", icon="✨")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
            
    # --- Main Area ---
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.title("My Tasks")
    with col_b:
        search = st.text_input("🔍 Filter Tags", placeholder="e.g. work")

    tasks = manager.get_all_tasks(tag_filter=search if search else None)
    
    if not tasks:
        st.info("No tasks found. Start by adding one from the sidebar!")
    
    for task in tasks:
        # Visual Priority Indicator
        p_color = {Priority.HIGH: "#EF4444", Priority.MEDIUM: "#F59E0B", Priority.LOW: "#10B981"}
        border_color = p_color[task.priority]
        
        # Task Container
        with st.container():
            # Custom HTML for task card
            cols = st.columns([0.05, 0.85, 0.1])
            with cols[0]:
                is_checked = st.checkbox("", value=task.is_completed, key=f"chk_{task.id}")
                if is_checked != task.is_completed:
                    manager.toggle_task(task.id)
                    st.rerun()
            
            with cols[1]:
                title_style = "text-decoration: line-through; color: #9CA3AF;" if task.is_completed else "font-weight: 600; color: #1F2937;"
                st.markdown(f"<span style='{title_style} font-size: 1.1rem;'>{task.title}</span>", unsafe_allow_html=True)
                
                meta = []
                if task.priority.name: meta.append(f"<span style='color: {border_color}; font-size: 0.8rem; font-weight: bold;'>{task.priority.name}</span>")
                if task.tags: meta.append(f"<span style='color: #6B7280; font-size: 0.8rem;'>#{' #'.join(task.tags)}</span>")
                
                if meta:
                    st.markdown(" &bull; ".join(meta), unsafe_allow_html=True)
                
                if task.description:
                    st.caption(task.description)

            with cols[2]:
                if st.button("✕", key=f"del_{task.id}", help="Delete Task"):
                    manager.delete_task(task.id)
                    st.rerun()
            
            st.markdown(f"<div style='border-bottom: 1px solid #F3F4F6; margin: 5px 0;'></div>", unsafe_allow_html=True)

# --- Router ---
if st.session_state.logged_in:
    if st.session_state.is_admin:
        show_admin_view()
    else:
        show_dashboard()
else:
    show_auth_page()
