import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import locale


#register the page Resultate
dash.register_page(__name__, path='/', name='Resultate', order=1) # '/' is the home page for this app

layout = dbc.Container([
    html.H1('Kennzahlen der Liegenschaften', className='pages-header'),
    html.P('Auf dieser Seite kann der Nutzer die Kennzahlen der Liegenschaften anschauen.', className='subheader'),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='pie-chart', style={'margin-top': '20px', 'background-color': 'transparent'}),
                
            ]),
            width=6,
            style={'padding-right': '50px'}  # Add padding to the right of the left column
        ),

        dbc.Col([
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
                    clearable=False,
                    style={'color': 'black', 'font-weight': 'bold', 'font-size': '16px', 'width': '270px', 'margin-right': '20px', 'margin-top': '30px', 'background-color': 'transparent'},
                ),
                html.Div( 
                    id='table-container',
                    children=[
                        html.Table(
                            id='table1',
                            style={
                                'border': '1px solid black',
                                'border-collapse': 'collapse',
                                'width': '100%',
                                'margin': 'auto',
                                'margin-top': '5px'
                            },
                            children=[
                                html.Tr([
                                    html.Th('Column 1', style={'border': '1px solid black', 'padding': '8px'}),
                                    html.Th('Column 2', style={'border': '1px solid black', 'padding': '8px'}),
                                    html.Th('Column 3', style={'border': '1px solid black', 'padding': '8px'})
                                ])
                            ]
                        ),
                        html.Table(
                            id='table2',
                            style={
                                'border': '1px solid black',
                                'border-collapse': 'collapse',
                                'width': '100%',
                                'margin': 'auto',
                                'margin-top': '15px'
                            },
                            children=[
                                html.Tr([
                                    html.Th('Column 1', style={'border': '1px solid black', 'padding': '8px'}),
                                    html.Th('Column 2', style={'border': '1px solid black', 'padding': '8px'}),
                                    html.Th('Column 3', style={'border': '1px solid black', 'padding': '8px'})
                                ])
                            ]
                        )
                    ],
                    style={'overflow': 'auto'}
                )
            ]),
        ], width=6,
        style={'padding-left': '50px'}  # Add padding to the right of the left column
        
        ),
    ], style={'margin-top': '20px'}),
])


