from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class EventForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=200)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    data = DateField('Data', validators=[DataRequired()], format='%Y-%m-%d')
    tipo = SelectField('Tipo', choices=[
        ('exame', 'Exame'),
        ('entrega', 'Entrega'),
        ('aula', 'Aula Importante'),
        ('outro', 'Outro')
    ], default='outro')
    submit = SubmitField('Salvar')
