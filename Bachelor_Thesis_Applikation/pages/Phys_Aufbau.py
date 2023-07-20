import dash
from dash import dcc, html, callback, Output, Input
import plotly.graph_objs as go
import dash_leaflet as dl
import json

# Register the subpage Physikalischer Aufbau
dash.register_page(__name__, path='/aufbau', name='Physikalischer Aufbau', order=2)  # is a subpage of the home page

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
                            html.Span(className='far fa-chevron-left', style={'margin-right': '10px', 'color': 'black', 'font-size': '20px'}),
                            id='previous-button',
                            n_clicks=0,
                            style={'display': 'inline-block', 'color': 'white', 'background-color': 'transparent', 'border': 'none'}
                        ),
                        html.Span('Standort', style={'margin-right': '20px', 'font-size': '15px', 'font-weight': 'bold', 'color': 'white'}),
                        html.Span('Aufbau', style={'margin-left': '20px','font-size': '15px', 'color': 'white', 'font-weight': 'bold'}),
                        html.Button(
                            html.Span(className='fas fa-chevron-right', style={'margin-left': '10px', 'color': 'black', 'font-size': '20px'}),
                            id='next-button',
                            n_clicks=0,
                            style={'display': 'inline-block', 'color': 'white', 'background-color': 'transparent', 'border': 'none'}
                        )                         
                        ],
                        style={'margin-top': '10px'}
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



# @callback(
#     Output('image1', 'src'),
#     Output('image2', 'src'),
#     Output('previous-button', 'style'),
#     Output('next-button', 'style'),
#     Input('dropdown', 'value'),
#     Input('previous-button', 'n_clicks'),
#     Input('next-button', 'n_clicks')
# )



# def update_images(value, prev_clicks, next_clicks):
#     assets_path_standort = 'assets/Phys_Aufbau/Standort_RS_'
#     assets_path_aufbau = 'assets/Phys_Aufbau/Aufbau_RS_'
#     images = [f'{assets_path_standort}{value}.png', f'{assets_path_aufbau}{value}.png']
#     num_images = len(images)
#     prev_clicks = prev_clicks or 0
#     next_clicks = next_clicks or 0
#     current_image_index = (prev_clicks - next_clicks) % num_images

#     prev_button_style = {'display': 'inline-block', 'background-color': 'transparent', 'color': 'white'}
#     next_button_style = {'display': 'inline-block', 'background-color': 'transparent', 'color': 'white'}

#     if current_image_index == 0:
#         prev_button_style['display'] = 'none'
#     elif current_image_index == num_images - 1:
#         next_button_style['display'] = 'none'

#     return images[current_image_index], images[current_image_index + 1], prev_button_style, next_button_style

# def update_images(value, prev_clicks, next_clicks):
#     assets_path_standort = 'assets/Phys_Aufbau/Standort_RS_'
#     assets_path_aufbau = 'assets/Phys_Aufbau/Aufbau_RS_'
#     images = [f'{assets_path_standort}{value}.png', f'{assets_path_aufbau}{value}.png']
#     num_images = len(images)
#     prev_clicks = prev_clicks or 0
#     next_clicks = next_clicks or 0
#     current_image_index = (prev_clicks - next_clicks) % num_images

#     prev_button_style = {}
#     next_button_style = {}

#     if current_image_index == 0:
#         prev_button_style = {'display': 'none'}
#     elif current_image_index == num_images - 1:
#         next_button_style = {'display': 'none'}

#     return images[current_image_index], images[current_image_index + 1], prev_button_style, next_button_style













# import dash
# from dash import dcc, html, callback, Output, Input
# import plotly.graph_objs as go
# import dash_leaflet as dl
# import json

# #register the subpage Physikalischer Aufbau
# dash.register_page(__name__, path='/aufbau', name='Physikalischer Aufbau', order=2) # is a subpage of the home page

# # Define the layout for the this page
# layout = html.Div([
#     html.Div([
#         html.H1("Physikalischer Aufbau der Liegenschafen", style={"text-align": "center", 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
#         html.P("Auf dieser Seite werden der Standort, der physikalische Aufbau, wie auch die benötigten Komponenten der Solaranlage erwähnt, welche benötigt werden um das Ganze in Betrieb zu nehmen.", style={"text-align": "left"})
#     ], style={"margin": "auto", "width": "50%"}),  # Centered text
#     html.Div([
#         html.Div([
#             dcc.Dropdown(
#                 id='dropdown',
#                 options=[
#                     {'label': 'Riedgrabenstrasse 5', 'value': '5'},
#                     {'label': 'Riedgrabenstrasse 7/9/11', 'value': '7_9_11'},
#                     {'label': 'Riedgrabenstrasse 13', 'value': '13'},
#                     {'label': 'Riedgrabenstrasse 5/7/9/11/13', 'value': '5_7_9_11_13'}
#                 ],
#                 value='5',
#                 clearable=False,
#                 style={'color': 'black','font-weight': 'bold', 'font-size': '16px','width': '270px', 'margin-right': '20px', 'margin-top': '20px','background-color': 'transparent'}
#             ),
#             html.Div(
#                 id='image-container',
#                 children=[
#                     html.Img(id='image', style={'max-width': '100%'})
#                 ],
#                 style={'margin-top': '15px'}
#             )
#         ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50%'}),
#         html.Div([
#             dl.Map(
#                 id='map',
#                 center=[47.4617372, 8.5202995],
#                 zoom=15,
#                 style={'width': '90%', 'height': '400px', 'margin-top': '20px'},
#                 children=[
#                     dl.TileLayer(url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
#                     dl.Marker(
#                         position=[47.462, 8.5195],
#                         children=[
#                             dl.Tooltip(
#                                 children=[
#                                     html.Div(
#                                         "Riedgrabenstrasse 5/7/9/11/13, 8153 Rümlang",
#                                         className="custom-tooltip",
#                                         style={'font-size': '12px', 'font-weight': 'bold'}
#                                     )
#                                 ],
#                                 permanent=True
#                             )
#                         ]
#                     )
#                 ]
#             )
#         ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '40%','margin-right': '5px'}),
#     ], style={'text-align': 'left'})
# ])



# @callback(
#     Output('image', 'src'),
#     Input('dropdown', 'value')
# )
# def update_image(value):

#     assets_path = 'assets/Phys_Aufbau/Standort_RS_'
#     return f'{assets_path}{value}.png'



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

