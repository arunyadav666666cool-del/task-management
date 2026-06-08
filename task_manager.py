import sqlite3          
import tkinter as tk    
from tkinter import ttk, messagebox, font
from datetime import datetime

class Database:
    """
    Think of this class as your filing cabinet.
    It knows how to open/close the database
    and how to store and retrieve tasks.
    """

    def __init__(self, db_name="tasks.db"):
        """Connect to database when app starts."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the tasks table if it doesn't exist yet."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                description TEXT,
                priority    TEXT    DEFAULT 'Medium',
                status      TEXT    DEFAULT 'Pending',
                created_at  TEXT
            )
        """)
        self.connection.commit()

    def add_task(self, title, description, priority):
        """Save a new task to the database."""
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute("""
            INSERT INTO tasks (title, description, priority, status, created_at)
            VALUES (?, ?, ?, 'Pending', ?)
        """, (title, description, priority, created_at))
        self.connection.commit()

    def get_all_tasks(self):
        """Load all tasks from the database."""
        self.cursor.execute("""
            SELECT id, title, description, priority, status, created_at
            FROM tasks
            ORDER BY
                CASE priority
                    WHEN 'High'   THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low'    THEN 3
                END,
                created_at DESC
        """)
        return self.cursor.fetchall()

    def mark_complete(self, task_id):
        """Change task status to Done."""
        self.cursor.execute("""
            UPDATE tasks SET status = 'Done'
            WHERE id = ?
        """, (task_id,))
        self.connection.commit()

    def delete_task(self, task_id):
        """Remove a task from the database."""
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.connection.commit()

    def get_stats(self):
        """Count tasks by status."""
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Done'")
        done = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
        pending = self.cursor.fetchone()[0]

        return total, done, pending

    def close(self):
        """Close the database connection cleanly."""
        self.connection.close()