# Callback for the pie chart
@callback(
    Output('pie-chart', 'figure'),  # The output is the children of the pie chart container
    Input('main_store', 'data'),
)
def update_pie_chart(data_main_store): # The input argument is the data from the main store

    # Set the locale
    locale.setlocale(locale.LC_ALL, 'de_CH')

    data_frames_stromdaten_pd_frame = pd.DataFrame(data_main_store['data_frames'])

    data_frames_stromdaten_column_names = data_frames_stromdaten_pd_frame.columns.tolist()

    data_frames_stromdaten_5 = round(data_frames_stromdaten_pd_frame[data_frames_stromdaten_column_names[0]].sum()/4,0)

    data_frames_stromdaten_7_9_11 = round(data_frames_stromdaten_pd_frame[data_frames_stromdaten_column_names[1]].sum()/4,0)

    data_frames_stromdaten_13 = round(data_frames_stromdaten_pd_frame[data_frames_stromdaten_column_names[2]].sum()/4,0)

    # Load data later from the Excel file from Solextron
    labels_yearly_consumption = ['<b>Riedgrabenstrasse 5</b>', '<b>Riedgrabenstrasse 7/9/11</b>','<b>Riedgrabenstrasse 13</b>']
    values_yearly_consumption = [data_frames_stromdaten_5, data_frames_stromdaten_7_9_11, data_frames_stromdaten_13]  #later replace with data from Excel file

    # Format the values with the thousands separator
    values_yearly_consumption_formatted = [locale.format('%.0f', value, grouping=True) for value in values_yearly_consumption]

    # Create pie chart trace
    trace = go.Pie(
        labels=labels_yearly_consumption,
        values=values_yearly_consumption,
        text=[f'<span style="font-weight:bold;">{value}</span>' for value in values_yearly_consumption_formatted],  # Apply CSS styling to make the numbers bold
        textinfo='percent+text',  # Display label, percentage, and value
        hoverinfo= 'label+text+percent',  # Display label, percentage, and value on hover
        hovertemplate='%{label}: %{text} kWh (%{percent})',  # Customize the hover template
        name='',  # Empty string for the trace name
        hole=0.2,  # Create a donut chart
        marker=dict(line=dict(color='#000000', width=1.5)), # Set the colors of the trace and the width of the border
        # pull=[0.2, 0.2, 0.2],
        # insidetextfont=dict(color='black', size=13, family='Arial'),  # Set the color and size of the labels outside the pie
        textfont=dict(color='black', size=16, family='Arial'),
        # textfont=dict(size=13, family='Arial',),
        # marker=dict(colors=['#FF0000', '#00FF00', '#0000FF'])  # Set the colors of the trace
    )

    # Create layout for the chart
    chart_layout = go.Layout(
        title='<b>Kreisdiagramm des jährlichen Stromverbrauchs der Liegenschaften (kWh)</b>',
        title_font=dict(size=17, color='black', family='Arial'),
        title_x=0.5,  # Center the title horizontally
        title_y=0.9,  # Adjust the vertical position of the title
        showlegend=True,
        legend=dict(orientation='h', x=0, y=-0.25),
        # legend=dict(font=dict(color='black'), orientation='h', x=0, y=-0.15),

        annotations=[
            dict(
                text=f'<b>Summe: {locale.format("%.0f", sum(values_yearly_consumption), grouping=True)} kWh (5/7/9/11/13 zusammen)</b>',
                x=0.5,
                y=-0.17,
                showarrow=False,
                font=dict(size=17, color='black', family='Arial'),
                align='center'
            ),
        ],
        paper_bgcolor='rgba(0,0,0,0)',  # Set the background of the entire chart to transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Set the background of the plot area to transparent  
        
    )


    # Create figure using the trace and layout
    figure = go.Figure(data=[trace], layout=chart_layout)

    # Add double lines below the annotation text
    figure.update_layout(
        shapes=[
            go.layout.Shape(
                type='line',
                x0=0.1,  # Adjust the position of the lines based on the x-axis
                y0=-0.16,
                x1=0.475,
                y1=-0.16,
                line=dict(color='black', width=1)
            ),
            go.layout.Shape(
                type='line',
                x0=0.1,  # Adjust the position of the lines based on the x-axis
                y0=-0.175,
                x1=0.475,
                y1=-0.175,
                line=dict(color='black', width=1)
            )
        ]
    )

    # set font color of legend
    figure.update_layout(legend_font_color="black") 
    # set font size of legend
    figure.update_layout(legend_font_size=13)


    # # Customize the CSS style for the chart
    # figure.update_layout(
    #     plotly_html_template='<style>.glabel {fill: black !important;}</style>{plotly_html}'
    # )
    return figure


