"""
Evolution of Todo - Final Polish (The Web Interface)
Production Streamlit Application with Secure Auth and Multi-Tenancy.
Built by Khizr for Ghulam Sarwar Khan for GIAIC Hackathon II.
"""

import streamlit as st
import json
import hashlib
from pathlib import Path
from main import TodoManager, StorageManager, Priority

# --- Constants & Auth Utils ---
USER_DB = Path("users.json")

def hash_password(password: str) -> str:
    """Consistently hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users() -> dict:
    """Loads the user registry from disk."""
    if not USER_DB.exists():
        return {}
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_user(username: str, hashed_pw: str) -> bool:
    """Registers a new user in the system."""
    users = load_users()
    if username in users:
        return False
    users[username] = hashed_pw
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)
    return True

# --- Page Configuration ---
st.set_page_config(
    page_title="Evolution of Todo",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# --- Authentication UI ---
def show_auth_page():
    st.title("🛡️ Secure Access")
    st.subheader("Login or Register to access your Task Forest")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            user = st.text_input("Username").strip()
            pw = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Access Forest")

            if login_btn:
                users = load_users()
                if user in users and users[user] == hash_password(pw):
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Choose Username").strip()
            new_pw = st.text_input("Choose Password", type="password")
            confirm_pw = st.text_input("Confirm Password", type="password")
            reg_btn = st.form_submit_button("Plant Seeds")

            if reg_btn:
                if not new_user or not new_pw:
                    st.warning("Fields cannot be empty.")
                elif new_pw != confirm_pw:
                    st.error("Passwords do not match.")
                else:
                    if save_user(new_user, hash_password(new_pw)):
                        st.success("Account created! You can now login.")
                    else:
                        st.error("Username already exists.")

# --- Dashboard UI ---
def show_dashboard():
    # Multi-tenant logic: Initialize manager for specific user
    user = st.session_state.username
    if 'manager' not in st.session_state:
        filename = f"tasks_{user.lower()}.json"
        storage = StorageManager(filename)
        st.session_state.manager = TodoManager(storage)

    manager = st.session_state.manager

    # --- Sidebar: Add Tasks & Utils ---
    with st.sidebar:
        st.header(f"🌳 {user}'s Forest")
        st.subheader("Seed New Task")

        with st.form("add_task_form", clear_on_submit=True):
            new_title = st.text_input("Task Title", placeholder="What needs to be done?")
            new_desc = st.text_area("Description (optional)", placeholder="Add more details...")
            new_tags = st.text_input("Tags", placeholder="e.g. Work, Urgent")
            new_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=1)
            submit = st.form_submit_button("Seed Task")

            if submit:
                if new_title:
                    tag_list = [t.strip() for t in new_tags.split(",") if t.strip()]
                    p_map = {"Low": Priority.LOW, "Medium": Priority.MEDIUM, "High": Priority.HIGH}
                    manager.add_task(new_title, new_desc, tag_list, p_map[new_priority])
                    st.success("Task seeded!")
                    st.rerun()
                else:
                    st.warning("Title required.")

        st.markdown("---")
        if st.button("🧹 Clear Completed Tasks"):
            count = manager.clear_completed()
            if count > 0:
                st.toast(f"Cleaned up {count} tasks!")
                st.rerun()
            else:
                st.toast("Forest is already tidy.")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

        st.caption(f"Partner: Khizr | User: {user}")

    # --- Main Dashboard ---
    st.title("🚀 Evolution of Todo")
    st.markdown("High-Perfection Task Management Engine")

    # Search and Filter
    col_a, col_b = st.columns([3, 1])
    with col_a:
        search = st.text_input("🔍 Filter by Tag", placeholder="Search tags...")
    with col_b:
        st.write("")
        st.write(f"Total: **{len(manager.get_all_tasks())}** tasks")

    # List Display
    tasks = manager.get_all_tasks(tag_filter=search if search else None)
    if not tasks:
        st.info("No tasks found. Begin seeding in the sidebar!")
    else:
        for task in tasks:
            p_icons = {Priority.HIGH: "🔴", Priority.MEDIUM: "🟡", Priority.LOW: "🟢"}
            with st.container():
                c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
                with c1:
                    if st.checkbox("", value=task.is_completed, key=f"chk_{task.id}"):
                        if not task.is_completed:
                            manager.toggle_task(task.id)
                            st.rerun()
                    else:
                        if task.is_completed:
                            manager.toggle_task(task.id)
                            st.rerun()

                with c2:
                    strike = "~~" if task.is_completed else ""
                    st.markdown(f"### {p_icons[task.priority]} {strike}{task.title}{strike}")
                    if task.description: st.caption(task.description)
                    if task.tags:
                        st.markdown(" ".join([f"`#{t}`" for t in task.tags]))

                with c3:
                    if st.button("🗑️ Delete", key=f"del_{task.id}"):
                        manager.delete_task(task.id)
                        st.toast("Task removed.")
                        st.rerun()
                st.markdown("---")

    st.caption("Strategic AI Partner: Khizr. Built for the GIAIC Hackathon II.")

# --- Router ---
if st.session_state.logged_in:
    show_dashboard()
else:
    show_auth_page()
