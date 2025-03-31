from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from flask_login import login_user
from werkzeug.security import check_password_hash
from app.forms import LoginForm
from flask_login import logout_user, login_required, current_user
from flask_login import login_required, current_user
from flask import abort
from app.forms import EditProfileForm
from app.forms import TranscriptRequestForm
from app.models import TranscriptRequest


main = Blueprint('main', __name__)

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

@main.route('/transcript_requests')
@login_required
def view_transcript_requests():
    if current_user.role not in ['teacher', 'admin']:
        abort(403)
    requests = TranscriptRequest.query.order_by(TranscriptRequest.timestamp.desc()).all()
    return render_template('transcript_requests.html', requests=requests)

@main.route('/transcript_request/<int:request_id>/approve')
@login_required
def approve_request(request_id):
    if current_user.role not in ['teacher', 'admin']:
        abort(403)
    req = TranscriptRequest.query.get_or_404(request_id)
    req.status = 'approved'
    db.session.commit()
    flash('Request approved.', 'success')
    return redirect(url_for('main.view_transcript_requests'))

@main.route('/transcript_request/<int:request_id>/reject')
@login_required
def reject_request(request_id):
    if current_user.role not in ['teacher', 'admin']:
        abort(403)
    req = TranscriptRequest.query.get_or_404(request_id)
    req.status = 'rejected'
    db.session.commit()
    flash('Request rejected.', 'danger')
    return redirect(url_for('main.view_transcript_requests'))

from flask import abort

@main.route('/forbidden-test')
def forbidden_test():
    abort(403)


@main.route('/student/profile')
@login_required
def student_profile():
    if current_user.role != 'student':
        abort(403)
    return render_template('student_profile.html', user=current_user)

@main.route('/student/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role != 'student':
        abort(403)

    form = EditProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.student_profile'))

    return render_template('edit_profile.html', form=form)

@main.route('/request/transcript', methods=['GET', 'POST'])
@login_required
def request_transcript():
    if current_user.role != 'student':
        abort(403)

    form = TranscriptRequestForm()
    if form.validate_on_submit():
        req = TranscriptRequest(
            student_id=current_user.id,
            reason=form.reason.data
        )
        db.session.add(req)
        db.session.commit()
        flash('Transcript request submitted!', 'success')
        return redirect(url_for('main.student_dashboard'))
    return render_template('request_transcript.html', form=form)

@main.route('/transcript_requests')
@login_required
def transcript_requests():
    if current_user.role not in ['teacher', 'admin']:
        abort(403)

    requests = TranscriptRequest.query.all()
    return render_template('transcript_requests.html', requests=requests)
