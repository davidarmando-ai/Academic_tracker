from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.blueprints.auth.forms import (
    RegistrationForm, LoginForm, ProfileForm,
    PasswordChangeForm
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(nome=form.nome.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Conta criada com sucesso! Já pode entrar.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Bem-vindo(a), {user.nome}!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        flash('Email ou palavra-passe incorretos.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    password_form = PasswordChangeForm()
    if form.validate_on_submit() and 'submit' in request.form:
        if form.email.data != current_user.email and \
                User.query.filter_by(email=form.email.data).first():
            flash('Este email já está em uso.', 'danger')
        else:
            current_user.nome = form.nome.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
    form.nome.data = current_user.nome
    form.email.data = current_user.email
    return render_template('auth/profile.html', form=form, password_form=password_form)


@auth_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    password_form = PasswordChangeForm()
    if password_form.validate_on_submit():
        if current_user.check_password(password_form.current_password.data):
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Palavra-passe alterada com sucesso!', 'success')
        else:
            flash('Palavra-passe atual incorreta.', 'danger')
    return redirect(url_for('auth.profile'))



