from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash
from flask_login import current_user
from waitress import serve
from app import app
from pages import login, data, register

# Layout principal
app.layout = html.Div([
    dcc.Location(id="base-url", refresh=False),
    dcc.Store(id="login-state", data=""),
    dcc.Store(id="register-state", data=""),
    html.Div(id="page-content", style={"height": "100vh", "display": "flex", "justify-content": "center"})
])

# Callbacks
@app.callback(
    Output("base-url", "pathname"),
    [Input("login-state", "data"), Input("register-state", "data")]
)
def redirect_user(login_state, register_state):
    if login_state == "success":
        return "/data"
    elif login_state == "error" or register_state == "":
        return "/login"
    elif register_state:
        return "/register"
    return "/"

@app.callback(
    Output("page-content", "children"),
    Input("base-url", "pathname"),
    [State("login-state", "data"), State("register-state", "data")]
)
def render_page(pathname, login_state, register_state):
    if pathname in ["/", "/login"]:
        return login.render_layout(login_state)
    if pathname == "/register":
        return register.render_layout(register_state)
    if pathname == "/data" and current_user.is_authenticated:
        return data.render_layout(current_user.username)
    return login.render_layout(register_state)

if __name__ == "__main__":
    serve(app.server, host='0.0.0.0', port=8050)