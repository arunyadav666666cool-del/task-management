# ✅ TaskFlow — Python Task Manager

A clean, fully functional **desktop Task Manager** built with pure Python.  
No external libraries needed — runs on any machine with Python 3.8+.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite)
![UI](https://img.shields.io/badge/UI-Tkinter-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Preview

```
╔══════════════════════════════════════════════════╗
║  ✓ TaskFlow                    Python + SQLite   ║
╠══════════════════════════════════════════════════╣
║  Total: 5    Pending: 3    Done: 2               ║
╠══════════════════╦═══════════════════════════════╣
║  Task List       ║  ADD NEW TASK                 ║
║  ─────────────── ║  ─────────────────────────── ║
║  Buy groceries   ║  Task Title *                 ║
║  Call doctor ✓   ║  [____________________]       ║
║  Study Python    ║                               ║
║                  ║  Description                  ║
║  [✓ Mark Done]   ║  [____________________]       ║
║  [✕ Delete  ]    ║                               ║
║                  ║  Priority: [Medium ▼]         ║
║                  ║  [  + ADD TASK  ]             ║
╚══════════════════╩═══════════════════════════════╝
```

---

## ✨ Features

- **Add tasks** with a title, description, and priority level (High / Medium / Low)
- **Mark tasks as Done** with a single click
- **Delete tasks** with a confirmation dialog
- **Live stats bar** — shows Total, Pending, and Done counts
- **Persistent storage** — tasks are saved to a local `tasks.db` file
- **Sorted by priority** — High priority tasks always appear first
- **Timestamps** — every task is stamped with the date and time it was created
- Zero external dependencies — uses only Python's standard library

---

## 🛠️ Tech Stack

| Tool | Purpose | Why we used it |
|------|---------|---------------|
| `Python 3.8+` | Core language | Simple, beginner-friendly |
| `tkinter` | Desktop UI / window | Built into Python, no install needed |
| `sqlite3` | Database | File-based, no server required |
| `datetime` | Timestamps | Built into Python |
| `ttk` | Styled widgets | Cleaner UI components |

---

## 📁 Project Structure

```
task-manager/
│
├── task_manager.py     ← Main application (all code in one file)
└── tasks.db            ← Auto-created on first run (your data lives here)
```

> `tasks.db` is created automatically the first time you run the app.  
> You can open it with [DB Browser for SQLite](https://sqlitebrowser.org/) to inspect your data.

---

## 🚀 Getting Started

### Prerequisites

Make sure Python is installed on your computer:

```bash
python --version
# or
python3 --version
```

You should see something like `Python 3.11.0`.  
If not, download it from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation

**Step 1 — Clone the repository**

```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
```

**Step 2 — Run the app**

```bash
python task_manager.py
```

That's it! No `pip install` needed. The window will open immediately.

> On some systems, use `python3` instead of `python`

---

## 🖥️ How to Use

| Action | Steps |
|--------|-------|
| Add a task | Fill in the title → choose priority → click **+ ADD TASK** |
| Complete a task | Click on a task in the list → click **✓ Mark Done** |
| Delete a task | Click on a task in the list → click **✕ Delete** → confirm |

---

## 🗄️ Database Schema

The app creates a SQLite database (`tasks.db`) with one table:

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    priority    TEXT    DEFAULT 'Medium',   -- 'High', 'Medium', 'Low'
    status      TEXT    DEFAULT 'Pending',  -- 'Pending', 'Done'
    created_at  TEXT                        -- e.g. '2024-06-08 14:30'
);
```

---

## 🏗️ Code Architecture

The code follows a simple **2-layer architecture**:

```
┌─────────────────────────────┐
│      TaskManagerApp         │  ← UI Layer (Tkinter)
│  Draws window, handles      │    Handles all user interactions
│  button clicks              │
└────────────┬────────────────┘
             │ calls
┌────────────▼────────────────┐
│        Database             │  ← Data Layer (SQLite)
│  Saves, loads, updates,     │    All SQL operations live here
│  deletes tasks              │
└────────────┬────────────────┘
             │ reads/writes
┌────────────▼────────────────┐
│         tasks.db            │  ← Storage (file on disk)
└─────────────────────────────┘
```

**Why this structure?**  
The UI layer doesn't know how data is stored. The database layer doesn't know what the window looks like. They are separated on purpose — this is called **separation of concerns** and makes the code easier to maintain.

---

## 🐛 Troubleshooting

**Error: `No module named tkinter`**

```bash
# Ubuntu / Linux
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows
# Reinstall Python and check "tcl/tk and IDLE" during setup
```

**Error: `python not recognized`**

```bash
# Try this instead:
python3 task_manager.py
```

**Nothing happens when I double-click the file**

Run it from the terminal to see the error message:

```bash
python task_manager.py
```

---

## 🔮 Future Improvements

- [ ] Add due date / deadline field
- [ ] Search and filter tasks by keyword or priority
- [ ] Edit existing tasks
- [ ] Export tasks to CSV
- [ ] Add task categories / tags
- [ ] Light / dark theme toggle
- [ ] Migrate to a web UI using Flask + PostgreSQL

---

## 📚 What I Learned

Building this project helped me understand:

- How to use **SQLite** with Python for persistent local storage
- How to build a **desktop GUI** with Tkinter and ttk
- The concept of **classes and OOP** — separating concerns into Database and UI classes
- How **SQL queries** (INSERT, SELECT, UPDATE, DELETE) work in practice
- How `if __name__ == "__main__"` works as the entry point of a Python program

---





