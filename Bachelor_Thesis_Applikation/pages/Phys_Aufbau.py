import dash
from dash import dcc, html, callback, Output, Input
import plotly.graph_objs as go
import dash_leaflet as dl
import json

# Register the subpage Physikalischer Aufbau
dash.register_page(__name__, path='/aufbau', name='Physikalischer Aufbau', order=3)  # is a subpage of the home page

# Define the layout for this page
layout = html.Div([
    html.Div([
        html.H1("Physikalischer Aufbau der Liegenschafen",
                style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
        html.P("Auf dieser Seite werden der Standort, der physikalische Aufbau, wie auch die benötigten Komponenten der Solaranlage erwähnt, welche benötigt werden um das Ganze in Betrieb zu nehmen.",
               style={"text-align": "left"})
    ], style={"margin": "auto", "width": "50%"}),  # Centered text
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Riedgrabenstrasse 5', 'value': '5'},
                    {'label': 'Riedgrabenstrasse 7/9/11', 'value': '7_9_11'},
                    {'label': 'Riedgrabenstrasse 13', 'value': '13'},
                    {'label': 'Riedgrabenstrasse 5/7/9/11/13', 'value': '5_7_9_11_13'}
                ],
                value='5',
                clearable=False,
                style={'color': 'black', 'font-weight': 'bold', 'font-size': '16px',
                       'width': '270px', 'margin-right': '20px', 'margin-top': '20px', 'background-color': 'transparent'}
            ),
            html.Div(
                id='image-slider-container',
                children=[
                    html.Img(id='image1', style={'max-width': '100%'}),
                    html.Img(id='image2', style={'max-width': '100%'}),
                    html.Div(
                        [
                         html.Button(
                            html.Span(className='arrow-button', children=['➜']),
                            id='previous-button',
                            title = 'Zeige den Standort im Bild',
                            style={
                                'font-size': '35px',
                                'font-weight': 'bold',
                                "box-shadow": "2px 2px 5px rgba(0, 0, 0, 0.3)",
                                "transition": "background-color 0.3s ease-in-out",
                                'padding': '25px 25px',
                                'background-color': 'transparent',
                                'color': 'black',
                                'border': 'none',
                                'border-radius': '10px',
                                'cursor': 'pointer',
                                'transform': 'rotate(180deg)',
                            }
                        ),
                        html.Span('Standort', style={'margin-left': '20px', 'margin-right': '20px', 'font-size': '17px', 'font-weight': 'bold', 'color': 'white'}),
                        html.Span('Aufbau', style={'margin-left': '20px', 'margin-right': '20px', 'font-size': '17px', 'color': 'white', 'font-weight': 'bold'}),

                        html.Button(
                            html.Span(className='arrow-button', children=['➜']),
                            id='next-button',
                            title = 'Zeige den Aufbau im Bild',
                            style={
                                'font-size': '35px',
                                'font-weight': 'bold',
                                "box-shadow": "2px 2px 5px rgba(0, 0, 0, 0.3)",
                                "transition": "background-color 0.3s ease-in-out",
                                'padding': '25px 25px',
                                'background-color': 'transparent',
                                'color': 'black',
                                'border': 'none',
                                'border-radius': '2px',
                                'cursor': 'pointer',
                            }
                        )                   
                        ],
                        style={"text-align": "center",'margin-top': '10px'}
                    )
                ],
                style={'margin-top': '15px'}
            )

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50%'}),
        html.Div([
            dl.Map(
                id='map',
                center=[47.4617372, 8.5202995],
                zoom=15,
                style={'width': '90%', 'height': '400px', 'margin-top': '20px'},
                children=[
                    dl.TileLayer(url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
                    dl.Marker(
                        position=[47.462, 8.5195],
                        children=[
                            dl.Tooltip(
                                children=[
                                    html.Div(
                                        "Riedgrabenstrasse 5/7/9/11/13, 8153 Rümlang",
                                        className="custom-tooltip",
                                        style={'font-size': '12px', 'font-weight': 'bold'}
                                    )
                                ],
                                permanent=True
                            )
                        ]
                    )
                ]
            )
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '40%', 'margin-right': '5px'}),
    ], style={'text-align': 'left'})
])


