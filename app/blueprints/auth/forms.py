from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User


class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Palavra-passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Palavra-passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Criar Conta')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está registado.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Palavra-passe', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class ProfileForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Atualizar Perfil')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Palavra-passe Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Palavra-passe', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirmar Nova Palavra-passe', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Alterar Palavra-passe')



