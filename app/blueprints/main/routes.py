from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.task import Task
from app.models.calendar_event import CalendarEvent
from app.models.study_goal import StudyGoal
from datetime import date, timedelta

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def dashboard():
    hoje = date.today()
    fim_semana = hoje + timedelta(days=7)

    tarefas_hoje = Task.query.filter(
        Task.user_id == current_user.id,
        Task.data_entrega == hoje,
        Task.estado != 'concluida'
    ).order_by(Task.prioridade).all()

    tarefas_semana = Task.query.filter(
        Task.user_id == current_user.id,
        Task.data_entrega >= hoje,
        Task.data_entrega <= fim_semana,
        Task.estado != 'concluida'
    ).order_by(Task.data_entrega).all()

    proximos_eventos = CalendarEvent.query.filter(
        CalendarEvent.user_id == current_user.id,
        CalendarEvent.data >= hoje
    ).order_by(CalendarEvent.data).limit(5).all()

    metas_ativas = current_user.study_goals.filter_by(estado='em_andamento').all()
    metas_concluidas = current_user.study_goals.filter_by(estado='concluida').count()

    total_tarefas = current_user.tasks.count()
    tarefas_concluidas = current_user.tasks.filter_by(estado='concluida').count()
    taxa_conclusao = round((tarefas_concluidas / total_tarefas * 100), 1) if total_tarefas > 0 else 0

    tarefas_pendentes = current_user.tasks.filter(Task.estado != 'concluida').count()

    return render_template(
        'main/dashboard.html',
        tarefas_hoje=tarefas_hoje,
        tarefas_semana=tarefas_semana,
        proximos_eventos=proximos_eventos,
        metas_ativas=metas_ativas,
        metas_concluidas=metas_concluidas,
        total_tarefas=total_tarefas,
        tarefas_concluidas=tarefas_concluidas,
        tarefas_pendentes=tarefas_pendentes,
        taxa_conclusao=taxa_conclusao,
        hoje=hoje
    )
