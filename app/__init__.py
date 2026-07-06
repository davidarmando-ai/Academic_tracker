from flask import Flask
from app.config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.tasks.routes import tasks_bp
    from app.blueprints.calendar.routes import calendar_bp
    from app.blueprints.goals.routes import goals_bp
    from app.blueprints.main.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(goals_bp, url_prefix='/goals')
    app.register_blueprint(main_bp, url_prefix='/')

    with app.app_context():
        from app.models import User, Task, CalendarEvent, StudyGoal
        db.create_all()

    return app
