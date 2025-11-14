from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from app import db
from forms import LoginForm, RegistrationForm
import logging

logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Get user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check if user exists and password is correct
        if user and form.password.data and check_password_hash(
                user.password_hash, form.password.data):
            # Log in the user
            login_user(user, remember=form.remember.data)

            # Set theme preference from user
            session['theme'] = user.theme_preference

            # Redirect to the page they were trying to access
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')

            flash('Login successful!', 'success')
            return redirect(next_page)
        else:
            flash('Please check your login details and try again.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email address already registered.', 'danger')
            return render_template('register.html', form=form)

        # Check if username already exists
        existing_username = User.query.filter_by(
            username=form.username.data).first()
        if existing_username:
            flash('Username already taken.', 'danger')
            return render_template('register.html', form=form)

        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            theme_preference='dark'  # Default theme
        )

        # Add user to database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration. Please try again.',
                  'danger')

    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        # Update theme preference
        theme = request.form.get('theme')
        if theme in ['light', 'dark']:
            current_user.theme_preference = theme
            session['theme'] = theme
            db.session.commit()
            flash('Preferences updated!', 'success')

    # Get user's quizzes
    from models import QuizDB
    user_quizzes = QuizDB.query.filter_by(user_id=current_user.id).order_by(
        QuizDB.created_at.desc()).all()

    return render_template('profile.html',
                           user=current_user,
                           quizzes=user_quizzes)
