import dash
from dash import dcc, html, callback, Output, Input
import plotly.graph_objs as go
import dash_leaflet as dl
import json



dash.register_page(__name__, path='/aufbau', name='Physikalischer Aufbau', order=2) # is a subpage of the home page

# Define the layout for the PDF page
layout = html.Div([
    html.Div([
        html.H1("Physikalischer Aufbau der Liegenschafen", style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
        html.P("Auf dieser Seite werden der Standort, der physikalische Aufbau, wie auch die benötigten Komponenten der Solaranlage erwähnt, welche benötigt werden um das Ganze in Betrieb zu nehmen.", style={"text-align": "left"})
    ], style={"margin": "auto", "width": "50%"}),  # Centered text
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Riedgrabenstrasse 5', 'value': 'option1'},
                {'label': 'Riedgrabenstrasse 7/9/11', 'value': 'option2'},
                {'label': 'Riedgrabenstrasse 13', 'value': 'option3'},
                {'label': 'Riedgrabenstrasse 5/7/9/11/13', 'value': 'option4'}
            ],
            value='option1',
            clearable=False,  # This will disable the clearable 'x' option
            style={'width': '270px', 'margin-right': '20px', 'margin-top': '30px'}
        ),
        html.Div(
            id='map-container',
            children=[
                html.Div(id='map-dash-leaflet'),
                html.Div(id='map-custom-js')
            ],
            style={'width': '70%', 'margin-top': '20px'}
        )
    ], style={'width': '50%', 'display': 'inline-block'})
])


# Option 2: Using dash-leaflet
@callback(
    Output('map-dash-leaflet', 'children'),
    Input('dropdown', 'value')
)
def update_leaflet(value):
    if value == 'option1':
        map_data = dl.Map(
            center=[47.4617372, 8.5202995],  # Rümlang coordinates
            zoom=15,
            style={'width': '100%', 'height': '400px'},
            children=[
                dl.TileLayer(url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
                dl.Marker(position=[47.4618, 8.5201])
            ]
        )
        return map_data
    else:
        return None

# Option 3: Using custom JavaScript
@callback(
    Output('map-custom-js', 'children'),
    Input('dropdown', 'value')
)
def update_custom_js(value):
    if value == 'option2':
        custom_map = """
        <div id='custom-map' style='width: 100%; height: 400px;'></div>
        <script>
            // Create the map instance
            var map = L.map('custom-map').setView([51.5074, -0.1278], 10);
            // Add a tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(map);
            // Add markers or other map interactions as needed
        </script>
        """
        return html.Div([html.Script(custom_map)])
    else:
        return None



# # Option 2: Using dash-leaflet
# @callback(
#     Output('map-dash-leaflet', 'children'),
#     Input('dropdown', 'value')
# )
# def update_leaflet(value):
#     if value == 'option1':
#         map_data = dl.Map(
#             center=[51.5074, -0.1278],  # London coordinates
#             zoom=10,
#             style={'width': '100%', 'height': '400px'}
#         )
#         return map_data
#     else:
#         return None


# # Option 3: Using custom JavaScript
# @callback(
#     Output('map-custom-js', 'children'),
#     Input('dropdown', 'value')
# )
# def update_custom_js(value):
#     if value == 'option2':
#         custom_map = """
#         <div id='custom-map' style='width: 100%; height: 400px;'></div>
#         <script>
#             // Create the map instance
#             var map = new google.maps.Map(document.getElementById('custom-map'), {
#                 center: {lat: 51.5074, lng: -0.1278},  // London coordinates
#                 zoom: 10
#             });
#             // Add markers or other map interactions as needed
#         </script>
#         """
#         return html.Div([html.Script(custom_map)])
#     else:
#         return None