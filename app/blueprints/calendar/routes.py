from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.calendar_event import CalendarEvent
from app.models.task import Task
from app.blueprints.calendar.forms import EventForm
from datetime import date, timedelta
import calendar

calendar_bp = Blueprint('calendar', __name__)


def obter_mes(ano, mes):
    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, calendar.monthrange(ano, mes)[1])
    inicio_calendario = primeiro_dia - timedelta(days=primeiro_dia.weekday())
    fim_calendario = ultimo_dia + timedelta(days=(6 - ultimo_dia.weekday()))
    return primeiro_dia, ultimo_dia, inicio_calendario, fim_calendario


@calendar_bp.route('/')
@login_required
def view_calendar():
    hoje = date.today()
    ano = request.args.get('ano', hoje.year, type=int)
    mes = request.args.get('mes', hoje.month, type=int)

    primeiro_dia, ultimo_dia, inicio_calendario, fim_calendario = obter_mes(ano, mes)

    eventos = CalendarEvent.query.filter(
        CalendarEvent.user_id == current_user.id,
        CalendarEvent.data >= inicio_calendario,
        CalendarEvent.data <= fim_calendario
    ).order_by(CalendarEvent.data).all()

    tarefas = Task.query.filter(
        Task.user_id == current_user.id,
        Task.data_entrega >= inicio_calendario,
        Task.data_entrega <= fim_calendario
    ).order_by(Task.data_entrega).all()

    dias_mes = []
    dia_atual = inicio_calendario
    while dia_atual <= fim_calendario:
        semana = []
        for _ in range(7):
            eventos_dia = [e for e in eventos if e.data == dia_atual]
            tarefas_dia = [t for t in tarefas if t.data_entrega == dia_atual]
            semana.append({
                'data': dia_atual,
                'eventos': eventos_dia,
                'tarefas': tarefas_dia,
                'fora_mes': dia_atual.month != mes,
                'hoje': dia_atual == hoje
            })
            dia_atual += timedelta(days=1)
        dias_mes.append(semana)

    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    dias_semana_pt = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']

    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1
    mes_seguinte = mes + 1 if mes < 12 else 1
    ano_seguinte = ano if mes < 12 else ano + 1

    return render_template(
        'calendar/calendar.html',
        dias_mes=dias_mes,
        mes_atual=meses_pt[mes - 1],
        ano=ano,
        mes=mes,
        mes_anterior=mes_anterior,
        ano_anterior=ano_anterior,
        mes_seguinte=mes_seguinte,
        ano_seguinte=ano_seguinte,
        dias_semana_pt=dias_semana_pt,
        hoje=hoje
    )


@calendar_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        event = CalendarEvent(
            user_id=current_user.id,
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            data=form.data.data,
            tipo=form.tipo.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Evento criado com sucesso!', 'success')
        return redirect(url_for('calendar.view_calendar'))
    return render_template('calendar/form.html', form=form, titulo='Novo Evento')


@calendar_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = CalendarEvent.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.titulo = form.titulo.data
        event.descricao = form.descricao.data
        event.data = form.data.data
        event.tipo = form.tipo.data
        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('calendar.view_calendar'))
    return render_template('calendar/form.html', form=form, titulo='Editar Evento')


@calendar_bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = CalendarEvent.query.filter_by(id=event_id, user_id=current_user.id).first_or_404()
    db.session.delete(event)
    db.session.commit()
    flash('Evento excluído com sucesso!', 'success')
    return redirect(url_for('calendar.view_calendar'))
