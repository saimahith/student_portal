from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_user
from werkzeug.security import check_password_hash
from app.forms import LoginForm
main = Blueprint('main', __name__)
from flask_login import logout_user, login_required, current_user
from flask_login import login_required, current_user
from flask import abort

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.index'))  # ✅ temporary fix
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            
            # ✅ Role-based redirect
            if user.role == 'student':
                return redirect(url_for('main.student_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('main.teacher_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.index'))

        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))  # Or 'main.index' if you prefer

@main.route('/dashboard/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        abort(403)
    return render_template('student_dashboard.html', user=current_user)

@main.route('/dashboard/teacher')
@login_required
def teacher_dashboard():
    if current_user.role != 'teacher':
        abort(403)
    return render_template('teacher_dashboard.html', user=current_user)

@main.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    return render_template('admin_dashboard.html', user=current_user)

from flask import abort

@main.route('/forbidden-test')
def forbidden_test():
    abort(403)

