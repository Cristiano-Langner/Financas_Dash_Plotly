from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import *
from werkzeug.security import check_password_hash
from flask_login import login_user
from dash.exceptions import PreventUpdate

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding': '25px',
}

# =========  Layout  =========== #
def render_layout(message):
    message_dict = {
        "error_user": "Usuário não encontrado.",
        "error_pass": "Senha incorreta.",
        "error": "Ocorreu um erro durante o login."
    }
    message = message_dict.get(message, "")

    login = dbc.Card([
                html.Legend("Login"),
                dbc.Input(id="user_login", placeholder="Username", type="text"),
                dbc.Input(id="pwd_login", placeholder="Password", type="password"),
                dbc.Button("Login", id="login_button"),
                html.Span(message, style={"text-align": "center", "color": "red"}),

                html.Div([
                    html.Label("Ou", style={"margin-right": "5px"}),
                    dcc.Link("Registre-se", href="/register"),
                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})
            ], style=card_style, className="align-self-center")
    
    return login

# =========  Callbacks Page1  =========== #
@app.callback(
    Output('login-state', 'data'),
    Input('login_button', 'n_clicks'),
    [State('user_login', 'value'), State('pwd_login', 'value')],
)
def successful(n_clicks, username, password):
    if not n_clicks:  # Se não houve clique, não faz nada
        raise PreventUpdate

    if not username or not password:  # Se algum campo estiver vazio
        return "error"

    user = User.query.filter_by(username=username).first()

    if not user:
        return "error_user"  # Mensagem mais específica

    if not check_password_hash(user.password, password):
        return "error_pass"  # Mensagem mais específica

    login_user(user)
    return "success"