class TaskManagerApp:
    """
    This is the main window of the application.
    It uses Tkinter to draw buttons, text boxes, and lists.
    """

    # ── Color Palette ──────────────────────
    BG          = "#0f0f13"      # Dark background
    SURFACE     = "#1a1a24"      # Card/panel background
    SURFACE2    = "#22222f"      # Slightly lighter surface
    ACCENT      = "#7c6af7"      # Purple accent
    ACCENT2     = "#a78bfa"      # Light purple
    SUCCESS     = "#22c55e"      # Green for done
    WARNING     = "#f59e0b"      # Orange for medium
    DANGER      = "#ef4444"      # Red for high priority
    TEXT        = "#e2e8f0"      # Main text
    TEXT_MUTED  = "#64748b"      # Dimmed text
    BORDER      = "#2d2d3d"      # Border color

    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.selected_task_id = None

        self.setup_window()
        self.build_ui()
        self.load_tasks()

    # ── Window Setup ───────────────────────
    def setup_window(self):
        """Configure the main window."""
        self.root.title("✓ TaskFlow — Task Manager")
        self.root.geometry("1000x700")
        self.root.minsize(800, 550)
        self.root.configure(bg=self.BG)

        # Center on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1000) // 2
        y = (self.root.winfo_screenheight() - 700)  // 2
        self.root.geometry(f"1000x700+{x}+{y}")

    # ── Build the UI ───────────────────────
    def build_ui(self):
        """Construct all UI sections."""
        self.build_header()
        self.build_stats_bar()
        self.build_main_area()

    def build_header(self):
        """Top bar with app name."""
        header = tk.Frame(self.root, bg=self.SURFACE, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="  ✓ TaskFlow",
            font=("Courier New", 20, "bold"),
            bg=self.SURFACE,
            fg=self.ACCENT2,
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header,
            text="Powered by Python + SQLite",
            font=("Courier New", 9),
            bg=self.SURFACE,
            fg=self.TEXT_MUTED,
        ).pack(side="right", padx=20)

    def build_stats_bar(self):
        """Show quick stats below the header."""
        self.stats_frame = tk.Frame(self.root, bg=self.BG, pady=10)
        self.stats_frame.pack(fill="x", padx=20)

        self.stat_total   = self._stat_box(self.stats_frame, "Total",   "0", self.ACCENT2)
        self.stat_pending = self._stat_box(self.stats_frame, "Pending", "0", self.WARNING)
        self.stat_done    = self._stat_box(self.stats_frame, "Done",    "0", self.SUCCESS)

    def _stat_box(self, parent, label, value, color):
        """Helper: create one stat box."""
        frame = tk.Frame(parent, bg=self.SURFACE, padx=20, pady=8)
        frame.pack(side="left", padx=(0, 10))

        num_lbl = tk.Label(frame, text=value, font=("Courier New", 22, "bold"),
                           bg=self.SURFACE, fg=color)
        num_lbl.pack()

        tk.Label(frame, text=label, font=("Courier New", 9),
                 bg=self.SURFACE, fg=self.TEXT_MUTED).pack()

        return num_lbl  # Return so we can update it later

    def build_main_area(self):
        """Two-column layout: task list + form."""
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.build_task_list(main)
        self.build_form(main)

    # ── Left: Task List ────────────────────
    def build_task_list(self, parent):
        """The scrollable list of tasks."""
        left = tk.Frame(parent, bg=self.BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Header row for the list
        list_header = tk.Frame(left, bg=self.BG)
        list_header.pack(fill="x", pady=(0, 8))

        tk.Label(list_header, text="YOUR TASKS",
                 font=("Courier New", 11, "bold"),
                 bg=self.BG, fg=self.TEXT).pack(side="left")

        # Treeview (table-style list)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
            background=self.SURFACE,
            foreground=self.TEXT,
            fieldbackground=self.SURFACE,
            rowheight=36,
            borderwidth=0,
        )
        style.configure("Custom.Treeview.Heading",
            background=self.SURFACE2,
            foreground=self.ACCENT2,
            font=("Courier New", 9, "bold"),
            borderwidth=0,
        )
        style.map("Custom.Treeview",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "white")],
        )

        columns = ("title", "priority", "status", "date")
        self.tree = ttk.Treeview(left, columns=columns,
                                 show="headings", style="Custom.Treeview")

        self.tree.heading("title",    text="Task")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("status",   text="Status")
        self.tree.heading("date",     text="Created")

        self.tree.column("title",    width=240)
        self.tree.column("priority", width=70,  anchor="center")
        self.tree.column("status",   width=80,  anchor="center")
        self.tree.column("date",     width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(left, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # When user clicks a row
        self.tree.bind("<<TreeviewSelect>>", self.on_task_select)

        # Action buttons below the list
        btn_row = tk.Frame(parent.master if False else left.master,
                           bg=self.BG)

        btn_area = tk.Frame(left, bg=self.BG, pady=10)
        btn_area.pack(fill="x")

        self._btn(btn_area, "✓  Mark Done",  self.SUCCESS, self.mark_done).pack(side="left", padx=(0,8))
        self._btn(btn_area, "✕  Delete",     self.DANGER,  self.delete_task).pack(side="left")

    def _btn(self, parent, text, color, command):
        """Helper: styled button."""
        return tk.Button(
            parent, text=text,
            font=("Courier New", 10, "bold"),
            bg=color, fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat", padx=14, pady=7,
            cursor="hand2",
            command=command,
        )

    # ── Right: Add Task Form ───────────────
    def build_form(self, parent):
        """Form to add new tasks."""
        right = tk.Frame(parent, bg=self.SURFACE, padx=20, pady=20, width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="ADD NEW TASK",
                 font=("Courier New", 11, "bold"),
                 bg=self.SURFACE, fg=self.ACCENT2).pack(anchor="w")

        tk.Frame(right, bg=self.ACCENT, height=2).pack(fill="x", pady=(4, 16))

        # Title field
        tk.Label(right, text="Task Title *",
                 font=("Courier New", 9), bg=self.SURFACE,
                 fg=self.TEXT_MUTED).pack(anchor="w")

        self.title_var = tk.StringVar()
        title_entry = tk.Entry(right, textvariable=self.title_var,
                               font=("Courier New", 11),
                               bg=self.SURFACE2, fg=self.TEXT,
                               insertbackground=self.ACCENT2,
                               relief="flat", bd=8)
        title_entry.pack(fill="x", pady=(4, 12))

        # Description field
        tk.Label(right, text="Description",
                 font=("Courier New", 9), bg=self.SURFACE,
                 fg=self.TEXT_MUTED).pack(anchor="w")

        self.desc_text = tk.Text(right, height=4,
                                 font=("Courier New", 10),
                                 bg=self.SURFACE2, fg=self.TEXT,
                                 insertbackground=self.ACCENT2,
                                 relief="flat", bd=8, wrap="word")
        self.desc_text.pack(fill="x", pady=(4, 12))

        # Priority dropdown
        tk.Label(right, text="Priority",
                 font=("Courier New", 9), bg=self.SURFACE,
                 fg=self.TEXT_MUTED).pack(anchor="w")

        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.Combobox(right, textvariable=self.priority_var,
                                     values=["High", "Medium", "Low"],
                                     font=("Courier New", 10),
                                     state="readonly")
        priority_menu.pack(fill="x", pady=(4, 20))

        # Submit button
        tk.Button(
            right,
            text="＋  ADD TASK",
            font=("Courier New", 11, "bold"),
            bg=self.ACCENT, fg="white",
            activebackground=self.ACCENT2,
            activeforeground="white",
            relief="flat", pady=10,
            cursor="hand2",
            command=self.add_task,
        ).pack(fill="x")

        # Tip text
        tk.Label(right,
                 text="\nTip: Click a task in the list\nto select it, then use the\nbuttons below to manage it.",
                 font=("Courier New", 8), bg=self.SURFACE,
                 fg=self.TEXT_MUTED, justify="left").pack(anchor="w", pady=(20, 0))

    # ── Logic: Load tasks into list ────────
    def load_tasks(self):
        """Fetch tasks from DB and show them."""
        # Clear the list first
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get tasks from database
        tasks = self.db.get_all_tasks()

        # Priority color tags
        self.tree.tag_configure("High",    foreground="#ef4444")
        self.tree.tag_configure("Medium",  foreground="#f59e0b")
        self.tree.tag_configure("Low",     foreground="#22c55e")
        self.tree.tag_configure("Done",    foreground=self.TEXT_MUTED)

        for task in tasks:
            task_id, title, desc, priority, status, created_at = task
            tag = "Done" if status == "Done" else priority
            status_icon = "✓ Done" if status == "Done" else "● Pending"
            self.tree.insert("", "end",
                             iid=str(task_id),
                             values=(title, priority, status_icon, created_at),
                             tags=(tag,))

        self.update_stats()

    def update_stats(self):
        """Refresh the stat boxes at the top."""
        total, done, pending = self.db.get_stats()
        self.stat_total.config(text=str(total))
        self.stat_done.config(text=str(done))
        self.stat_pending.config(text=str(pending))

    # ── Logic: Add a task ─────────────────
    def add_task(self):
        """Read the form and save a new task."""
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Oops!", "Please enter a task title.")
            return

        description = self.desc_text.get("1.0", "end").strip()
        priority    = self.priority_var.get()

        # Save to database
        self.db.add_task(title, description, priority)

        # Clear the form
        self.title_var.set("")
        self.desc_text.delete("1.0", "end")
        self.priority_var.set("Medium")

        # Refresh the list
        self.load_tasks()

    # ── Logic: Select a task ──────────────
    def on_task_select(self, event):
        """Remember which task the user clicked."""
        selected = self.tree.selection()
        if selected:
            self.selected_task_id = int(selected[0])

    # ── Logic: Mark done ──────────────────
    def mark_done(self):
        """Mark selected task as completed."""
        if not self.selected_task_id:
            messagebox.showinfo("Hint", "Click a task in the list first!")
            return
        self.db.mark_complete(self.selected_task_id)
        self.selected_task_id = None
        self.load_tasks()

    # ── Logic: Delete task ─────────────────
    def delete_task(self):
        """Delete selected task after confirmation."""
        if not self.selected_task_id:
            messagebox.showinfo("Hint", "Click a task in the list first!")
            return

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?\nThis cannot be undone."
        )
        if confirm:
            self.db.delete_task(self.selected_task_id)
            self.selected_task_id = None
            self.load_tasks()

    def on_close(self):
        """Close database cleanly when window is closed."""
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app  = TaskManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)  
    root.mainloop()
