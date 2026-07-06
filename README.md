# AcademicTracker

Aplicação web de organização de tarefas acadêmicas para estudantes.

## Pilha Técnica

- **Backend:** Python + Flask + Flask-SQLAlchemy
- **Autenticação:** Flask-Login + Flask-WTF + Werkzeug (bcrypt)
- **Base de Dados:** SQLite (preparado para migrar para PostgreSQL)
- **Frontend:** HTML + CSS + Jinja2 + Bootstrap 5

## Funcionalidades

- Sistema de registo e autenticação de utilizadores
- Gestão de tarefas académicas (CRUD, filtros, vista kanban)
- Calendário académico (vista mensal com eventos e tarefas)
- Metas de estudo com progresso e histórico
- Dashboard com resumo e estatísticas

## Como Executar Localmente

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd academic_tracker
```

### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
```

- Windows: `venv\Scripts\activate`
- Linux/macOS: `source venv/bin/activate`

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Estrutura do Projeto

```
academic_tracker/
├── app/
│   ├── __init__.py            # App factory
│   ├── config.py              # Configurações
│   ├── extensions.py          # Extensões Flask
│   ├── models/                # Modelos de dados
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── calendar_event.py
│   │   └── study_goal.py
│   ├── blueprints/            # Blueprints por módulo
│   │   ├── auth/              # Autenticação
│   │   ├── tasks/             # Tarefas
│   │   ├── calendar/          # Calendário
│   │   ├── goals/             # Metas
│   │   └── main/              # Dashboard
│   ├── templates/             # Templates Jinja2
│   ├── static/                # Ficheiros estáticos
├── instance/                  # Base de dados (SQLite)
├── run.py                     # Ponto de entrada
└── requirements.txt           # Dependências
```

## Migração para PostgreSQL

Para migrar do SQLite para PostgreSQL:

1. Instalar `psycopg2`: `pip install psycopg2-binary`
2. Configurar a variável de ambiente `DATABASE_URL`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/academic_tracker
   ```
3. A aplicação usa SQLAlchemy ORM, por isso as migrações são transparentes.