@callback(
    Output('image1', 'src'),
    Output('image2', 'src'),
    Output('previous-button', 'style'),
    Output('next-button', 'style'),
    Input('dropdown', 'value'),
    Input('previous-button', 'n_clicks'),
    Input('next-button', 'n_clicks')
)
def update_images(value, prev_clicks, next_clicks):
    assets_path_standort = 'assets/Phys_Aufbau/Standort_RS_'
    assets_path_aufbau = 'assets/Phys_Aufbau/Aufbau_RS_'
    images = [f'{assets_path_standort}{value}.png', f'{assets_path_aufbau}{value}.png']
    num_images = len(images)
    prev_clicks = prev_clicks or 0
    next_clicks = next_clicks or 0
    current_image_index = (prev_clicks - next_clicks) % num_images

    prev_button_style = {'display': 'inline-block', 'background-color': 'transparent', 'color': 'white'}
    next_button_style = {'display': 'inline-block', 'background-color': 'transparent', 'color': 'white'}

    if current_image_index == 0:
        prev_button_style['display'] = 'none'
    elif current_image_index == num_images - 1:
        next_button_style['display'] = 'none'

    if current_image_index == 0:
        return images[current_image_index], None, prev_button_style, next_button_style
    else:
        return None, images[current_image_index], prev_button_style, next_button_style

# Font Awesome Icons:

#     'fas fa-chevron-left': Solid chevron-left icon
#     'fas fa-chevron-right': Solid chevron-right icon
#     'fas fa-arrow-left': Solid arrow-left icon
#     'fas fa-arrow-right': Solid arrow-right icon
#     'fas fa-angle-left': Solid angle-left icon
#     'fas fa-angle-right': Solid angle-right icon
#     'fas fa-caret-left': Solid caret-left icon
#     'fas fa-caret-right': Solid caret-right icon
#     'fas fa-long-arrow-alt-left': Solid long-arrow-alt-left icon
#     'fas fa-long-arrow-alt-right': Solid long-arrow-alt-right icon

# Bootstrap Icons:

#     'bi bi-chevron-left': Chevron-left icon from Bootstrap Icons
#     'bi bi-chevron-right': Chevron-right icon from Bootstrap Icons
#     'bi bi-arrow-left': Arrow-left icon from Bootstrap Icons
#     'bi bi-arrow-right': Arrow-right icon from Bootstrap Icons
#     'bi bi-caret-left': Caret-left icon from Bootstrap Icons
#     'bi bi-caret-right': Caret-right icon from Bootstrap Icons
#     'bi bi-box-arrow-left': Box-arrow-left icon from Bootstrap Icons
#     'bi bi-box-arrow-right': Box-arrow-right icon from Bootstrap Icons

# Feather Icons:

#     'feather icon-chevron-left': Chevron-left icon from Feather Icons
#     'feather icon-chevron-right': Chevron-right icon from Feather Icons
#     'feather icon-arrow-left': Arrow-left icon from Feather Icons
#     'feather icon-arrow-right': Arrow-right icon from Feather Icons
#     'feather icon-caret-left': Caret-left icon from Feather Icons
#     'feather icon-caret-right': Caret-right icon from Feather Icons
#     'feather icon-corner-left-down': Corner-left-down icon from Feather Icons
#     'feather icon-corner-right-down': Corner-right-down icon from Feather Icons




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
#             var map = L.map('custom-map').setView([51.5074, -0.1278], 10);
#             // Add a tile layer
#             L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
#                 attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
#             }).addTo(map);
#             // Add markers or other map interactions as needed
#         </script>
#         """
#         return html.Div([html.Script(custom_map)])
#     else:
#         return None

