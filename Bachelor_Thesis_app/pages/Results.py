import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')


dash.register_page(__name__, path='/', name='Results', order=1) # '/' is the home page fo this app

# Load data later from the Excel file from Solextron
labels_yearly_consumption = ['Riedgrabenstrasse 5', 'Riedgrabenstrasse 7/9/11','Riedgrabenstrasse 13']
values_yearly_consumption = [35300, 13100, 42000]


# Format the values with the thousands separator
values_yearly_consumption_formatted = [locale.format('%.0f', value, grouping=True) for value in values_yearly_consumption]

# Create pie chart trace
trace = go.Pie(
    labels=labels_yearly_consumption,
    values=values_yearly_consumption,
    text=values_yearly_consumption_formatted,  # Use the formatted values as labels
    textinfo='percent+text',  # Display label, percentage, and value
    hoverinfo= 'label+text+percent',  # Display label, percentage, and value on hover
    textfont=dict(size=13, family='Arial'),
)




# Create layout for the chart
chart_layout = go.Layout(
    title='Kreisdiagramm des jährlichen Stromverbrauchs der Liegenschaften (kWh)',
    title_font=dict(size=20, color='black', family='Arial'),
    title_x=0.5,  # Center the title horizontally
    title_y=0.9,  # Adjust the vertical position of the title
    showlegend=True,
    legend=dict(font=dict(size=15), orientation='h', x=0, y=-0.15),
    annotations=[
        dict(
            text=f'<b>Summe: {locale.format("%.0f", sum(values_yearly_consumption), grouping=True)} kWh</b>',
            x=0.5,
            y=-0.15,
            showarrow=False,
            font=dict(size=15),
            align='center'
        )
    ]
)


# Create figure using the trace and layout
figure = go.Figure(data=[trace], layout=chart_layout)


# Define the layout of the Dash application
layout = html.Div(children=[
    html.H1(children='Kennzahlen der Liegenschaften',
            style={'text-align': 'center', 'font-size': '32px'}),
    html.Div([
        dcc.Graph(id='pie-chart', figure=figure)
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '20px'}),
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
            id='table-container',
            children=[
                html.Table(
                    id='table',
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
                )
            ],
            style={'overflow': 'auto'}
        )
    ], style={'width': '50%', 'display': 'inline-block'})
])


@callback(
    Output('table', 'children'),
    Input('dropdown', 'value')
)
def update_table(option):
    options_data = {
        'option1': [
            ['Eigenverbrauch [%]', '40.1', '43.1'],
            ['Autarkiegrad [%]', '31.5', '33.9'],
            ['Amortisationszeit [Jahre]', '9.1', '12.8'],
            ['MWh/Jahr', '24.8', '24.8'],
            ['kWp', '23.9', '23.9']
        ],
        'option2': [
            ['Eigenverbrauch [%]', '5', '6'],
            ['Autarkiegrad [%]', 'X', 'Y'],
            ['Amortisationszeit [Jahre]', '!', '@'],
            ['MWh/Jahr', 'A', 'B'],
            ['kWp', '1', '2']
        ],
        'option3': [
            ['Eigenverbrauch [%]', 'A', 'B'],
            ['Autarkiegrad [%]', '!', '@'],
            ['Amortisationszeit [Jahre]', '1', '2'],
            ['MWh/Jahr', 'X', 'Y'],
            ['kWp', '5', '6']
        ],
        'option4': [
            ['Eigenverbrauch [%]', '!', '@'],
            ['Autarkiegrad [%]', '5', '6'],
            ['Amortisationszeit [Jahre]', 'A', 'B'],
            ['MWh/Jahr', '1', '2'],
            ['kWp', 'X', 'Y']
        ]
    }
    
    data = options_data.get(option, [])
    
    table_rows = [
        html.Tr([
            html.Th('Solextron Simulationsdaten', style={'border': '1px solid black', 'padding': '8px'}),
            html.Th('Ohne Batterie', style={'border': '1px solid black', 'padding': '8px'}),
            html.Th('Mit Batterie', style={'border': '1px solid black', 'padding': '8px'})
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
        ) for row in data]
    ]
    return table_rows





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

