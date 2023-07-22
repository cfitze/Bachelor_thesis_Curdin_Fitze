import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')

dash.register_page(__name__, path='/kosten', name='Kosten berechnen', order=4) # is a subpage of the home page

# Define the layout for Results_Compare page
layout = html.Div(
    [
        html.Div(
            [
                html.H1("Kostenberechnung", className="pages-header"),
                html.P("Auf dieser Seite kann der Nutzer die Kosten von zwei verschiedenen Varianten vergleichen.", className= 'subheader'),
                html.P("NS = Niederspannung, HT = Hochtarif, NT = Niedertarif",className= 'regular-text', style={"text-align": "left"}),
                html.P("Leistungspreis = Als Monatsmaximum gilt die während einer 15-minütigen Messperiode gemittelte, höchste Leistung. Für die Ermittlung des Monatsmaximums werden nur Leistungsbezüge während der Hochtarifzeit berücksichtigt. Gilt pro kW des Monatsmaximums, pro Monat",className= 'regular-text', style={"text-align": "left"}),
            ],
            style={"margin": "auto", "width": "70%"}
        ),  # Centered text
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.P("Plotten der Kosten der Liegenschaften:",className= 'plot-title', style={"text-align": "left", "margin-left": "5%", "margin-right": "5%"}),
                            dcc.Loading(
                                id="loading",
                                type="graph",
                                style={'marginTop': '80px'},  # Adjust the marginTop value as desired
                                children=[
                                    # html.Div(
                                    #     className="loading-text",
                                    #     children="Berechnungen werden ausgeführt",
                                    #     style={'text-align': 'center', 'font-weight': 'bold'}
                                    # ),
                                    html.Div(id='cost-graphs')
                                ]
                            ),
                            # html.Img(src="assets/el_verschaltung/Trafo_el_Verschaltung_ist_Zustand_Eigenstrom_x.svg", style={"display": "block", "margin": "auto", "width": "85%", "margin-top" : "5%", "opacity": 0.95}),
                            html.P("Aufzeigen der Verbrauchsdaten der einzelnen Verbraucher --> Später mit Kosten verlinken.", style={'font-size': '16px', 'font-weight': 'normal', 'fontFamily': 'Arial', "text-align": "left", "margin-top": "5%", "margin-left": "5%", "margin-right": "5%"})
                        ]
                    ),
                    width=7,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.P("Wählen Sie den Bezugscharakter aus:",className= 'table-title', style={"text-align": "left", "margin-left": "5%", "margin-right": "5%"}),
                            dcc.Dropdown(
                                id='dropdown-el-cost',
                                options=[
                                    {'label': 'Bezugscharakter Energie „Klassik"', 'value': 'option1'},
                                    {'label': 'Bezugscharakter Netz „Industrie NS 50 bis 100 MWh“', 'value': 'option2'},
                                    {'label': 'Bezugscharakter Netz „Industrie NS über 100 MWh“', 'value': 'option3'},
                                    {'label': 'Eigenstrom X', 'value': 'option4'},
                                    {'label': 'ZEV', 'value': 'option5'}
                                ],
                                value='option1',
                                clearable=False,  # This will disable the clearable 'x' option
                                style={'color': 'black', 'font-weight': 'bold', 'font-size': '16px', 'width': '450px', 'margin-right': '20px', 'margin-top': '20px', 'background-color': 'transparent'},
                            ),
                            html.Div(
                                id='table-container',
                                children=[
                                    html.Table(
                                        id='table-el-cost',
                                        style={
                                            'border': '1px solid black',
                                            'border-collapse': 'collapse',
                                            'width': '100%',
                                            'margin': 'auto',
                                            'margin-top': '5px'
                                        },
                                        children=[
                                            html.Tr(
                                                [
                                                    html.Th('Column 1', style={'border': '1px solid black', 'padding': '8px'}),
                                                    html.Th('Column 2', style={'border': '1px solid black', 'padding': '8px'}),
                                                    html.Th('Column 3', style={'border': '1px solid black', 'padding': '8px'})
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                style={'overflow': 'auto', 'margin-right': '1%'}
                            )

                        ],
                        style={'width': '100%', 'display': 'inline-block', 'background-color': 'transparent'}
                    ),
                    width=5,
                ),
            ]
        ),
    ]
)

