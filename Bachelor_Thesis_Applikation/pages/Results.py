import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')


dash.register_page(__name__, path='/', name='Resultate', order=1) # '/' is the home page fo this app

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
    hovertemplate='%{label}: %{text} kWh (%{percent})',  # Customize the hover template
    name='',  # Empty string for the trace name
    # insidetextfont=dict(color='black', size=13, family='Arial'),  # Set the color and size of the labels outside the pie
    textfont=dict(color='black', size=13, family='Arial'),
    # textfont=dict(size=13, family='Arial',),
    # marker=dict(colors=['#FF0000', '#00FF00', '#0000FF'])  # Set the colors of the trace
)




# Create layout for the chart
chart_layout = go.Layout(
    title='<b>Kreisdiagramm des jährlichen Stromverbrauchs der Liegenschaften (kWh)</b>',
    title_font=dict(size=18, color='black', family='Arial'),
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
            font=dict(size=17, color='black', family='Arial'),
            align='center'
        )
    ],
    paper_bgcolor='rgba(0,0,0,0)',  # Set the background of the entire chart to transparent
    plot_bgcolor='rgba(0,0,0,0)',  # Set the background of the plot area to transparent
    # outsidetextfont=dict(color='black', size=13, family='Arial')  # Set the color and size of the labels outside the pie
)


# Create figure using the trace and layout
figure = go.Figure(data=[trace], layout=chart_layout)

# # Customize the CSS style for the chart
# figure.update_layout(
#     plotly_html_template='<style>.glabel {fill: black !important;}</style>{plotly_html}'
# )


# Define the layout of the Dash application
layout = html.Div(children=[
    html.H1(children='Kennzahlen der Liegenschaften',
            style={'text-align': 'center', 'font-size': '35px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
    html.Div([
        dcc.Graph(id='pie-chart', figure=figure)
    ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '20px', 'margin-right': '20px','background-color': 'transparent'}),
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
            style={'color': 'black','font-weight': 'bold', 'font-size': '16px','width': '270px', 'margin-right': '20px', 'margin-top': '30px','background-color': 'transparent'},

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
    ], style={'width': '50%', 'display': 'inline-block', 'background-color': 'transparent'})
]),


@callback(
    Output('table1', 'children'),
    Input('dropdown', 'value')
)
def update_table1(option):
    options_data1 = {
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
    
    data1 = options_data1.get(option, [])
    
    table_rows1 = [
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
        ) for row in data1]
    ]
    return table_rows1


@callback(
    Output('table2', 'children'),
    Input('dropdown', 'value')
)
def update_table2(option):
    options_data2 = {
        'option1': [
            ['CAPEX [CHF]', 'A', 'B'],
            ['CAPEX [CHF] mit EV', 'C', 'D'],
            ['kWh/kWp', 'E', 'F'],
            ['Stromkosten [CHF/kWh]', 'G', 'H'],
            ['Table 2 - Data 5', 'I', 'J']
        ],
        'option2': [
            ['CAPEX [CHF]', '1', '2'],
            ['CAPEX [CHF] mit EV', '3', '4'],
            ['kWh/kWp', '5', '6'],
            ['Stromkosten [CHF/kWh]', '7', '8'],
            ['Table 2 - Data 5', '9', '10']
        ],
        'option3': [
            ['CAPEX [CHF]', 'X', 'Y'],
            ['CAPEX [CHF] mit EV', 'Z', 'A'],
            ['kWh/kWp', 'B', 'C'],
            ['Stromkosten [CHF/kWh]', 'D', 'E'],
            ['Table 2 - Data 5', 'F', 'G']
        ],
        'option4': [
            ['CAPEX [CHF]', '!', '@'],
            ['CAPEX [CHF] mit EV', '#', '$'],
            ['kWh/kWp', '%', '^'],
            ['Stromkosten [CHF/kWh]', '&', '*'],
            ['Table 2 - Data 5', '(', ')']
        ]
    }

    data2 = options_data2.get(option, [])

    table_rows2 = [
        html.Tr([
            html.Th('Kosten aus der Simulation', style={'border': '1px solid black', 'padding': '8px'}),
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

