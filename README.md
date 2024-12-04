# Todolist
ToDoMate - A Simple and Efficient Task Management App

ToDoMate is a user-friendly task management application designed to help users organize and track their daily tasks efficiently. Built using Python and SQLite, it offers a minimalistic and intuitive interface to improve productivity.

Features

 • User Authentication:
   • Sign up and log in with a username and password.
 • Task Management:
   • Add, view, update, and delete tasks.
   • Mark tasks as complete.
   • Search tasks by keyword.
 • User Interface:
   • Built with Tkinter for a clean and intuitive design.
 • Database:
   • SQLite for secure and reliable task storage.

Technology Stack

 • Programming Language: Python
 • Database: SQLite
 • Libraries and Tools:
   • tkinter (for GUI)
   • tkcalendar (for calendar widgets)
   • Pillow (for image handling)

Setup and Installation

1. Prerequisites

 • Python 3.8 or higher installed on your system.
 • Internet connection (for fetching online images, if needed).

2. Clone the Repository

git clone https://github.com/yourusername/ToDoMate.git
cd ToDoMate
3. Install Required Libraries

Run the following command to install dependencies:

pip install tkcalendar pillow requests

4. Run the Application

Start the application by executing:

python Final.py

How to Use

 1. Launch the Application:
   • After running the script, the login/sign-up window will appear.
 2. Sign Up or Log In:
   •Create a new account or log in with an existing one.
 3. Add Tasks:
   •Enter task to add a new task.
 4. Manage Tasks:
   •View your task list, delete tasks, or mark them as complete.
 5. Search Tasks:
   •Use keywords to search through your tasks quickly.
 6. Exit:
   •Save your changes and close the application.

Database Structure

 • Users Table: Stores user credentials.
   • Columns: user_id, username, password
 • Tasks Table: Stores task details.
   • Columns: task_id, user_id, task_name,date, status
   
Acknowledgments

 • SQLite Documentation (https://www.sqlite.org/docs.html)
 • Python Official Documentation (https://docs.python.org/3/)
 • Tutorials & resources from W3Schools and YouTube.
