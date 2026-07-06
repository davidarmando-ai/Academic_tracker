import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-super-secreta-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://'
    ) or f'sqlite:///{Path(__file__).resolve().parent.parent / "instance" / "academic_tracker.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
