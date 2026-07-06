from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.study_goal import StudyGoal
from app.blueprints.goals.forms import GoalForm, ProgressForm

goals_bp = Blueprint('goals', __name__)


@goals_bp.route('/')
@login_required
def list_goals():
    goals_activas = StudyGoal.query.filter_by(
        user_id=current_user.id, estado='em_andamento'
    ).order_by(StudyGoal.prazo.asc().nulls_last()).all()

    goals_concluidas = StudyGoal.query.filter_by(
        user_id=current_user.id, estado='concluida'
    ).order_by(StudyGoal.data_criacao.desc()).all()

    return render_template('goals/list.html', goals=goals_activas, goals_concluidas=goals_concluidas)


@goals_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = StudyGoal(
            user_id=current_user.id,
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            horas_objetivo=form.horas_objetivo.data,
            prazo=form.prazo.data
        )
        db.session.add(goal)
        db.session.commit()
        flash('Meta de estudo criada com sucesso!', 'success')
        return redirect(url_for('goals.list_goals'))
    return render_template('goals/form.html', form=form, titulo='Nova Meta')


@goals_bp.route('/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = StudyGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    form = GoalForm(obj=goal)
    if form.validate_on_submit():
        goal.titulo = form.titulo.data
        goal.descricao = form.descricao.data
        goal.horas_objetivo = form.horas_objetivo.data
        goal.prazo = form.prazo.data
        db.session.commit()
        flash('Meta atualizada com sucesso!', 'success')
        return redirect(url_for('goals.list_goals'))
    return render_template('goals/form.html', form=form, titulo='Editar Meta')


@goals_bp.route('/<int:goal_id>/progress', methods=['POST'])
@login_required
def update_progress(goal_id):
    goal = StudyGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    form = ProgressForm()
    if form.validate_on_submit():
        goal.horas_concluidas = form.horas_concluidas.data
        if goal.horas_concluidas >= goal.horas_objetivo:
            goal.estado = 'concluida'
            flash('Meta concluída! Parabéns!', 'success')
        else:
            flash('Progresso atualizado com sucesso!', 'success')
        db.session.commit()
    return redirect(url_for('goals.list_goals'))


@goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = StudyGoal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    db.session.delete(goal)
    db.session.commit()
    flash('Meta excluída com sucesso!', 'success')
    return redirect(url_for('goals.list_goals'))


@goals_bp.route('/history')
@login_required
def history():
    goals_concluidas = StudyGoal.query.filter_by(
        user_id=current_user.id, estado='concluida'
    ).order_by(StudyGoal.data_criacao.desc()).all()
    return render_template('goals/history.html', goals=goals_concluidas)
