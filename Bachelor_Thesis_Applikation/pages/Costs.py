import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import locale
import calendar

# Set the locale
locale.setlocale(locale.LC_ALL, 'de_CH')

dash.register_page(__name__, path='/kosten', name='Kosten berechnen', order=4) # is a subpage of the home page

#set the parameters for the costs
inflation_el_cost = 1.05 # inflation of the electrical costs by 5% per year
operating_costs = 1.01 # operating costs are 1% of the investment costs
taxes_deduction = 1 #the deduction of the taxes is 100% of the investment costs
financial_lifetime_produkt = 25 #the financial lifetime of the product is 25 years
# list of colors for the plots
colors_el_cost = ['#1F77B4', '#9467BD', '#2CA02C', '#D62728']
#name of the options in the dictionary for the electrical costs for the chosen character
# option_list = ['option1', 'option1', 'option1', 'option1'] #option1 = 'Bezugscharakter Energie „Klassik"', option2 = 'Bezugscharakter Netz „Industrie NS 50 bis 100 MWh“', option3 = 'Bezugscharakter Netz „Industrie NS über 100 MWh“', option4 = 'Eigenstrom X', option5 = 'ZEV mit „Industrie NS über 100 MWh“ '

cost_plot_names = ['Riedgrabenstrasse 5', 'Riedgrabenstrasse 7/9/11', 'Riedgrabenstrasse 13', 'Riedgrabenstrasse 5/7/9/11/13'] #name of the plots for the costs

property_el_cost_character = {
''

}