@callback(
    Output('table-el-cost', 'children'),
    Input('dropdown-el-cost', 'value')
)
def update_table1(option):
    options_data_el_cost = {
        'option1': [
            ['Grundpreis', '2.69 Fr./Mt.', 'inkl. 7.7% MwSt.'],
            ['Verbrauchspreise HT', '17.39 Rp./kWh.', 'inkl. 7.7% MwSt.'],
            ['Verbrauchspreise NT', '17.39 Rp./kWh.', 'inkl. 7.7% MwSt.'],
            ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
            ['Tarifzeiten NT', 'übrige Zeit', '']
        ],
        'option2': [
            ['Grundpreis', '5.5 Fr./Mt.', 'exkl. 7.7% MwSt.'],
            ['Arbeitspreise HT', '5.17 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Arbeitspreise NT', '3.6 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
            ['Tarifzeiten NT', 'übrige Zeit', ''],
            ['Leistungspreis', '5.1 Fr./kWh' , '(exkl. 7.7% MWST)']
        ],
        'option3': [
            ['Grundpreis', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
            ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
            ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
            ['Tarifzeiten NT', 'übrige Zeit', ''],
            ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)']
        ],
        'option4': [
            ['Grundpreis', '!', 'Fr./Mt. (ekl. MWST)'],
            ['Arbeitspreise', '5', '6'],
            ['Amortisationszeit [Jahre]', 'A', 'B'],
            ['MWh/Jahr', '1', '2'],
            ['kWp', 'X', 'Y']
        ]
    }
    
    data_el_cost = options_data_el_cost.get(option, [])
    
    table_rows_el_cost = [
        html.Tr([
            html.Th('Preisinformation', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Kosten', style={'border': '2px solid black', 'padding': '8px'}),
            html.Th('Information', style={'border': '2px solid black', 'padding': '8px'})
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
        ) for row in data_el_cost]
    ]
    return table_rows_el_cost




# Define the callbacks
@callback(
    dash.dependencies.Output('cost-graphs', 'children'),
    dash.dependencies.Input('main_store', 'data')
)
def generate_cost_plots(main_store_data):

    # Create a DataFrame from the data stored in the main_store
    main_store_data_cost_df = pd.DataFrame(main_store_data['data_frames']).reset_index(drop=True)

    # Create a list to hold the traces for each array of data
    traces = []

    # Generate x-axis array based on the length of the first array
    x_axis = list(range(1, len(main_store_data_cost_df)+1))

    # Iterate through the columns of the DataFrame
    for col in main_store_data_cost_df.columns:
        # Extract the numeric values from the dictionary and create a separate list
        y_values = main_store_data_cost_df[col]
        trace = go.Scattergl(x=x_axis, y=y_values, mode='lines+markers', name=f'{col} Data', marker=dict(size=0.5))
        traces.append(trace)

    # Create the plot using Plotly
    cost_plot = go.Figure(data=traces)
    cost_plot.update_layout(
        title=dict(
            text="Verbrauch/Kosten plotten --> DateTime einfügen",
            x=0.5,  # Set the title's horizontal position to the middle (0.5)
            y=0.95,  # Set the title's vertical position closer to the top
            font=dict(
                family="Arial",  # Specify the font family
                size=20,  # Set the title font size to 24
                color="black",  # Set the title font color to blue
            ),
            # weight="bold",  # Set the title font weight to bold
            # style="italic",  # Set the title font style to italic
        ),
        xaxis_title="Zeit [15min Abschnitte]",
        yaxis_title="Verbrauchsdaten [kWh]",
        legend=dict(
            x=0, y=1.2, bgcolor='rgba(255, 255, 255, 0.5)',  # Make the legend background opaque
            font=dict(size=10),  # Change the legend text size to 14
            bordercolor='rgba(100, 100, 200, 0.2)',  # Make the legend border transparent
            borderwidth=2,  # Make the legend border width 1
        ),
        plot_bgcolor='rgba(255, 255, 255, 0.3)',  # Set the plot background to 20% opaque white
        paper_bgcolor='rgba(255, 255, 255, 0.1)',  # Set the paper (outside plot) background to 20% opaque white
        margin=dict(l=25, r=10, t=20, b=15)  # Adjust the margins
    )
    # Return the plot as the children of the 'cost-graphs' div
    return dcc.Graph(figure=cost_plot)


    # # Create a trace for each array of data
    # for i in range(1, 5):  # Replace 5 with the number of arrays you have (e.g., 4)
    #     array_key = f'array_{i}'
    #     if array_key in main_store_data_cost:
    #         trace = go.Scatter(x=x_axis, y=main_store_data_cost[array_key], mode='lines+markers', name=f'Data {i}')
    #         traces.append(trace)

    # # Create a trace for each array of data
    # for i, col_name in enumerate(main_store_data_cost_df.columns):
    #     trace = go.Scatter(x=x_axis, y=main_store_data_cost[col_name], mode='lines+markers', name=f'Data {i+1}')
    #     traces.append(trace)


    # datetime_column = pd.to_datetime([i['DateTime'] for i in stored_data['datetime_column']])
    # start_date, end_date = [pd.to_datetime(date, unit='s') for date in selected_date_range]  # convert timestamp to datetime
    # initial_data_without_datetime = pd.DataFrame(stored_data['initial_data_without_datetime'])

    # # Generate combined plot
    # combined_figure = create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, selected_columns, color_list, plot_name = plot_name_combined)
    # combined_plot = dcc.Graph(
    #         id='combined-bar-plot',
    #         figure=combined_figure
    # )