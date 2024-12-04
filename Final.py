import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from tkinter import simpledialog
import random
from PIL import Image, ImageTk

class ToDoApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("To-Do List")
        self.root.geometry("950x800")
        self.root.resizable(False, False)
       
        bg_image = Image.open("C:/Users/ASUS/Downloads/icon8.jpg")  
        bg_image = bg_image.resize((950, 800), )
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_image_tk)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.initialize_database()
      
        # Calendar
        self.calendar = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd', font=("Verdana", 11))
        self.calendar.grid(row=1, column=1, padx=10, pady=5, sticky="n")

        # Search Bar (Row 1, Column 1)
        self.search_frame = Frame(root)
        self.search_frame.grid(row=0, column=1, padx=10, pady=(0, 5), sticky="n")

        self.search_entry = Entry(self.search_frame, font=("Verdana", 11), width=30)
        self.search_entry.grid(row=0, column=0, padx=5, pady=0)

        self.search_btn = Button(self.search_frame, text="Search Task", command=self.search_task, bg="lightsteelblue", fg="black", font=("Verdana", 11))
        self.search_btn.grid(row=0, column=1, padx=5, pady=0)

        # Task List Frame (Row 2, Column 1, Below Search Bar)
        self.task_frame = LabelFrame(root, text="Tasks", font=("Verdana", 11), padx=10, pady=10)
        self.task_frame.grid(row=1, column=0, padx=10, pady=5, sticky="n")

        self.task_list = Listbox(self.task_frame, width=40, height=15, font=("Verdana", 11))
        self.task_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.task_scroll = Scrollbar(self.task_frame, command=self.task_list.yview)
        self.task_scroll.pack(side=RIGHT, fill=Y)
        self.task_list.config(yscrollcommand=self.task_scroll.set)
        

        # Task Entry (Row 2, Column 1)
        self.entry = Entry(root, font=("Verdana", 11), width=40)
        self.entry.grid(row=3, column=0, columnspan=2, pady=5, padx=10)

        # Buttons (Row 3, Column 1)
        self.button_frame = Frame(root)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.add_btn = Button(self.button_frame, text="Add Task", command=self.add_task, bg="palegreen", fg="black", font=("Verdana", 11))
        self.add_btn.grid(row=0, column=0, padx=5)

        self.delete_btn = Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="lightcoral", fg="black", font=("Verdana", 11))
        self.delete_btn.grid(row=0, column=1, padx=5)

        self.mark_done_btn = Button(self.button_frame, text="Mark as Done", command=self.mark_done, bg="lightskyblue", fg="black", font=("Verdana", 11))
        self.mark_done_btn.grid(row=0, column=2, padx=5)

        self.view_all_btn = Button(self.button_frame, text="View All Tasks", command=self.view_all_tasks, bg="moccasin", fg="black", font=("Verdana", 11))
        self.view_all_btn.grid(row=0, column=3, padx=5)

        self.update_btn = Button(self.button_frame, text="Update Task", command=self.update_task, bg="plum", fg="black", font=("Verdana", 11))
        self.update_btn.grid(row=0, column=4, padx=5)

        self.delete_all_btn = Button(self.button_frame, text="Delete All Tasks", command=self.delete_all_tasks, bg="rosybrown", fg="black", font=("Verdana", 11))
        self.delete_all_btn.grid(row=0, column=5, padx=5)

        # Recommendations Frame (Row 4, Column 0 and 1)
        self.recommendations_frame = LabelFrame(root, text="Recommendations", font=("Verdana", 11), padx=10, pady=10)
        self.recommendations_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20)
 
        # List of recommended tasks
        self.recommended_tasks = [
            "Read a self-help book",
            "Meditate for 10 minutes",
            "Exercise for 30 minutes",
            "Learn a new skill online",
            "Write in a journal for 10 minutes",
            "Practice gratitude by listing 3 things you're thankful for"
        ]

        # Combobox for recommendations
        self.recommendation_combobox = ttk.Combobox(self.recommendations_frame, values=self.recommended_tasks, width=40, font=("Verdana", 11))
        self.recommendation_combobox.set("Select a recommendation")
        self.recommendation_combobox.pack(pady=10)

        self.add_recommendation_btn = Button(self.recommendations_frame, text="Add to Task Entry", command=self.add_recommendation, bg="cornflowerblue", fg="black", font=("Verdana", 11))
        self.add_recommendation_btn.pack(pady=10)

        self.delete_all_btn = Button(self.button_frame, text="Delete All Tasks", command=self.delete_all_tasks, bg="indianred", fg="black", font=("Verdana", 11))
        self.delete_all_btn.grid(row=0, column=5, padx=10)
        
        self.calendar.bind("<<CalendarSelected>>", self.load_tasks)
    def add_recommendation(self):
        """Add the selected recommendation to the task entry box."""
        selected_task = self.recommendation_combobox.get()
        if selected_task == "Select a recommendation":
            messagebox.showwarning("Selection Error", "Please select a task from the recommendations.")
        else:
            self.entry.delete(0, tk.END)  
            self.entry.insert(0, selected_task)  

    def initialize_database(self):
        """Create SQLite tables for lists and users if they don't exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )""")
        self.conn.commit()

    def add_task(self):
        """Add a task for the selected date."""
        date = self.calendar.get_date()
        task = self.entry.get().strip()

        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty!")
            return

        self.cursor.execute("INSERT INTO lists (user_id, date, task, status) VALUES (?, ?, ?, ?)",
                            (self.user_id, date, task, "pending"))
        self.conn.commit()
        self.entry.delete(0, END)
        self.load_tasks()
    #search function
    def search_task(self):
        """Search for tasks containing the text in the search entry."""
        search_text = self.search_entry.get().strip()
        if not search_text:
            messagebox.showwarning("Input Error", "Search text cannot be empty!")
            return

        self.task_list.delete(0, END)
        self.cursor.execute("SELECT date, task, status FROM lists WHERE user_id = ? AND task LIKE ?", 
                            (self.user_id, f"%{search_text}%"))
        tasks = self.cursor.fetchall()

        if not tasks:
            messagebox.showinfo("No Results", "No tasks found matching your search.")
        else:
            for date, task, status in tasks:
                display_task = f"{date}: {task} (Done)" if status == "done" else f"{date}: {task}"
                self.task_list.insert(END, display_task)
    def delete_task(self):
        """Delete a selected task."""
        try:
            selected_task = self.task_list.get(self.task_list.curselection()).replace(" (Done)", "")
            date = self.calendar.get_date()
            self.cursor.execute("DELETE FROM lists WHERE user_id = ? AND date = ? AND task = ?",
                                (self.user_id, date, selected_task))
            self.conn.commit()
            self.load_tasks()
        except TclError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
    def delete_all_tasks(self):
        """Delete all tasks for the selected date."""
        date = self.calendar.get_date()
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete all tasks for {date}?")
        
        if confirmation:
            self.cursor.execute("DELETE FROM lists WHERE user_id = ? AND date = ?", (self.user_id, date))
            self.conn.commit()
            self.load_tasks()  
            messagebox.showinfo("Success", "All tasks have been deleted.")

        

    def mark_done(self):
        """Mark a task as done and show motivation pop-up."""
        try:
            selected_task = self.task_list.get(self.task_list.curselection()).replace(" (Done)", "")
            date = self.calendar.get_date()

            self.cursor.execute("UPDATE lists SET status = ? WHERE user_id = ? AND date = ? AND task = ?",
                                ("done", self.user_id, date, selected_task))
            self.conn.commit()

            self.show_motivation_popup()
     
            self.load_tasks()

        except TclError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")
    def show_motivation_popup(self):
        """Show a pop-up with motivational message."""
        
        date = self.calendar.get_date()
        self.cursor.execute("SELECT COUNT(*) FROM lists WHERE user_id = ? AND status = 'done' AND date = ?", 
                            (self.user_id, date))
        completed_count = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM lists WHERE user_id = ? AND date = ?", 
                            (self.user_id, date))
        total_count = self.cursor.fetchone()[0]
        
        motivation_quotes = [
            "Keep going, you're doing great!",
            "Success is the sum of small efforts, repeated day in and day out.",
            "Don't watch the clock; do what it does. Keep going!",
            "The secret to getting ahead is getting started.",
            "Believe in yourself, you are capable of amazing things!"
        ]
        
        quote = random.choice(motivation_quotes)
        
        # Create pop-up window
        popup = Toplevel(self.root)
        popup.title("Motivational Quote")
        popup.geometry("600x300")
        
        label = Label(popup, text=f"Tasks completed: {completed_count}/{total_count}\n\n{quote}", 
                    font=("Verdana", 10), justify="center")
        label.pack(pady=20)
        
        close_button = Button(popup, text="Close", command=popup.destroy, bg="red", fg="white", font=("Verdana", 10))
        close_button.pack(pady=10)
      
        popup.after(5000, popup.destroy)  
    def load_tasks(self, event=None):
        """Load tasks for the selected date."""
        date = self.calendar.get_date()
        self.task_list.delete(0, END)

        self.cursor.execute("SELECT task, status FROM lists WHERE user_id = ? AND date = ?", (self.user_id, date))
        tasks = self.cursor.fetchall()

        for task, status in tasks:
            display_task = f"{task} (Done)" if status == "done" else task
            self.task_list.insert(END, display_task)

    def view_all_tasks(self):
        """View all tasks across the calendar."""
        self.task_list.delete(0, END)
        self.cursor.execute("SELECT date, task, status FROM lists WHERE user_id = ? ORDER BY date", (self.user_id,))
        tasks = self.cursor.fetchall()

        for date, task, status in tasks:
            display_task = f"{date}: {task} (Done)" if status == "done" else f"{date}: {task}"
            self.task_list.insert(END, display_task)
    def show_motivation_popup(self):
        """Display motivational quote and task progress."""
        quotes = [
            "Keep going! You're doing great!",
            "Believe in yourself! Every task is a step towards success!",
            "You're on the right track, keep it up!",
            "Success is the sum of small efforts, repeated day in and day out."
        ]
        
        quote = random.choice(quotes)

        done_tasks = self.cursor.execute("SELECT COUNT(*) FROM lists WHERE user_id = ? AND status = 'done'", (self.user_id,)).fetchone()[0]
        total_tasks = self.cursor.execute("SELECT COUNT(*) FROM lists WHERE user_id = ?", (self.user_id,)).fetchone()[0]

        # Create the pop-up
        popup = Toplevel(self.root)
        popup.title("Motivational Report")
        popup.geometry("400x200")
        
        message = f"You've completed {done_tasks} out of {total_tasks} lists.\n\n{quote}"
        Label(popup, text=message, font=("Georgia", 10), justify=LEFT).pack(pady=20)

        close_btn = Button(popup, text="Close", command=lambda: self.close_motivation_popup(popup))
        close_btn.pack(pady=10)

        self.shown_motivation_popup = True

    def close_motivation_popup(self, popup):
        """Close the motivation popup."""
        popup.destroy()
        self.shown_motivation_popup = False           

    def close_app(self):
        """Close the application and save the database."""
        self.conn.close()
        self.root.destroy()
    def update_task(self):
        """Update the selected task."""
        try:
            
            selected_task = self.task_list.get(self.task_list.curselection()).replace(" (Done)", "")
            date = self.calendar.get_date()

            
            new_task = simpledialog.askstring("Update Task", "Enter the updated task:", initialvalue=selected_task)
            if not new_task:
                messagebox.showwarning("Input Error", "Task cannot be empty!")
                return

            
            self.cursor.execute(
                "UPDATE lists SET task = ? WHERE user_id = ? AND date = ? AND task = ?",
                (new_task, self.user_id, date, selected_task)
            )
            self.conn.commit()

            
            self.load_tasks()

        except TclError:
            messagebox.showwarning("Selection Error", "Please select a task to update.")


class LoginSignUpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ToDoMate")
        self.root.geometry("600x700")
        self.root.resizable(False, False)  
 
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()
        self.initialize_database()

        bg_image = Image.open("C:/Users/ASUS/Downloads/icon3.jpg")  
        bg_image = bg_image.resize((600, 700), )
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_image_tk)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        header_image = Image.open("C:/Users/ASUS/Downloads/icon2.png") 
        header_image = header_image.resize((150, 150))
        self.header_image_tk = ImageTk.PhotoImage(header_image)
        header_label = Label(self.root, image=self.header_image_tk, bg="white")
        header_label.pack(pady=(20, 10))

        Label(
            root,
            text="Welcome to ToDoMate",
            font=("Verdana", 20, "bold"),
            bg="lightblue",
            fg="#333",
        ).pack(pady=(10, 5))

        Label(
            root,
            text="Your Intelligent Task Management Assistant",
            font=("Georgia", 14),
            bg="lightblue",
            fg="#555",
        ).pack(pady=(0, 20))

        # Instructions
        Label(
            root,
            text="Please sign up to create your new account.",
            font=("Georgia", 12),
            bg="lightblue",
            fg="#333",
        ).pack(pady=(0, 5))

        Label(
            root,
            text="Log in to access your existing account.",
            font=("Georgia", 12),
            bg="lightblue",
            fg="#333",
        ).pack(pady=(0, 20))

        # Buttons
        Button(
            root,
            text="Log In",
            font=("Verdana", 12),
            bg="#4caf50",
            fg="white",
            width=15,
            command=self.login_page,
            height=1, bd=5, relief="raised", highlightthickness=0
        ).pack(pady=10)

        Button(
            root,
            text="Sign Up",
            font=("Verdana", 12),
            bg="#2196f3",
            fg="white",
            width=15,
            command=self.signup_page,
            height=1, bd=5, relief="raised", highlightthickness=0
        ).pack(pady=10)

    def initialize_database(self):
        """Ensure users table exists."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")
        self.conn.commit()

    def login_page(self):
        self.clear()
       
        bg_image = Image.open("C:/Users/ASUS/Downloads/icon4.jpg")
        bg_image = bg_image.resize((600, 700), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        bg_label = Label(self.root, image=bg_photo)
        bg_label.image = bg_photo 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        Label(self.root, text="Welcome back to ToDoMate!", font=("Georgia", 12), bg="lightblue").pack(pady=20)

        Label(self.root, text="Log In", bg="lightblue",font=("Verdana", 16)).pack(pady=20)

        Label(self.root,bg="lightblue", text="Username").pack(pady=20)
        username = Entry(self.root)
        username.pack()

        Label(self.root, bg="lightblue",text="Password").pack(pady=20)
        password = Entry(self.root, show="*")
        password.pack()
        
        def login():
            user = username.get().strip()
            pwd = password.get().strip()

            self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (user, pwd))
            user_data = self.cursor.fetchone()

            if user_data:
                messagebox.showinfo("Success", "Login successful!")
                self.open_todo_app(user_data[0]) 
            else:
                messagebox.showwarning("Error", "Invalid Input!")

        Button(self.root, text="Log In",bg="lightgreen",width=8, height=1, fg="black",bd=5, relief="raised", highlightthickness=0, font=("Verdana", 10), command=login).pack(pady=10)
        Label(self.root, text="Don't have an account?", font=("Georgia", 10), bg="lightblue").pack()
        Button(self.root, text="Sign Up",width=8, height=1, bd=5, relief="raised", highlightthickness=0, font=("Verdana", 10), bg="lightblue", fg="black", command=self.signup_page).pack(pady=10)


    def signup_page(self):
        self.clear()
         
        bg_image = Image.open("C:/Users/ASUS/Downloads/icon4.jpg")
        bg_image = bg_image.resize((600, 700), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        bg_label = Label(self.root, image=bg_photo)
        bg_label.image = bg_photo 
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        Label(self.root, text="Sign Up", font=("Verdana", 16)).pack(pady=20)

        Label(self.root, text="Username").pack(pady=20)
        username = Entry(self.root)
        username.pack()

        Label(self.root, text="Password").pack(pady=20)
        password = Entry(self.root, show="*")
        password.pack()

        def signup():
            user = username.get().strip()
            pwd = password.get().strip()

            if not user or not pwd:
                messagebox.showwarning("Error", "Fields cannot be empty!")
                return

            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
                self.conn.commit()
                messagebox.showinfo("Success", "Account created!")
                self.login_page()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Error", "Username already exists!")

        Button(self.root, text="Sign Up",width=8, height=1, bd=5, relief="raised", highlightthickness=0,font=("Verdana", 10), bg="lightblue", fg="white",command=signup).pack(pady=20)

    def open_todo_app(self, user_id):
        self.root.destroy()
        root = Tk()
        app = ToDoApp(root, user_id)
        root.protocol("WM_DELETE_WINDOW", app.close_app)
        root.mainloop()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = Tk()
    app = LoginSignUpApp(root)
    root.mainloop()


