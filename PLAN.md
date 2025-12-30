# Technical Plan: Phase VI (Production Refactor)

## 1. Engine (`main.py`)
- Remove `CLIHandler`.
- Wrap the script in `if __name__ == "__main__":` with a small demo or keep it pure library.
- Refactor `TodoManager.get_all_tasks()`:
  ```python
  return sorted(self._tasks, key=lambda t: (t.priority.value, t.created_at.timestamp()), reverse=True)
  ```
- Ensure `asdict` is used for saving and explicit constructor for loading.

## 2. Web interface (`app.py`)
- **Initialization:**
  ```python
  if 'manager' not in st.session_state:
      st.session_state.storage = StorageManager()
      st.session_state.manager = TodoManager(st.session_state.storage)
  ```
- **Sidebar:** `st.text_input` (Title), `st.text_area` (Desc), `st.text_input` (Tags), `st.selectbox` (Priority).
- **Listing:** Iterate through filtered tasks and create `st.columns` for card-like feel.
- **Search:** `st.text_input` on the main page for tag filtering.

## 3. Deployment (`requirements.txt`)
- `streamlit`

## Steps
1. Refactor `main.py` -> Pure Logic.
2. Create `app.py` -> Streamlit UI.
3. Create `requirements.txt`.
4. Run verification.

---
*Created by Khizr for Ghulam Sarwar Khan.*
