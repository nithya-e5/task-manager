from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, Task
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered','warning')
            return redirect(url_for('signup'))

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid credentials','danger')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/task/create', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title','').strip()
    desc = request.form.get('description','').strip()

    if not title:
        flash('Title required','warning')
    else:
        task = Task(user_id=current_user.id, title=title, description=desc)
        db.session.add(task)
        db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not allowed','danger')
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('Not allowed','danger')
        return redirect(url_for('dashboard'))

    task.status = 'done' if task.status == 'pending' else 'pending'
    db.session.commit()
    return redirect(url_for('dashboard'))


# ⭐⭐⭐ NEW: EDIT TASK ROUTE ⭐⭐⭐
@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Only allow the owner to edit
    if task.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            flash("Title cannot be empty.", "danger")
            return render_template('edit.html', task=task)

        task.title = title
        task.description = description
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)

