import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale
import base64

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')



dash.register_page(__name__, path='/el-verschaltung', name='El. Verschaltung', order=6) # is a subpage of the home page

# Define the layout for Results_Compare page
layout = html.Div(
    [
        html.Div(
            [
                html.H1("Elektrische Verschaltung", className="pages-header"),
                html.P("Auf dieser Seite kann der Nutzer die elektrische Verschaltung für den momentanen Betrieb wie auch den ZEV anschauen. Dabei geht es um die Verschaltung des Transformators", style={"text-align": "left", 'font-size': '18px', 'fontWeight': 'bold', 'fontFamily': 'Arial', "margin-bottom" : "1%"})
            ],
            style={"margin": "auto", "width": "50%"}  # Centered text
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Img(src="assets/el_verschaltung/Trafo_el_Verschaltung_ist_Zustand_Eigenstrom_x.svg", style={"display": "block", "margin": "auto", "width": "85%", "margin-top" : "5%", "opacity": 0.95}),
                            html.P("Verschaltung des Transformators im Ist-Zustand. Die selbe Verschaltung gilt auch für das Eigenstrom X Modell vom Energienetzwerk Rümlang (EWR).", style={ 'font-size': '16px', 'fontWeight': 'normal', 'fontFamily': 'Arial', "text-align": "left", "margin-top" : "5%", "margin-left" : "5%", "margin-right" : "5%"})
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Img(src="assets/el_verschaltung/Trafo_el_Verschaltung_Zev.svg", style={"display": "block", "margin": "auto", "width": "85%", "margin-top" : "5%", "opacity": 1}),
                            html.P("Verschaltung des Transformators im ZEV. Dabei werden alle elektrischen Komponenten ab der gestrichelten Linie privatisiert und sind nicht mehr in der Verantwortung von EWR.", style={ 'font-size': '16px', 'fontWeight': 'normal', 'fontFamily': 'Arial',"text-align": "left", "margin-top" : "5%", "margin-left" : "5%", "margin-right" : "5%"})
                        ]
                    ),
                    width=6,
                ),
            ]
        ),
    ]
)
# , style={"margin": "auto"}),  # Centered text



# def encode_svg(file_path):
#     with open(file_path, "rb") as file:
#         svg_data = file.read()
#         encoded_data = base64.b64encode(svg_data).decode("utf-8")
#         return encoded_data
