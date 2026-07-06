from datetime import datetime
from app.extensions import db


class StudyGoal(db.Model):
    __tablename__ = 'study_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    horas_objetivo = db.Column(db.Float, nullable=False)
    horas_concluidas = db.Column(db.Float, default=0.0)
    prazo = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(20), default='em_andamento')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def progresso_percentual(self):
        if self.horas_objetivo > 0:
            return min(round((self.horas_concluidas / self.horas_objetivo) * 100, 1), 100.0)
        return 0.0

    def __repr__(self):
        return f'<StudyGoal {self.titulo}>'
