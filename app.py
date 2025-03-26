import dash
import dash_bootstrap_components as dbc
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import os
import logging

# Inicialização do Flask e Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
server = app.server  # O servidor Flask será usado pelo Dash
app.config.suppress_callback_exceptions = True

# Configuração do banco de dados
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=False,
    ENV='production',
)

db = SQLAlchemy(server)  # Inicializa o SQLAlchemy

# Modelo de Usuário
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Inicialização do LoginManager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Função para criar o banco de dados caso não exista
def create_db():
    with server.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run_server(debug=False)