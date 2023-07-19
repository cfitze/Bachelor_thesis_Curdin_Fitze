import base64
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/bachelor-thesis', name='Bachelor Thesis', order=4) # is a subpage of the home page


# Define the layout for the PDF page
layout = html.Div([
    html.Div([
        html.H1("Bachelor Thesis", style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
        html.P("Willkommen bei der Bachelor Thesis von Curdin Fitze.", style={"text-align": "center"})
    ], style={"margin": "auto", "width": "50%"}),  # Centered text

    html.Iframe(src="data:application/pdf;base64," + base64.b64encode(open('Bachelor_Thesis_Applikation/assets/Bachelorthesis_EUT_P6_FS23_Curdin_Fitze-2.pdf', "rb").read()).decode('utf-8'),
                style={"width": "90%", "height": "700px", "zoom": "80%"})
                # style={"width": "100%", "height": "500px"})
])