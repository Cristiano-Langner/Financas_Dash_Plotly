from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from werkzeug.security import generate_password_hash
from app import db, app, User
from dash.exceptions import PreventUpdate

# Layout
def render_layout(message=""):
    message = "Erro no registro." if message == "error" else message
    return dbc.Card([
        html.Legend("Registrar"),
        dbc.Input(id="user_register", placeholder="Username", type="text"),
        dbc.Input(id="pwd_register", placeholder="Password", type="password"),
        dbc.Input(id="email_register", placeholder="E-mail", type="email"),
        dbc.Button("Registrar", id='register-button'),
        html.Span(message, style={"text-align": "center"}),
        html.Div([dcc.Link("Faça login", href="/login")], style={"padding": "20px"})
    ], style={"width": "300px", "min-height": "300px", "padding": "25px"}, className="align-self-center")  # <-- Adiciona o mesmo estilo do login

# Callback
@app.callback(
    Output('register-state', 'data'),
    Input('register-button', 'n_clicks'),
    [State('user_register', 'value'), State('pwd_register', 'value'), State('email_register', 'value')]
)
def register_user(n_clicks, username, password, email):
    if n_clicks is None or not username or not password or not email:
        raise PreventUpdate
    
    try:
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return ""
    except Exception:
        return "error"