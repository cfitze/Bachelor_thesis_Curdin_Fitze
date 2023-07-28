import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from TkinterDnD2 import *
import dash # Dash application with interactivity
from dash import dcc, html, callback, Output, Input  # import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pickle # to save the import_excel Data from the Excel-file into a binary pickle file
import scipy.stats as stats # for the normal distribution

# import cProfile # to profile the code and see where it takes the most time

# from flask_caching import Cache
# from main_app_module import get_cached_data



dash.register_page(__name__, path='/daten-analyse', name='Datenanalyse', order=5) # is a subpage of the home page

# Create a cache object and do some initial calculations
filename_excel = "BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle"
filename_user = "Riedgrabenstrasse 5/7/9/11/13"
plot_name_combined = "alle ausgewählten Simulationsdaten"

import_excel = pickle.load(open(filename_excel, "rb"))

columns_available = import_excel.columns.tolist()

# columns_available_without_datetime_inital = columns_available[1:6]
columns_available_without_datetime = columns_available[1:]


# Convert DateTime column to datetime format
datetime_column = pd.to_datetime(import_excel['DateTime'])


datetime_column_frame = import_excel.iloc[:,[0]] 


# Set initial values for the slider and dropdown menu

initial_selected_columns = ['Solar [kWh]','SelfConsumption [kWh]', 'Demand [kWh]', 'Net Grid Import/Export [kWh]', 'Battery [kWh]']  # Set the initial selected columns as a list
initial_data_without_datetime = import_excel.iloc[:, 1:]  # Exclude the first column (DateTime)
testing = initial_data_without_datetime.to_dict('records')


# Get the first and last dates from the DateTime column
initial_first_date = import_excel['DateTime'].iloc[0]
initial_last_date = import_excel['DateTime'].iloc[20000]

initial_start_date_index = int(initial_first_date.timestamp())
initial_end_date_index = int(initial_last_date.timestamp())

# # Get the index of the first and last dates
# initial_start_index = initial_first_date.index
# initial_end_index = initial_last_date.index

initial_start_index = datetime_column.index[0]
initial_end_index = datetime_column.index[-1]

# # Get the index of the first and last dates
# initial_start_date_index = datetime_column.index[0]
# initial_end_date_index = datetime_column.index[-1]

# # Convert first and last dates to Swiss time format
swiss_time_format = '%d.%b.%Y'
initial_start_date_index_swiss = initial_first_date.strftime(swiss_time_format)
initial_end_date_index_swiss = initial_last_date.strftime(swiss_time_format)

# Create marks dictionary with English month names
# month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# Create marks dictionary with German month names
month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
days_names = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag','Sonntag']

# List of colors to be used in the bar plots
# color_list = ['#0000FF', '#FF0000', '#008000', '#FFFF00', '#800080', '#000000', '#FFA500']
color_list = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9A6324', '#800000']

# Year
year = "2023"

# date_range = pd.date_range(initial_first_date, initial_last_date, freq='MS')  # 'MS' stands for Month Start
# slider_marks = {date.timestamp(): {'label': date.strftime('%b %Y'), 'style': {'color': "#{:06x}".format(random.randint(0, 0xFFFFFF))}} for date in date_range}

# Define the marks for the slider
date_range = pd.date_range(initial_first_date, initial_last_date, freq='D')
# slider_marks = {date.timestamp(): date.strftime('%b %Y') for date in date_range}

# # Update the marks with corresponding dates
# for timestamp, mark in slider_marks.items():
#     date = pd.Timestamp.fromtimestamp(timestamp)
#     formatted_date = date.strftime('%d.%b.%Y')
#     slider_marks[timestamp] = {'label': formatted_date}
# # data_per_month = initial_data_without_datetime.set_index(datetime_column_frame['DateTime']).resample('M').sum()



