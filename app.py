"""
Evolution of Todo - Phase VI (The Web Interface)
Production Streamlit Application.
Built by Khizr for Ghulam Sarwar Khan for GIAIC Hackathon II.
"""

import streamlit as st
from main import TodoManager, StorageManager, Priority
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Evolution of Todo",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .task-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        background-color: white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .priority-high { border-left-color: #ff4b4b; }
    .priority-medium { border-left-color: #ffa500; }
    .priority-low { border-left-color: #28a745; }
    </style>
    """, unsafe_allow_index=True)

# --- Initalization ---
if 'manager' not in st.session_state:
    storage = StorageManager()
    st.session_state.manager = TodoManager(storage)

manager = st.session_state.manager

# --- Sidebar: Add Tasks ---
with st.sidebar:
    st.header("🌳 Bonsai Tasks")
    st.subheader("Add New Task")

    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task Title", placeholder="What needs to be done?")
        new_desc = st.text_area("Description (optional)", placeholder="Add more details...")
        new_tags = st.text_input("Tags", placeholder="e.g. Work, Urgent")
        new_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=1)

        submit = st.form_submit_button("Seed Task")

        if submit:
            if new_title:
                tag_list = [t.strip() for t in new_tags.split(",") if t.strip()]
                p_mapping = {"Low": Priority.LOW, "Medium": Priority.MEDIUM, "High": Priority.HIGH}

                try:
                    manager.add_task(
                        title=new_title,
                        description=new_desc,
                        tags=tag_list,
                        priority=p_mapping[new_priority]
                    )
                    st.success("Task seeded successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Title is mandatory.")

    st.markdown("---")
    st.caption(f"Partner: Khizr | User: Ghulam Sarwar Khan")

# --- Main Dashboard ---
st.title("🚀 Evolution of Todo")
st.markdown("Professional Management for GIAIC Hackathon II")

# Search and Filter Bar
col_a, col_b = st.columns([3, 1])
with col_a:
    search_query = st.text_input("🔍 Search by Tag", placeholder="Type a tag name...")
with col_b:
    st.write("") # Padding
    st.write(f"Total Tasks: **{len(manager.get_all_tasks())}**")

# Task Listing
tasks = manager.get_all_tasks(tag_filter=search_query if search_query else None)

if not tasks:
    st.info("Your task forest is empty or no matches found. Start seeding tasks from the sidebar!")
else:
    for task in tasks:
        # Priority Logic
        p_icons = {Priority.HIGH: "🔴", Priority.MEDIUM: "🟡", Priority.LOW: "🟢"}
        p_styles = {Priority.HIGH: "high", Priority.MEDIUM: "medium", Priority.LOW: "low"}

        # CSS Card Container
        with st.container():
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])

            with col1:
                # Toggle Checkbox
                checked = st.checkbox("", value=task.is_completed, key=f"check_{task.id}")
                if checked != task.is_completed:
                    manager.toggle_task(task.id)
                    st.toast(f"Task '{task.title}' updated!")
                    st.rerun()

            with col2:
                # Title and Metatdata
                title_style = "~~" if task.is_completed else ""
                st.markdown(f"### {p_icons[task.priority]} {title_style}{task.title}{title_style}")

                if task.description:
                    st.caption(task.description)

                # Tags
                if task.tags:
                    tags_html = " ".join([f"`#{tag}`" for tag in task.tags])
                    st.markdown(tags_html)

            with col3:
                # Delete Button
                if st.button("🗑️ Delete", key=f"del_{task.id}"):
                    manager.delete_task(task.id)
                    st.toast("Task removed from forest.")
                    st.rerun()

            st.markdown("---")

st.caption("Strategic AI Partner: Khizr. Built for Perfection.")

