from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class GoalForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=200)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    horas_objetivo = FloatField('Horas Objetivo', validators=[DataRequired(), NumberRange(min=0.1)])
    prazo = DateField('Prazo', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Salvar')


class ProgressForm(FlaskForm):
    horas_concluidas = FloatField('Horas Concluídas', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Atualizar Progresso')