# Define the layout for Results_Compare page
layout = html.Div(
    [
        html.Div(
            [
                html.H1("Kostenberechnung", className="pages-header"),
                html.P("Auf dieser Seite kann der Nutzer die Kosten von zwei verschiedenen Varianten vergleichen.", className= 'subheader',style={"margin-bottom:": "15px"}),
            ],
            style={"margin": "auto", "width": "80%", 'margin-bottom': '15px'}
        ),  # Centered text
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.P("Wählen Sie die gewünschte Liegenschaft aus:", className = 'subheader', style={"text-align": "left"}),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='dropdown-costs',
                                            options=[
                                                {"label": "Riedgrabenstrasse 5", "value": "0"},
                                                {"label": "Riedgrabenstrasse 7/9/11", "value": "1"},
                                                {"label": "Riedgrabenstrasse 13", "value": "2"},
                                                {"label": "Riedgrabenstrasse 5/7/9/11/13", "value": "3"},
                                            ],
                                            value="0",
                                            clearable=False,
                                            style={
                                                "color": "black",
                                                "font-weight": "bold",
                                                "font-size": "16px",
                                                "width": "270px",
                                                "margin-right": "20px",
                                                "margin-top": "12px",
                                                "margin-bottom": "15px",
                                                "background-color": "transparent",
                                            },
                                        ),
                                        width=4  # Adjust the width as needed
                                    ),
                                    dbc.Col(
                                        dbc.Button(id='button-start', children= "Berechnung starten", class_name= 'button-standard'),
                                        width=2  # Adjust the width as needed
                                    ),
                                    dbc.Col(
                                        dbc.Button(id='button-cancel', children= "Berechnung abbrechen", class_name= 'button-standard'),
                                        width=2  # Adjust the width as needed
                                    ),
                                ],
                                style={"margin-bottom": "8px"}  # Adjust the margin as needed
                            ),
                            html.P("Plotten der Kosten und des Verbrauchs der Liegenschaften:", className = 'subheader', style={"text-align": "left"}),
                            dcc.Loading(
                                id="loading1",
                                type="graph",
                                style={'marginTop': '80px'},  # Adjust the marginTop value as desired
                                children=[
                                    # html.Div(
                                    #     className="loading-text",
                                    #     children="Berechnungen werden ausgeführt",
                                    #     style={'text-align': 'center', 'font-weight': 'bold'}
                                    # ),
                                    html.Div(id='cost-graphs'),
                                    # html.P("Aufzeigen der Verbrauchsdaten der einzelnen Verbraucher --> Später mit Kosten verlinken.",className= 'regular-text', style={"text-align": "left"}),
                                ]                            
                            ),
                            dcc.Loading(
                                id="loading2",
                                type="graph",
                                style={'marginTop': '80px'},  # Adjust the marginTop value as desired
                                children=[
                                    # html.Div(
                                    #     className="loading-text",
                                    #     children="Berechnungen werden ausgeführt",
                                    #     style={'text-align': 'center', 'font-weight': 'bold'}
                                    # ),
                                    html.Div(id='usage-graphs'),
                                    # html.P("Aufzeigen der Verbrauchsdaten der einzelnen Verbraucher --> Später mit Kosten verlinken.",className= 'regular-text', style={"text-align": "left"}),
                                ]
                            # html.Img(src="assets/el_verschaltung/Trafo_el_Verschaltung_ist_Zustand_Eigenstrom_x.svg", style={"display": "block", "margin": "auto", "width": "85%", "margin-top" : "5%", "opacity": 0.95}),
                            
                            ),
                        ]
                    ),
                    width=8,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.P("Liste der Bezugscharakter:",className= 'subheader', style={"text-align": "left"}),
                            dcc.Dropdown(
                                id='dropdown-reference-character',
                                options=[
                                    {'label': 'Bezugscharakter Energie „Klassik"', 'value': 'option1'},
                                    {'label': 'Bezugscharakter Netz „Industrie NS 50 bis 100 MWh“', 'value': 'option2'},
                                    {'label': 'Bezugscharakter Netz „Industrie NS über 100 MWh“', 'value': 'option3'},
                                    {'label': 'Eigenstrom X', 'value': 'option4'},
                                    {'label': 'ZEV mit „Industrie NS über 100 MWh“ ', 'value': 'option5'}
                                ],
                                value='option1',
                                clearable=False,  # This will disable the clearable 'x' option
                                style={'color': 'black', 'font-weight': 'bold', 'font-size': '16px', 'width': '450px', 'margin-right': '20px', 'margin-top': '12px', 'background-color': 'transparent'},
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
                    width=4,
                ),
            ]
        ),
        html.Br(),
        html.P("NS = Niederspannung, HT = Hochtarif, NT = Niedertarif",className= 'side-note-text', style={"text-align": "left"}),
        html.P("Leistungspreis = Als Monatsmaximum gilt die während einer 15-minütigen Messperiode gemittelte, höchste Leistung. Für die Ermittlung des Monatsmaximums werden nur Leistungsbezüge während der Hochtarifzeit berücksichtigt. Gilt pro kW des Monatsmaximums, pro Monat und wird am letzten Tag des Monates zum dynamischen Preis dazu addiert.",className= 'side-note-text', style={"text-align": "left"}),
        html.P("Für die Bestimmung des Bezugscharakter (BC*) wird die Summe der kWh/Jahr genommen. ",className= 'side-note-text', style={"text-align": "left"}),
        html.P(f"Laut Annahme ist die Inflation pro Jahr der Strompreise ist auf {inflation_el_cost*100-100} % angesetzt (hoch angesetzt). Die Inflation der Rückspeisungsvergütung hat den gleichen Wert.",className= 'side-note-text', style={"text-align": "left"}),
        html.P(f"Die Betriebkosten wurden auf {operating_costs*100-100} % der Investitionskosten (CAPEX) angesetzt. Den Abzug von den Steuern ist in den meisten Kantonen bei {taxes_deduction*100} % des CAPEX angesetzt.",className= 'side-note-text', style={"text-align": "left"}),
        html.P(f"Die Lebensdauer der Anlage wurde auf {financial_lifetime_produkt} Jahre angesetzt.",className= 'side-note-text', style={"text-align": "left"}),
    ]
)


@callback(
    Output('table-el-cost', 'children'),
    [Input('dropdown-reference-character', 'value'),
    Input('main_store', 'data')],
    background=True,
    cache_by=True,
    running=[
        (Output("dropdown-costs", "disabled"), True, False),
    ],
)
def update_table1(option, stored_data_el_cost_table):

    #get the data from the table from the main_store
    options_data_el_cost = stored_data_el_cost_table['options_data_el_cost_table']

    #get the data for the selected option
    data_el_cost = options_data_el_cost.get(option, [])
    
    # Create the table rows using the data from the table from the main_store
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

