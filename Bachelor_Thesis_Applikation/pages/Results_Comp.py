import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')


dash.register_page(__name__, path='/resultate-vergleichen', name='Resultate vergleichen', order=2) # '/' is the home page for this app


# Define the layout for Results_Compare page
layout = html.Div([
    html.Div([
        html.H1("Resultate vergleichen", className="pages-header"),
        html.P("Auf dieser Seite kann der Nutzer die Resutate von zwei verschiedenen Varianten vergleichen.", className= 'subheader'),
        html.P("Zwei auf der linken Seite auswählen --> Rechts vergleich als Barchart der Resutlate.", className= 'regular-text')
    ], style={"margin": "auto", "width": "60%"}),  # Centered text
])