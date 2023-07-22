import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')

#register the page Resultate
dash.register_page(__name__, path='/', name='Resultate', order=1) # '/' is the home page for this app

# Load data later from the Excel file from Solextron
labels_yearly_consumption = ['<b>Riedgrabenstrasse 5</b>', '<b>Riedgrabenstrasse 7/9/11</b>','<b>Riedgrabenstrasse 13</b>']
values_yearly_consumption = [35300, 13100, 42000]

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
            x0=0.18,  # Adjust the position of the lines based on the x-axis
            y0=-0.16,
            x1=0.475,
            y1=-0.16,
            line=dict(color='black', width=1)
        ),
        go.layout.Shape(
            type='line',
            x0=0.18,  # Adjust the position of the lines based on the x-axis
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


# Define the layout of the Dash application
layout = html.Div(children=[
    html.H1(children='Kennzahlen der Liegenschaften', className='pages-header'),
    html.P(children='Auf dieser Seite kann der Nutzer die Kennzahlen der Liegenschaften anschauen.', className= 'subheader'),
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
            style={'color': 'black','font-weight': 'bold', 'font-size': '16px','width': '270px', 'margin-right': '20px', 'margin-top': '30px',
                #    'background-color': 'rgba(255, 255, 255, 0.8)'  # Set the background color to opaque white
                   'background-color': 'transparent'
                },

        ),
        # html.Script(
        #     """
        #     document.getElementById('dropdown').addEventListener('click', function() {
        #         this.style.backgroundColor = 'black';
        #     });
        #     """
        # ),
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
    Input('dropdown', 'value')
)
def update_table2(option):
    options_data2 = {
        'option1': [
            ['Ivestitionskosten/CAPEX [CHF]', 'A', 'B'],
            ['CAPEX mit Einmalvergütung [CHF]', 'C', 'D'],
            ['Spez. Investitionskosten (CAPEX/kWP) [CHF/kWp]', 'E', 'F'],
            ['Betriebskosten/OPEX [CHF/Jahr]', 'I', 'J'],
            ['Amortisationszeit [Jahre]', '9.1', '12.8'],
            ['Stromkosten [CHF/kWh]', 'G', 'H'],
            
        ],
        'option2': [
            ['Ivestitionskosten/CAPEX [CHF]', '1', '2'],
            ['CAPEX mit Einmalvergütung [CHF]', '3', '4'],
            ['Spez. Investitionskosten (CAPEX/kWP) [CHF/kWp]', 'E', 'F'],
            ['Betriebskosten/OPEX [CHF/Jahr]', 'I', 'J'],
            ['Amortisationszeit [Jahre]', '9.1', '12.8'],
            ['Stromkosten [CHF/kWh]', '9', '10']
        ],
        'option3': [
            ['Ivestitionskosten/CAPEX [CHF]', 'X', 'Y'],
            ['CAPEX mit Einmalvergütung [CHF]', 'Z', 'A'],
            ['Spez. Investitionskosten (CAPEX/kWP) [CHF/kWp]', 'E', 'F'],
            ['Betriebskosten/OPEX [CHF/Jahr]', 'I', 'J'],
            ['Amortisationszeit [Jahre]', '9.1', '12.8'],
            ['Stromkosten [CHF/kWh]', 'F', 'G']
        ],
        'option4': [
            ['Ivestitionskosten/CAPEX [CHF]', '!', '@'],
            ['CAPEX mit Einmalvergütung [CHF]', '#', '$'],
            ['Spez. Investitionskosten (CAPEX/kWP) [CHF/kWp]', 'E', 'F'],
            ['Betriebskosten/OPEX [CHF/Jahr]', 'I', 'J'],
            ['Amortisationszeit [Jahre]', '9.1', '12.8'],
            ['Stromkosten [CHF/kWh]', '(', ')']
        ]
    }

    data2 = options_data2.get(option, [])

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