#call the function to calculate the electrical costs for the chosen character, is defined outside of the callback to be able to use it in the other callback
def calc_el_cost_character(option_dropdown_el_cost, name_chosen_column, y_values_chosen_column, datetime_column_costs, datetime_column_costs_hours ,data_el_cost_dict):

    # Convert the datetime_column_costs to pandas datetime objects with the format '%d-%m-%Y %H:%M'
    datetime_column_costs_pd = pd.to_datetime(datetime_column_costs, format='%d-%m-%Y %H:%M')
    # Calculate the sum of y_values_chosen_column
    sum_y_values_chosen_column = (y_values_chosen_column.sum()/4) #divide by 4 to get the sum of the kWh per year, since the data is in 15min steps
    # Define a dictionary to map the sum to the corresponding option value based on ranges
    sum_option_character = {
        (0, 50000): 'option1',
        (50000, 100000): 'option2',
        (100000, float('inf')): 'option3',  # Use float('inf') for the range above 100000 kWh
        # Add more range-value mappings here based on your requirements
        # For example:
        # (lower_limit, upper_limit): 'option_value',
        # (, 150000): 'option4',
        # (150000, float('inf')): 'option5',
    }
    try:
        # Find the corresponding option value based on the sum
        selected_option = next(value for (lower, upper), value in sum_option_character.items() if lower <= sum_y_values_chosen_column < upper)
    except StopIteration:
        # Handle the case when no match is found (optional)
        selected_option = None
    #get the dictionary for the chosen character from the dropdown option
    data_el_cost_dict_selected = data_el_cost_dict[selected_option]
    #get the keys from the dictionary for the chosen character from the dropdown option
    key_dict_secleceted_list = list(data_el_cost_dict_selected.keys())
    #get the keys from the keys list
    key_basic_price_dict_selected, key_el_cost_HT_dict_selected, key_el_cost_NT_dict_selected, key_el_time_HT_dict_selected, key_el_time_NT_dict_selected  = key_dict_secleceted_list[0],key_dict_secleceted_list[1],key_dict_secleceted_list[2],key_dict_secleceted_list[3],key_dict_secleceted_list[4]
    if selected_option != 'option1': #if the selected option is not the first option, then the SDL price is also included
        key_SDL_price_dict_selected = key_dict_secleceted_list[5]
        value_SDL_price_dict_selected, factor_SDL_price_dict_selected = float(data_el_cost_dict_selected[key_SDL_price_dict_selected]['value']), data_el_cost_dict_selected[key_SDL_price_dict_selected]['factor_el_calc']
    
    #get the values and mathematical factors for the electrical host for the high tariff, low tariff and high tariff time; low tariff time equals the rest of the time
    value_basic_price_dict_selected, factor_basic_price_dict_selected = float(data_el_cost_dict_selected[key_basic_price_dict_selected]['value']), data_el_cost_dict_selected[key_basic_price_dict_selected]['factor_el_calc']
    value_el_cost_HT_dict_selected, factor_el_cost_HT_dict_selected = float(data_el_cost_dict_selected[key_el_cost_HT_dict_selected]['value']), data_el_cost_dict_selected[key_el_cost_HT_dict_selected]['factor_el_calc']
    value_el_cost_NT_dict_selected, factor_el_cost_NT_dict_selected = float(data_el_cost_dict_selected[key_el_cost_NT_dict_selected]['value']), data_el_cost_dict_selected[key_el_cost_NT_dict_selected]['factor_el_calc']
    value_el_time_HT_dict_selected, factor_el_time_HT_dict_selected = data_el_cost_dict_selected[key_el_time_HT_dict_selected]['value'], data_el_cost_dict_selected[key_el_time_HT_dict_selected]['factor_el_calc']
    #get the start and end day for the high tariff time during the week
    start_weekday_el_time_HT_dict_selected, end_weekday_el_time_HT_dict_selected = value_el_time_HT_dict_selected[0].split('-')
    #get the start day for the high tariff time during the weekend
    weekend_el_time_HT_dict_selected = value_el_time_HT_dict_selected[1]
    #get the start and end time for the high tariff time during the week
    start_time_weekday_el_time_HT_dict_selected, end_time_weekday_el_time_HT_dict_selected = factor_el_time_HT_dict_selected[0][0], factor_el_time_HT_dict_selected[0][1]
    #get the start and end time for the high tariff time during the weekend
    start_time_weekend_el_time_HT_dict_selected, end_time_weekend_el_time_HT_dict_selected = factor_el_time_HT_dict_selected[1][0], factor_el_time_HT_dict_selected[1][1]

    # Sample list of German day names
    german_days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    # Initialize lists to store cumulative and non-cumulative y values
    y_values_cumulative = []
    y_values_non_cumulative = []
    y_values_cum_sum = 0  # Initialize the cumulative sum variable

    # Check if the selected option is the first option
    if selected_option == 'option1':
        # Iterate through the index and datetime values in datetime_column_costs_pd using enumerate
        for index, dt in enumerate(datetime_column_costs_pd):

            # Check if the day is within the high tariff time range
            if dt.weekday() >= german_days.index(start_weekday_el_time_HT_dict_selected) and dt.weekday() <= german_days.index(end_weekday_el_time_HT_dict_selected):
                # Check if the time is within the high tariff time range for weekdays
                if dt.time() >= pd.to_datetime(start_time_weekday_el_time_HT_dict_selected).time() and dt.time() <= pd.to_datetime(end_time_weekday_el_time_HT_dict_selected).time():
                    # Apply high tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_HT_dict_selected * factor_el_cost_HT_dict_selected
                else:
                    # Apply low tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            # Check if the day is a weekend day
            elif dt.weekday() == german_days.index(weekend_el_time_HT_dict_selected):
                # Check if the time is within the high tariff time range for weekends
                if dt.time() >= pd.to_datetime(start_time_weekend_el_time_HT_dict_selected).time() and dt.time() <= pd.to_datetime(end_time_weekend_el_time_HT_dict_selected).time():
                    # Apply high tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_HT_dict_selected * factor_el_cost_HT_dict_selected
                else:
                    # Apply low tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            else:
                # Apply low tariff calculation for other days
                y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            # if dt.month != dt.shift(1).month and dt.day == calendar.monthrange(dt.year, dt.month)[1] and dt.hour == 23: #because the datetime_column_costs_pd from Solextron stops at the date 31.12.2023 23:00, so the last hour can not be used to check if it is the last day of the month
            if dt.day == calendar.monthrange(dt.year, dt.month)[1] and dt.hour == 23:    
                # Calculate the cost for the basic price and add it to the cumulative sum for the remaining days
                cost_remaining_days = value_basic_price_dict_selected * factor_basic_price_dict_selected
                y_values_cum_sum += cost_remaining_days

                # Append the basic price cost to the cumulative and non-cumulative y values lists
                y_values_cumulative[-1] = y_values_cum_sum
                y_values_non_cumulative[-1] = cost_remaining_days
                # y_values_cumulative.append(y_values_cum_sum)
                # y_values_non_cumulative.append(cost_remaining_days)

            # Update the cumulative sum variable
            y_values_cum_sum += y_value
            # Append the cumulative and non-cumulative y values to their respective lists
            y_values_cumulative.append(y_values_cum_sum)
            y_values_non_cumulative.append(y_value)

    else: #if the selected option is not the first option, then the SDL and performance price is also included
        # Iterate through the index and datetime values in datetime_column_costs_pd using enumerate
        for index, dt in enumerate(datetime_column_costs_pd):

            # Check if the day is within the high tariff time range
            if dt.weekday() >= german_days.index(start_weekday_el_time_HT_dict_selected) and dt.weekday() <= german_days.index(end_weekday_el_time_HT_dict_selected):
                # Check if the time is within the high tariff time range for weekdays
                if dt.time() >= pd.to_datetime(start_time_weekday_el_time_HT_dict_selected).time() and dt.time() <= pd.to_datetime(end_time_weekday_el_time_HT_dict_selected).time():
                    # Apply high tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_HT_dict_selected * factor_el_cost_HT_dict_selected
                else:
                    # Apply low tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            # Check if the day is a weekend day
            elif dt.weekday() == german_days.index(weekend_el_time_HT_dict_selected):
                # Check if the time is within the high tariff time range for weekends
                if dt.time() >= pd.to_datetime(start_time_weekend_el_time_HT_dict_selected).time() and dt.time() <= pd.to_datetime(end_time_weekend_el_time_HT_dict_selected).time():
                    # Apply high tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_HT_dict_selected * factor_el_cost_HT_dict_selected
                else:
                    # Apply low tariff calculation
                    y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            else:
                # Apply low tariff calculation for other days
                y_value = y_values_chosen_column[index] * value_el_cost_NT_dict_selected * factor_el_cost_NT_dict_selected
            # if dt.month != dt.shift(1).month and dt.day == calendar.monthrange(dt.year, dt.month)[1] and dt.hour == 23: #because the datetime_column_costs_pd from Solextron stops at the date 31.12.2023 23:00, so the last hour can not be used to check if it is the last day of the month
            if dt.day == calendar.monthrange(dt.year, dt.month)[1] and dt.hour == 23:    
                # Calculate the cost for the basic price and add it to the cumulative sum for the remaining days
                cost_basic_price = value_basic_price_dict_selected * factor_basic_price_dict_selected
                y_values_cum_sum += cost_basic_price

                # Append the basic price cost to the cumulative and non-cumulative y values lists
                y_values_cumulative[-1] = y_values_cum_sum
                y_values_non_cumulative[-1] = cost_basic_price

            # Calculate the SDL and performance price and add it to the cumulative sum
            sdl_performance_price = y_values_chosen_column[index] * value_SDL_price_dict_selected * factor_SDL_price_dict_selected
            # y_values_cum_sum += sdl_performance_price
            y_value += sdl_performance_price

            # # Update the last element of the cumulative and non-cumulative y values lists
            # y_values_cumulative[-1] = y_values_cum_sum
            # y_values_non_cumulative[-1] = sdl_performance_price

            # Update the cumulative sum variable
            y_values_cum_sum += y_value
            # Append the cumulative and non-cumulative y values to their respective lists
            y_values_cumulative.append(y_values_cum_sum)
            y_values_non_cumulative.append(y_value)

    # Return both the cumulative and non-cumulative y values
    return y_values_cumulative, y_values_non_cumulative, sum_y_values_chosen_column, y_values_cum_sum, selected_option



    # testing = data_el_cost_dict_selected[key_el_cost_HT_dict_selected]['value']