# Define the layout of the application
layout = html.Div(children=[
    # dcc.Location(id='url', refresh=False),  # Add the dcc.Location component here
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1('Daten-Visualisierung und Analyse', className="pages-header"),
                    html.P("Auf dieser Seite werden die simulierten Daten grafisch dargestellt und analytische/statistische Elemente hinzugefügt. Es kann zu Verzögerungen wegen den Berechnungen führen...", className= 'subheader',style={'font-size': '18px', 'fontWeight': 'bold', 'fontFamily': 'Arial'}),
                    
                ],
                style={'textAlign': 'center'}
            )
        ],
        # style={'display': 'flex', 'flexDirection': 'column'}
        # style={'display': 'flex'}
    ),
    dcc.Store(
        id='store' , storage_type='memory',
        data={
            'initial_data_without_datetime': initial_data_without_datetime.to_dict('records'),
            'datetime_column': datetime_column_frame.to_dict('records'),
            'initial_first_date': str(initial_first_date),
            'initial_last_date': str(initial_last_date),
            'initial_selected_columns': initial_selected_columns
        }
    ),
    
    dcc.RangeSlider(
        id='date-slider',
        step = None,    # If step=None, the slider will select the nearest step value.
        # marks = slider_marks,
        # marks = {initial_start_index: initial_start_date_index_swiss, initial_end_index: initial_end_date_index_swiss},
        included = True,
        min=initial_start_date_index,
        max=initial_end_date_index,
        value=[initial_start_date_index, initial_end_date_index],  # Set initial range # step=10, # value=[30, 70],# allowCross=False,# pushable=20,
        persistence=True,
        persistence_type='session',
        tooltip={'always_visible': True, 'placement': 'bottom'}
    ),
    # html.Br(),
    html.Div(id='selected-dates-output', style={'fontWeight': 'bold','textAlign': 'center', 'fontSize': '22px'}),  # Placeholder for displaying selected start and end dates
    # html.Br(),
            dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.P("Wählen sie die gewünschten Wochentage aus:", className='regular-text', style={"text-align": "left"}),

                        ]
                    ),
                    width=3,
                ),
                dbc.Col(
                    html.Div(
                        dcc.Checklist(
                            id='selected-days-checklist-items',
                            options=[{'label': day, 'value': day} for day in days_names],
                            value = days_names,
                            # labelStyle={'display': 'block'},
                            # labelStyle={ 'fontWeight': 'bold', 'fontSize': '15px'},
                            labelStyle={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '15px', 'text-align': 'left'},
                            inputStyle={'margin-right': '5px'},
                            inputClassName='check-input',
                            className='check-container',
                            persistence=True,
                            persistence_type='session',
                            inline=True,
                            style={'color': 'blue', 'font-size': '10px','opacity': '0.8'}
                        ),
                    ),
                    width=5,
                ),
                ]
            ),
    # html.Br(),
    # dcc.Dropdown(
    #     id='column-dropdown',
    #     options = [{'label': column, 'value': column} for column in initial_selected_columns],
    #     multi=True,  # Set multi=True to allow selecting multiple datasets
    #     value=initial_selected_columns  # Set the initial value to the first column
    # ),

    dcc.Checklist(
        id='selected-date-checklist-items',
        options=[{'label': column, 'value': column} for column in columns_available_without_datetime],
        value = initial_selected_columns,
        # labelStyle={'display': 'block'},
        # labelStyle={ 'fontWeight': 'bold', 'fontSize': '15px'},
        labelStyle={'display': 'inline-block', 'fontWeight': 'bold', 'fontSize': '15px', 'margin': '0px 10px 0px 0px'},
        inputStyle={'margin-right': '5px'},
        inputClassName='check-input',
        className='check-container',
        persistence=True,
        persistence_type='session',
        inline=True,
        style={'color': 'blue', 'font-size': '10px','opacity': '0.8'}
    ),
    html.Br(),

    dcc.Loading(
        id="loading",
        type="graph",
        style={'marginTop': '100px'},  # Adjust the marginTop value as desired
        children=[
            # html.Div(
            #     className="loading-text",
            #     children="Berechnungen werden ausgeführt",
            #     style={'text-align': 'center', 'font-weight': 'bold'}
            # ),
            html.Div(id='graphs-container')
        ]
    ),

    html.Br(),

])

    
@callback(
    dash.dependencies.Output('selected-dates-output', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
    dash.dependencies.Input('store', 'data')]
)
def display_selected_dates(selected_date_range, stored_data):
    start_date, end_date = [pd.to_datetime(date, unit='s') for date in selected_date_range]  # convert timestamp to datetime
    return html.Div(f"Zeitbereich von: {start_date.strftime('%d-%m-%Y')} bis {end_date.strftime('%d-%m-%Y')} für {filename_user}", style={'color': 'black', 'fontWeight': 'bold', 'fontSize': '20px'})


