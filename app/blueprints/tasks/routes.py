from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.task import Task
from app.blueprints.tasks.forms import TaskForm
from datetime import date

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/')
@login_required
def list_tasks():
    query = Task.query.filter_by(user_id=current_user.id)

    filtro_estado = request.args.get('estado')
    filtro_prioridade = request.args.get('prioridade')
    filtro_disciplina = request.args.get('disciplina')
    ordenar_por = request.args.get('ordenar', 'data_entrega')

    if filtro_estado:
        query = query.filter_by(estado=filtro_estado)
    if filtro_prioridade:
        query = query.filter_by(prioridade=filtro_prioridade)
    if filtro_disciplina:
        query = query.filter_by(disciplina=filtro_disciplina)

    if ordenar_por == 'prioridade':
        ordem_prioridade = db.case(
            (Task.prioridade == 'alta', 1),
            (Task.prioridade == 'media', 2),
            (Task.prioridade == 'baixa', 3),
            else_=4
        )
        query = query.order_by(ordem_prioridade)
    elif ordenar_por == 'titulo':
        query = query.order_by(Task.titulo)
    elif ordenar_por == 'disciplina':
        query = query.order_by(Task.disciplina)
    else:
        query = query.order_by(Task.data_entrega.asc().nulls_last())

    tasks = query.all()
    disciplinas = db.session.query(Task.disciplina).filter_by(user_id=current_user.id).distinct().all()
    disciplinas = [d[0] for d in disciplinas if d[0]]

    hoje = date.today()

    return render_template(
        'tasks/list.html',
        tasks=tasks,
        disciplinas=disciplinas,
        filtro_estado=filtro_estado,
        filtro_prioridade=filtro_prioridade,
        filtro_disciplina=filtro_disciplina,
        ordenar_por=ordenar_por,
        hoje=hoje
    )


@tasks_bp.route('/kanban')
@login_required
def kanban():
    pendentes = Task.query.filter_by(user_id=current_user.id, estado='pendente').order_by(
        Task.data_entrega.asc().nulls_last()
    ).all()
    em_progresso = Task.query.filter_by(user_id=current_user.id, estado='em_progresso').order_by(
        Task.data_entrega.asc().nulls_last()
    ).all()
    concluidas = Task.query.filter_by(user_id=current_user.id, estado='concluida').order_by(
        Task.data_entrega.asc().nulls_last()
    ).all()
    hoje = date.today()
    return render_template(
        'tasks/kanban.html',
        pendentes=pendentes,
        em_progresso=em_progresso,
        concluidas=concluidas,
        hoje=hoje
    )


@tasks_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            user_id=current_user.id,
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            disciplina=form.disciplina.data,
            data_entrega=form.data_entrega.data,
            prioridade=form.prioridade.data,
            estado=form.estado.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/form.html', form=form, titulo='Nova Tarefa')


@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.titulo = form.titulo.data
        task.descricao = form.descricao.data
        task.disciplina = form.disciplina.data
        task.data_entrega = form.data_entrega.data
        task.prioridade = form.prioridade.data
        task.estado = form.estado.data
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/form.html', form=form, titulo='Editar Tarefa')


@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('tasks.list_tasks'))


@tasks_bp.route('/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    estados = {'pendente': 'em_progresso', 'em_progresso': 'concluida', 'concluida': 'pendente'}
    task.estado = estados.get(task.estado, 'pendente')
    db.session.commit()
    flash(f'Tarefa marcada como "{task.estado}".', 'info')
    return redirect(request.referrer or url_for('tasks.list_tasks'))
