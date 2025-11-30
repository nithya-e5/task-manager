# Task Manager (Full-Stack - Flask + MySQL)

## Run locally (dev)
1. Create virtual env:
   python -m venv venv
   source venv/bin/activate   (on Windows: venv\Scripts\activate)

2. Install:
   pip install -r requirements.txt

3. Create .env file:
   SECRET_KEY=change_me
   DATABASE_URL=mysql+mysqlconnector://root:password@localhost/task_manager

4. Start MySQL and create DB:
   CREATE DATABASE task_manager;

5. Run:
   flask run
   or
   python app.py

## Features
- Signup / Login
- Add / Edit / Delete tasks
- Mark task done/pending