# Define the callbacks
@callback(
    dash.dependencies.Output('graphs-container', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
    dash.dependencies.Input('selected-date-checklist-items', 'value'),
    dash.dependencies.Input('store', 'data')],
    background=True,
    cache_by=True,
    running=[
        (Output("date-slider", "disabled"), True, False),
        (Output("selected-days-checklist-items", "disabled"), True, False),
        (Output("selected-date-checklist-items", "disabled"), True, False),
        
    ],
)
def generate_plots(selected_date_range, selected_columns, stored_data):
    datetime_column = pd.to_datetime([i['DateTime'] for i in stored_data['datetime_column']])
    start_date, end_date = [pd.to_datetime(date, unit='s') for date in selected_date_range]  # convert timestamp to datetime
    initial_data_without_datetime = pd.DataFrame(stored_data['initial_data_without_datetime'])

    # Generate combined plot
    combined_figure = create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, selected_columns, color_list, plot_name = plot_name_combined)
    combined_plot = dcc.Graph(
            id='combined-bar-plot',
            figure=combined_figure
    )

    # Generate a dcc.Graph instance for each selected column
    plots = [combined_plot]  # Add combined plot to list first
    for i, column in enumerate(selected_columns):
        color = color_list[i % len(color_list)]  # This line chooses the color for each graph
        figure = create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, [column], color_list=[color], plot_name = column)  # Here we pass the chosen color

        plot = dcc.Graph(
            id=f'{column}-bar-plot',
            figure=figure
        )
        plots.append(plot)

    return plots

# @cache.memoize(timeout=30)
def create_plot_figure(data_without_datetime, datetime_column, start_date, end_date, selected_columns, color_list, plot_name):
    # Filter the data based on the selected date range
    filtered_data_dates = datetime_column[(datetime_column >= start_date) & (datetime_column <= end_date)]

    filtered_data_columns = data_without_datetime.loc[(datetime_column >= start_date) & (datetime_column <= end_date), :]

    # print("Filtered data per chosen columns: {}".format(filtered_data_columns))

    figure = {
        'data': [
            go.Scattergl(
                x=filtered_data_dates,
                y=filtered_data_columns[column],
                mode='lines+markers',
                marker=dict(color=color_list[i % len(color_list)], line=dict(width=2), size=1),  # Use the color from the list, and set size of dots
                name=f'{column}-Streudiagramm'
            ) for i, column in enumerate(selected_columns)
        ] + [
            go.Bar(
                x=filtered_data_dates,
                y=filtered_data_columns[column],
                hoverinfo='all',
                marker=dict(color=color_list[i % len(color_list)], line=dict(width=1)),  # Use the color from the list
                name=f'{column}-Balkendiagramm',
                width=4,  # Adjust the width of the bars here
                visible='legendonly'  # Make the plot not visible by default
            ) for i, column in enumerate(selected_columns)      
        ],

        'layout': go.Layout(
            xaxis=dict(title='Date Time', showgrid=True, gridcolor='lightgray', gridwidth=0.5, tickwidth=1, ticks='inside'),
            yaxis=dict(title='[kWh]', showgrid=True, gridcolor='lightgray', gridwidth=0.5, tickwidth=1, ticks='inside'),
            barmode='group',
            title='Interaktives Plotten für ' + plot_name,
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(x=0, y=1.1, bgcolor='rgba(255, 255, 255, 0.4)',  # Make the legend background opaque
            # opacity=0.4,  # Make the legend entries semi-transparent
            font=dict(size=10),  # Change the legend text size to 14
            bordercolor='rgba(100, 100, 200, 0.2)',  # Make the legend border transparent
            borderwidth=2,  # Make the legend border width 1
            ),
            plot_bgcolor='rgba(255, 255, 255, 0.3)',  # Set the plot background to 20% opaque white
            paper_bgcolor='rgba(255, 255, 255, 0.3)'  # Set the paper (outside plot) background to 20% opaque white
    
            # plot_bgcolor='white',
            # paper_bgcolor='white'
        )
    }

    if len(selected_columns) == 1:

        # Get the selected column name, actually not needed because we only have one column, but for shortness of code
        column = selected_columns[0]

        # Additional code for adding other distribution traces as desired

        # Add average line for single column plot
        column = selected_columns[0]
        average_value = np.mean(filtered_data_columns[column])
        min_value = np.min(filtered_data_columns[column])
        max_value = np.max(filtered_data_columns[column])

        average_line = go.Scattergl(
            x=filtered_data_dates,
            y=average_value * np.ones(len(filtered_data_dates)),
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Mittelwert: <b>{average_value:.3f}</b>'
        )
        figure['data'].append(average_line)

        # Scattergl trace for minimum value
        min_scatter = go.Scattergl(
            x=filtered_data_dates,
            y=np.full(len(filtered_data_dates), min_value),
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Min: {min_value:.3f}',
            visible='legendonly'
        )
        figure['data'].append(min_scatter)

        # Scattergl trace for maximum value
        max_scatter = go.Scattergl(
            x=filtered_data_dates,
            y=np.full(len(filtered_data_dates), max_value),
            mode='lines',
            line=dict(color='black', dash='dash'),
            # marker=dict(color='black', symbol='triangle-up', size=10),
            name=f'Max: {max_value:.3f}',
            visible='legendonly'
        )
        figure['data'].append(max_scatter)


        # Calculate the moving average with the selected range
        range_start = start_date
        range_end = end_date
        selected_dates = filtered_data_dates[(filtered_data_dates >= range_start) & (filtered_data_dates <= range_end)]
        selected_data = filtered_data_columns[column][(filtered_data_dates >= range_start) & (filtered_data_dates <= range_end)]
        window_size = len(selected_dates)  # Window size based on the selected range
        moving_average = selected_data.rolling(window_size, min_periods=1).mean()
        amount_of_days = round(window_size / (4 * 24), 1)

        # Add the moving average line
        moving_average_line = go.Scattergl(
            x=filtered_data_dates,
            y=moving_average,
            mode='lines',
            line=dict(color='blue'),  # Adjust the color as desired
            name=f'Gleitender Durchschnitt über ({amount_of_days} Tage)',
            visible='legendonly'
        )
        figure['data'].append(moving_average_line)


    return figure
        # # Add annotations for the minimum and maximum values
        # figure['layout']['annotations'] = [
        #     dict(
        #         x=filtered_data_dates[0],
        #         y=min_value,
        #         text=f'Min: {min_value:.3f}',
        #         showarrow=True,
        #         arrowhead=1,
        #         arrowcolor='black',
        #         arrowsize=1,
        #         ax=20,
        #         ay=-40,
        #         font=dict(color='black')
        #     ),
        #     dict(
        #         x=filtered_data_dates[-1],
        #         y=max_value,
        #         text=f'Max: {max_value:.3f}',
        #         showarrow=True,
        #         arrowhead=1,
        #         arrowcolor='black',
        #         arrowsize=1,
        #         ax=20,
        #         ay=-40,
        #         font=dict(color='black')
        #     )
        # ]


    # return figure



