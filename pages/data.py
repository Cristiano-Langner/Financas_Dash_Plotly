from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from flask_login import logout_user, current_user
from dash.exceptions import PreventUpdate
from app import app

# Estilo do card
card_style = {
    'width': '800px',
    'min-height': '300px',
    'padding': '25px',
}

# Gerando um gráfico de exemplo
df = pd.DataFrame(np.random.randn(100, 1), columns=["data"])
fig = px.line(df, x=df.index, y="data", template="plotly_dark")

# Layout
def render_layout(username):
    return html.Div([
        dcc.Location(id="url", refresh=True),  # Para redirecionamento
        dbc.Card([
            html.Legend(f"Olá, {username}!"),
            dcc.Graph(figure=fig),
            dbc.Button("Logout", id="logout_button", style={"margin-top": "20px"})
        ], style=card_style)
    ], className="d-flex justify-content-center", style={"height": "100vh"})

# Callback para logout
@app.callback(
    Output('url', 'pathname'),  # Corrigido para 'url'
    Input('logout_button', 'n_clicks')
)
def logout(n_clicks):
    if n_clicks and n_clicks > 0:
        logout_user()
        return '/login'  # Redireciona para a página de login
    raise PreventUpdate