@callback(
    Output('table1', 'children'),
    Input('dropdown', 'value')
)
def update_table1(option):
    options_data1 = {
        'option1': [
            ['Eigenverbrauch [%]', '40.1', '43.1'],
            ['Autarkiegrad [%]', '31.5', '33.9'],
            ['Energieertrag [MWh/Jahr]', '24.8', '24.8'],
            ['Installierte PV-Leistung [kWp]', '23.9', '23.9'],
            ['Spez. Ertrag [kWh/kWp]', 'E', 'F'],
        ],
        'option2': [
            ['Eigenverbrauch [%]', '5', '6'],
            ['Autarkiegrad [%]', 'X', 'Y'],
            ['Energieertrag [MWh/Jahr]', '24.8', '24.8'],
            ['Installierte PV-Leistung [kWp]', '1', '2'],
            ['Spez. Ertrag [kWh/kWp]', 'E', 'F'],
        ],
        'option3': [
            ['Eigenverbrauch [%]', 'A', 'B'],
            ['Autarkiegrad [%]', '!', '@'],
            ['Energieertrag [MWh/Jahr]', '24.8', '24.8'],
            ['Installierte PV-Leistung [kWp]', '5', '6'],
            ['Spez. Ertrag [kWh/kWp]', 'E', 'F'],
        ],
        'option4': [
            ['Eigenverbrauch [%]', '!', '@'],
            ['Autarkiegrad [%]', '5', '6'],
            ['Energieertrag [MWh/Jahr]', '24.8', '24.8'],
            ['Installierte PV-Leistung [kWp]', 'X', 'Y'],
            ['Spez. Ertrag [kWh/kWp]', 'E', 'F'],
        ]
    }
    
    data1 = options_data1.get(option, [])
    
    table_rows1 = [
        html.Tr([
            html.Th('Solextron Simulationsdaten', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Ohne Batterie', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Mit Batterie', style={'border': '2px solid black', 'padding': '8px'})
        ]),
        *[html.Tr([
            html.Td(
                cell,
                style={
                    'border': '1px solid black',
                    'padding': '8px',
                    'font-weight': 'bold' if col_idx > 0 else 'normal'
                }
            ) for col_idx, cell in enumerate(row)]
        ) for row in data1]
    ]
    return table_rows1


@callback(
    Output('table2', 'children'),
    [Input('dropdown', 'value'),
     Input('main_store', 'data')]
)
def update_table2(option, stored_main_data):

    #get the data from the main store for the costs simulation table
    costs_simulation_table = stored_main_data.get('costs_simulation_table', [])
    #get the data for the chosen option
    data2 = costs_simulation_table.get(option, [])
    #add the header to the data
    table_rows2 = [
        html.Tr([
            html.Th('Kosten aus der Simulation', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Ohne Batterie', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Mit Batterie', style={'border': '2px solid black', 'padding': '8px'})
        ]),
        *[html.Tr([
            html.Td(
                cell,
                style={
                    'border': '1px solid black',
                    'padding': '8px',
                    'font-weight': 'bold' if col_idx > 0 else 'normal'
                }
            ) for col_idx, cell in enumerate(row)]
        ) for row in data2]
    ]
    return table_rows2





# @callback(
#     Output('table', 'children'),
#     Input('dropdown', 'value')
# )
# def update_table(option):
#     # Define the common table data for all options
#     common_data = [['Eigenverbrauch [%]', '40.1', '43.1'],
#                    ['Autarkiegrad [%]', '31.5', '33.9'],
#                    ['Amortisationszeit [Jahre]', '9.1', '12.8'],
#                    ['MWh/Jahr', '24.8', '24.8'],
#                    ['kWp', '23.9', '23.9']]
    
#     if option == 'option1':
#         data = common_data
#     elif option == 'option2':
#         data = [[row[0], '1', '2'] for row in common_data]
#     elif option == 'option3':
#         data = [[row[0], 'X', 'Y'] for row in common_data]
#     else:
#         data = [[row[0], '!', '@'] for row in common_data]
    
#     table_rows = [
#         html.Tr([
#             html.Th('Solextron Daten', style={'border': '1px solid black', 'padding': '8px'}),
#             html.Th('Ohne Batterie', style={'border': '1px solid black', 'padding': '8px'}),
#             html.Th('Mit Batterie', style={'border': '1px solid black', 'padding': '8px'})
#         ]),
#         *[html.Tr([
#             html.Td(
#                 cell,
#                 style={
#                     'border': '1px solid black',
#                     'padding': '8px',
#                     'font-weight': 'bold' if col_idx > 0 else 'normal'
#                 }
#             ) for col_idx, cell in enumerate(row)]
#         ) for row in data]
#     ]
#     return table_rows