# When working with 15-minute energy consumption, solar energy production, battery, and export/import data over a whole year, there are several statistical analysis and data exploration techniques you can consider. Here are some options:

# 1. Time Series Analysis: Perform time series analysis to identify patterns, trends, and seasonality in the data. You can use techniques such as decomposition, autocorrelation analysis, and spectral analysis to gain insights into the temporal behavior of the energy data.

# 2. Descriptive Statistics: Calculate descriptive statistics such as mean, median, variance, and standard deviation to summarize the central tendency, variability, and distribution of the energy data. This can provide insights into the average energy consumption, production, and fluctuations over the year.

# 3. Data Visualization: Create various plots and charts to visualize the energy data. Line plots, area plots, and stacked area plots can show the energy consumption, production, and other variables over time. Heatmaps can display patterns and correlations between different variables. Box plots can provide information about the distribution and variability of the data.

# 4. Correlation Analysis: Calculate correlation coefficients between different energy variables (e.g., consumption and production) to examine their relationships. Scatter plots can help visualize the correlation and identify any linear or nonlinear associations.

# 5. Seasonal Analysis: Perform seasonal analysis to identify recurring patterns or cycles in the energy data. This can involve techniques such as seasonal decomposition of time series, seasonal subseries plots, and seasonal indices.

# 6. Forecasting: Use time series forecasting methods (e.g., ARIMA, SARIMA, or exponential smoothing models) to predict future energy consumption, production, or other relevant variables. This can assist in capacity planning, demand management, and decision-making.

# 7. Anomaly Detection: Apply anomaly detection algorithms to identify unusual or anomalous energy consumption or production patterns. This can help detect energy efficiency issues, equipment malfunctions, or unusual events that require attention.

# 8. Energy Balance Analysis: Analyze the energy balance between consumption, production, battery storage, and export/import to assess energy self-sufficiency, grid interaction, and overall energy management.

# 9. Regression Analysis: Perform regression analysis to understand the relationship between energy consumption/production and other factors such as weather variables, time of day, or occupancy. This can help identify significant predictors and quantify their impact on energy usage.

# 10. Data Mining and Machine Learning: Apply data mining and machine learning techniques to discover hidden patterns, build predictive models, and uncover insights from the energy data. This could involve clustering analysis, decision trees, random forests, or neural networks.

# It's important to select the appropriate techniques based on the specific goals, characteristics of the data, and the insights you want to gain. Consider the data's temporal nature, correlations, trends, and seasonality when choosing the best options for analysis.




# Anomaly Detection: Apply anomaly detection algorithms to identify unusual or anomalous energy consumption or production patterns