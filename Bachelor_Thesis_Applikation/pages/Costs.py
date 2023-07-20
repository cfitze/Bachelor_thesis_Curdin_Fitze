import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')


dash.register_page(__name__, path='/kosten', name='Kosten berechnen', order=4) # is a subpage of the home page


# Define the layout for Results_Compare page
layout = html.Div([
    html.Div([
        html.H1("Kostenberechnung", style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
        html.P("Auf dieser Seite kann der Nutzer die Kosten von zwei verschiedenen Varianten vergleichen.", style={"text-align": "center"})
    ], style={"margin": "auto", "width": "50%"}),  # Centered text
])