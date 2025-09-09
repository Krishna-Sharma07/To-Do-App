<div align="center">
  <h1 align="center">✅ To-Do App – PySide6 Desktop Task Manager</h1>
  <p align="center">
    A full-featured <strong>desktop to-do list application</strong> built with PySide6.<br />
    Organize your tasks with lists, priorities, reminders, due dates, and more!
  </p>
  <br />
  <img src="https://img.shields.io/badge/PySide6-Qt_for_Python-green?style=for-the-badge&logo=qt&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Desktop-App-informational?style=for-the-badge" />
</div>

---

## 📋 Table of Contents

* [🌟 Features](#features)
* [🛠 Tech Stack](#tech-stack)
* [🚀 Getting Started](#getting-started)
* [📁 Project Structure](#project-structure)
* [🧠 Core Functionalities](#core-functionalities)
* [🎨 Dark Mode Support](#dark-mode-support)
* [🤝 Contributing](#contributing)

---

## 🌟 Features

* ✅ Create & manage **multiple task lists**
* 📝 Add, edit, delete, cut, copy, and paste tasks
* 📌 Set task **priority** (High, Medium, Low)
* ⏰ Add **due dates** and **reminders**
* 🔍 Filter by status: All, Completed, Pending, Overdue
* 🔃 Sort tasks by Name, Due Date, Priority, or Completion
* 💾 Save & load task data as **JSON**
* 🌓 Optional **Dark Mode** toggle for improved UI

---

## 🛠 Tech Stack

| Layer       | Technology              |
| ----------- | ----------------------- |
| Language    | Python 3.10+            |
| GUI Library | PySide6 (Qt for Python) |
| File Format | JSON                    |
| UI Toolkit  | Qt Widgets              |

---

## 🚀 Getting Started

### 🧰 Prerequisites

* Python 3.10+
* `PySide6` library

Install dependencies:

```bash
pip install PySide6
```

### 📦 Run the App

```bash
python to_do_main.py
```

> ℹ️ Make sure both `to_do_app.py` and `to_do_main.py` are in the same directory.

---

## 📁 Project Structure

```
to-do-app/
│
├── to_do_app.py     # Main application logic and GUI
├── to_do_main.py    # Entry point to run the app
└── README.md        # Project documentation
```

---

## 🧠 Core Functionalities

### 🎯 Task Management

* Create/edit/delete task lists and tasks
* Organize tasks by list
* Edit task name inline

### 🚦 Task Details

* Set **Priority** (High ★, Medium ☆, Low)
* Assign **Due Date**
* Set **Reminder** (Date + Time)

### 🗂️ Views & Filters

* Toggle between:

  * All Tasks
  * Completed Tasks
  * Pending Tasks
  * Overdue Tasks

* Sort by:

  * Name (A-Z)
  * Due Date (Earliest First)
  * Priority (High → Low)
  * Completion Status

### 💾 Save / Load

* Save all task data as a `.json` file
* Load from saved `.json` files

---

## 🎨 Dark Mode Support

Toggle dark mode from the **View** menu:

```bash
View → Dark Mode
```

Custom dark stylesheet applied to menus, widgets, and dialogs for better readability.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository
2. Create a feature branch:

   ```bash
   git checkout -b feature/awesome-feature
   ```
3. Commit your changes
4. Push to your fork
5. Open a Pull Request 🚀

---

<div align="center">
  🛠️ Built with Python & ❤️ by <a href="https://github.com/Krishna-Sharma07" target="_blank">Krishna Sharma</a>
</div>

---
