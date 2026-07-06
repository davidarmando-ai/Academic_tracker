from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=200)])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    disciplina = StringField('Disciplina/Cadeira', validators=[Optional(), Length(max=100)])
    data_entrega = DateField('Data de Entrega', validators=[Optional()], format='%Y-%m-%d')
    prioridade = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta')
    ], default='media')
    estado = SelectField('Estado', choices=[
        ('pendente', 'Pendente'),
        ('em_progresso', 'Em Progresso'),
        ('concluida', 'Concluída')
    ], default='pendente')
    submit = SubmitField('Salvar')