# Define the callbacks
@callback(
    Output('cost-graphs', 'children'),
    [Input('dropdown-costs', 'value'),
    Input('main_store', 'data')]
)
def generate_cost_plots(option_dropdown_el_cost, main_store_data):

    # print(type(main_store_data['data_frames']))
    # print(main_store_data['data_frames'])

    # Create a DataFrame from the data stored in the main_store
    main_store_data_cost_column = pd.DataFrame(main_store_data['data_frames']).reset_index(drop=True)
    
    # get the name for the chosen column through the dropdown option
    name_chosen_column = main_store_data_cost_column.columns[int(option_dropdown_el_cost)]

    # Extract the numeric values from the dictionary and create a separate list
    y_values_chosen_column = main_store_data_cost_column.iloc[:, int(option_dropdown_el_cost)]

    datetime_column_costs = main_store_data['results_excel_computation']['datetime_column']

    datetime_column_costs_hours = main_store_data['results_excel_computation']['datetime_column_serialized_hours']

    #get the data from the dictionary from the main_store for the electrical costs
    data_el_cost_dict = main_store_data['options_data_el_cost_dict']

    #call the function to calculate the electrical costs for the chosen character
    y_values_cumulative, y_values_non_cumulative, sum_y_values_chosen_column, y_values_cum_sum, selected_option = calc_el_cost_character(option_dropdown_el_cost, name_chosen_column, y_values_chosen_column, datetime_column_costs, datetime_column_costs_hours ,data_el_cost_dict)

    # Create a list to hold the traces for each array of data
    traces = []

    # Access the dropdown menu options directly from the layout
    dropdown_costs_menu_options = layout['dropdown-reference-character'].options

    # Find the corresponding dictionary for the selected option
    # selected_option_dict = next((option for option in dropdown_costs_menu_options if option['value'] == selected_option), None)
    selected_option_dict = next((option for option in dropdown_costs_menu_options if option['value'] == selected_option))

    # Get the label of the chosen option
    selected_label = selected_option_dict["label"] #if selected_option_dict is not None else "Default Label"  # Replace "Default Label" with your desired default value

    # Replace "Bezugscharakter" with "BC*"
    selected_label = selected_label.replace("Bezugscharakter", "BC*")

    trace = go.Scattergl(x=datetime_column_costs, y=y_values_cumulative, mode='lines+markers', name=f'{cost_plot_names[int(option_dropdown_el_cost)]} - kumulierte Summe für {selected_label} = {round(y_values_cum_sum,2)} CHF', marker=dict(size=0.5),line=dict(color=colors_el_cost[int(option_dropdown_el_cost)], width=1), showlegend=True)
    traces.append(trace)
    trace = go.Scattergl(x=datetime_column_costs, y=y_values_non_cumulative, mode='lines+markers', name=f'{cost_plot_names[int(option_dropdown_el_cost)]} - Kosten pro Zeit für {selected_label}', marker=dict(size=0.5),line=dict(color=colors_el_cost[int(option_dropdown_el_cost)], width=1), showlegend=True)
    traces.append(trace)

    # Create the plot using Plotly
    cost_plot = go.Figure(data=traces)
    cost_plot.update_layout(
        title=dict(
            text="Kosten plotten",
            x=0.6,  # Set the title's horizontal position to the middle (0.5)
            y=0.95,  # Set the title's vertical position closer to the top
            font=dict(
                family="Montserrat, bold",  # Specify the font family
                size=20,  # Set the title font size to 24
                color="black",  # Set the title font color to blue
            ),
            # weight="bold",  # Set the title font weight to bold
            # style="italic",  # Set the title font style to italic
        ),
        xaxis_title="Zeit [15min Abschnitte]",
        xaxis_title_font=dict(color='black', size=16, family='Montserrat, bold'),  # Set the x-axis title font color to black
        yaxis_title="Elektrizitätskosten [CHF]",
        yaxis_title_font=dict(color='black', size=16, family='Montserrat, bold'),  # Set the x-axis title font color to black
        legend=dict(
            x=-0.07, y=1.25, bgcolor='rgba(255, 255, 255, 0.5)',  # Make the legend background opaque
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


# Define the callbacks
@callback(
    Output('usage-graphs', 'children'),
    Input('main_store', 'data')
)
def generate_usage_plots(main_store_data):


    main_store_data_cost_df = pd.DataFrame(main_store_data['data_frames'])

    datetime_column_costs = main_store_data['results_excel_computation']['datetime_column']

    datetime_column_costs_hours = main_store_data['results_excel_computation']['datetime_column_serialized_hours']

    data_el_cost_dict = main_store_data['options_data_el_cost_dict']

    # Create a list to hold the traces for each array of data
    traces = []

    # Generate x-axis array based on the length of the first array
    x_axis = list(range(1, len(main_store_data_cost_df)+1))

    # Iterate through the columns of the DataFrame
    for col in main_store_data_cost_df.columns:
        # Extract the numeric values from the dictionary and create a separate list
        y_values = main_store_data_cost_df[col]
        sum_y_values = round((y_values.sum()/4),1)
        trace = go.Scattergl(x=datetime_column_costs, y=y_values, mode='lines+markers', name=f'{col} - Summe: {sum_y_values} [kWh/Jahr]', marker=dict(size=0.5),line=dict( width=1))
        traces.append(trace)

    # Create the plot using Plotly
    cost_plot = go.Figure(data=traces)
    cost_plot.update_layout(
        title=dict(
            text="Verbrauch plotten",
            x=0.5,  # Set the title's horizontal position to the middle (0.5)
            y=0.95,  # Set the title's vertical position closer to the top
            font=dict(
                family="Montserrat, bold",  # Specify the font family
                size=20,  # Set the title font size to 24
                color="black",  # Set the title font color to blue
            ),
            # weight="bold",  # Set the title font weight to bold
            # style="italic",  # Set the title font style to italic
        ),
        xaxis_title="Zeit [15min Abschnitte]",
        xaxis_title_font=dict(color='black', size=16, family='Montserrat, bold'),  # Set the x-axis title font color to black
        yaxis_title="Verbrauchsdaten [kWh]",
        yaxis_title_font=dict(color='black', size=16, family='Montserrat, bold'),  # Set the x-axis title font color to black
        legend=dict(
            x=-0.07, y=1.25, bgcolor='rgba(255, 255, 255, 0.5)',  # Make the legend background opaque
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