#!/usr/bin/env python3

# Importation des bibliothèques nécessaires
import datetime as dt
import csv
import numpy as np
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pathlib import Path
import plotly.express as px
import dash_bootstrap_components as dbc

# Utilisation du thème Darkly pour le style
external_stylesheets = [dbc.themes.DARKLY]

# Création de l'application Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Evolution du Bitcoin"

# Création de la mise en page du dashboard

app.layout = html.Div(children=[
    html.H1("Evolution du Bitcoin", style={"text-align": "center", "color":"orange", "font-family": "Roboto, sans-serif", "font-size": "60px"}),
    html.Div([
        html.Div(id="data-update", style={"color":"black", "font-weight": "bold", "font-size": "24px", "font-family": "Roboto, sans-serif"}),
    ], style={"background-color": "#EAF2F8", "padding": "10px", "border-radius": "10px", "position": "absolute", "top": "10px", "left": "10px"}),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0),
    dcc.Graph(id="graph-update"),
    html.Div([
        html.H2("Rapport journalier sur le Bitcoin à 20h", style={"text-align": "center", "color":"white", "font-family": "Roboto, sans-serif", "font-size": "40px"}),
        html.Div(id="details-update", style={"color":"white", "font-size": "24px", "font-family": "Roboto, sans-serif"}),
        html.Div([
            html.Div(id="data-j-max", style = {"text-align": "center", "color":"orange", "font-family": "Roboto, sans-serif", "font-size": "30px"}),
            html.Div(id="data-j-min", style = {"text-align": "center", "color":"orange", "font-family": "Roboto, sans-serif", "font-size": "30px"}),
            html.Div(id="data-j-vol", style = {"text-align": "center", "color":"orange", "font-family": "Roboto, sans-serif", "font-size": "30px"})
        ], style={"background-color": "gray", "padding": "20px", "border-radius": "10px", "margin-top": "50px"})
    ], style={"background-color": "black"})
])

@app.callback(
    dash.dependencies.Output("data-update", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)


# Fonction pour actualiser les données du bloc de données
def recup(n):
    with open('data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    last_row = rows[-1]
    last_price = last_row['bitcoin']
    return 'Dernier prix scraper : {} $'.format(last_price)


@app.callback(
    dash.dependencies.Output("graph-update", "figure"),
    dash.dependencies.Input("interval-component", "n_intervals")
)

# Mise à jour du graphique
def maj_graph(n):
    df = pd.read_csv('data.csv')
    df = df.loc[:, ['t', 'bitcoin']]
    df["t"] = pd.to_datetime(df["t"], unit="s")
    fig=px.line(df, x="t", y="bitcoin")
    fig.update_layout(
        title={"text" : "Courbe de l'évolution du Bitcoin en temps réel", "x" : 0.5},
        xaxis_title="Date",
        yaxis_title="Prix (en USD)",
        template="plotly_dark"
    )
    fig.update_traces(line=dict(color="red"))
    return fig

@app.callback(
    dash.dependencies.Output("data-j-min", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)


# Récupérer les données journalières dans le csv du rapport

# Le minimum
def min_donnee_j(n):
    df = pd.read_csv('rapport.csv')
    df = df.loc[:, ['t', 'bitcoin']]
    min_price = df['bitcoin'].min()
    return f'Minimum: {min_price} $'

@app.callback(
    dash.dependencies.Output("data-j-max", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)


# Le maximum
def max_donnee_j(n):
    df = pd.read_csv('rapport.csv')
    df = df.loc[:, ['t', 'bitcoin']]
    max_price = df['bitcoin'].max()
    return f'Maximum : {max_price} $'


@app.callback(
    dash.dependencies.Output("data-j-vol", "children"),
    dash.dependencies.Input("interval-component", "n_intervals")
)

# La volatilité
def max_donnee_j(n):
    df = pd.read_csv('rapport.csv')
    df = df.loc[:, ['t', 'bitcoin']]
    vol_price = df['bitcoin'].std()
    return f'Volatilité : {vol_price}'

# Lancer l'application Dash sur un serveur
if __name__ == '__main__':
   app.run_server(host='0.0.0.0', port=8050, debug=True)
