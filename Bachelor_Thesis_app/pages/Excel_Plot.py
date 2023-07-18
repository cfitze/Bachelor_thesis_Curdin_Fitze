import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from TkinterDnD2 import *
import dash # Dash application with interactivity
from dash import dcc, html, callback, Output, Input  # import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pickle # to save the import_excel Data from the Excel-file into a binary pickle file

# import cProfile # to profile the code and see where it takes the most time

from flask_caching import Cache



dash.register_page(__name__, path='/excel-plotting', name='Excel-Plotting', order=2) # is a subpage of the home page

# Define the layout for the home page
# home_page_layout = html.Div([
    
layout = html.Div([
    html.H1('Bachelor Thesis Curdin Fitze'),
    html.P('Willkommen auf der Startseite der Bachelor Thesis von Curdin Fitze / Testing.'),
    # html.A('Open PDF', href='/pdf')
])



import_excel = pickle.load(open("BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle", "rb"))

columns_available = import_excel.columns.tolist()

# columns_available_without_datetime_inital = columns_available[1:6]
columns_available_without_datetime = columns_available[1:]


# Convert DateTime column to datetime format
datetime_column = pd.to_datetime(import_excel['DateTime'])


datetime_column_frame = import_excel.iloc[:,[0]] 


# Set initial values for the slider and dropdown menu

initial_selected_columns = ['Solar [kWh]','SelfConsumption [kWh]', 'Demand [kWh]', 'Net Grid Import/Export [kWh]', 'Battery [kWh]']  # Set the initial selected columns as a list
initial_data_without_datetime = import_excel.iloc[:, 1:]  # Exclude the first column (DateTime)


# Get the first and last dates from the DateTime column
initial_first_date = import_excel['DateTime'].iloc[0]
initial_last_date = import_excel['DateTime'].iloc[10000]

initial_start_date_index = int(initial_first_date.timestamp())
initial_end_date_index = int(initial_last_date.timestamp())

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

# List of colors to be used in the bar plots
# color_list = ['blue', 'red', 'green', 'yellow', 'purple', 'black', 'orange']
# color_list = ['#0000FF', '#FF0000', '#008000', '#FFFF00', '#800080', '#000000', '#FFA500']
color_list = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9A6324', '#800000']

# Year
year = "2023"

# Generate the marks for every month
# marks = {i+1: {'label': month_names[i] + ' ' + year} for i in range(12)}


# Define the marks for the slider
date_range = pd.date_range(initial_first_date, initial_last_date, freq='D')
# # slider_marks = {date.timestamp(): date.strftime('%b %Y') for date in date_range}
# slider_marks = {date.timestamp(): date.strftime('%d.%m.%y') for date in date_range}

# date_range = pd.date_range(initial_first_date, initial_last_date, freq='MS')  # 'MS' stands for Month Start
slider_marks = {date.timestamp(): {'label': date.strftime('%b %Y'), 'style': {'color': "#{:06x}".format(random.randint(0, 0xFFFFFF))}} for date in date_range}

# data_per_month = initial_data_without_datetime.set_index(datetime_column_frame['DateTime']).resample('M').sum()

# print(slider_marks)


# Configure your cache with your dash app's server
# cache.init_app(app.server)


# Define the layout of the application
layout = html.Div(children=[
    # dcc.Location(id='url', refresh=False),  # Add the dcc.Location component here
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H1('Interactive Plotting', style={'textAlign': 'center','fontSize': '32px', 'fontWeight': 'bold', 'fontFamily': 'Source Sans Pro'})
                ],
                style={'textAlign': 'center'}
            )
        ],
        # style={'display': 'flex', 'flexDirection': 'column'}
        # style={'display': 'flex'}
    ),
    dcc.Store(
        id='store', 
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
        marks = slider_marks,
        # marks = {i: {'label': month_names[i-1]} for i in range(1, 13)},
        min=initial_start_date_index,
        max=initial_end_date_index,
        value=[initial_start_date_index, initial_end_date_index]  # Set initial range # step=10, # value=[30, 70],# allowCross=False,# pushable=20,
        # tooltip={'always_visible': True, 'placement': 'bottom'}
    ),
    # html.Br(),
    html.Div(id='selected-dates-output', style={'fontWeight': 'bold','textAlign': 'center', 'fontSize': '22px'}),  # Placeholder for displaying selected start and end dates
    html.Br(),
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
        style={'color': 'blue', 'font-size': '10px'}
    ),
    html.Br(),
    dcc.Graph(
        id='bar-plot',
        # figure=create_plot_figure(initial_data_without_datetime, datetime_column ,initial_first_date, initial_last_date, initial_selected_columns, color_list)  # Pass the initial date and empty dataset list
    ),
    html.Div(id='graphs-container'),
    html.Br(),

])

    
# Define the callbacks
@callback(
    dash.dependencies.Output('graphs-container', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
    dash.dependencies.Input('selected-date-checklist-items', 'value'),
    dash.dependencies.Input('store', 'data')]
)
def generate_plots(selected_date_range, selected_columns, stored_data):
    datetime_column = pd.to_datetime([i['DateTime'] for i in stored_data['datetime_column']])
    start_date, end_date = [pd.to_datetime(date, unit='s') for date in selected_date_range]  # convert timestamp to datetime
    initial_data_without_datetime = pd.DataFrame(stored_data['initial_data_without_datetime'])

    # Generate a dcc.Graph instance for each selected column
    plots = []
    for i, column in enumerate(selected_columns):
        color = color_list[i % len(color_list)]  # This line chooses the color for each graph
        figure = create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, [column], color_list=[color])  # Here we pass the chosen color

        plot = dcc.Graph(
            id=f'{column}-bar-plot',
            figure=figure
        )
        plots.append(plot)

    return plots

#         plots = [
#     dcc.Graph(
#         id=f'{column}-bar-plot',
#         figure=create_plot_figure(
#             initial_data_without_datetime, datetime_column, start_date, end_date, [column], color=color
#         )
#     ) for i, column in enumerate(selected_columns)
# ]

@callback(
    dash.dependencies.Output('selected-dates-output', 'children'),
    [dash.dependencies.Input('date-slider', 'value'),
    dash.dependencies.Input('store', 'data')]
)
def display_selected_dates(selected_date_range, stored_data):
    start_date, end_date = [pd.to_datetime(date, unit='s') for date in selected_date_range]  # convert timestamp to datetime
    return html.Div(f"Selected Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}", style={'color': 'black', 'fontWeight': 'bold', 'fontSize': '20px'})


# @cache.memoize(timeout=30)
def create_plot_figure(data_without_datetime, datetime_column, start_date, end_date, selected_columns, color_list):
    # Filter the data based on the selected date range
    filtered_data_dates = datetime_column[(datetime_column >= start_date) & (datetime_column <= end_date)]

    filtered_data_columns = data_without_datetime.loc[(datetime_column >= start_date) & (datetime_column <= end_date), :]

    # print("Filtered data per chosen columns: {}".format(filtered_data_columns))

    figure = {
        'data': [
            go.Scatter(
                x=filtered_data_dates,
                y=filtered_data_columns[column],
                mode='lines+markers',
                marker=dict(color=color_list[i % len(color_list)], line=dict(width=2), size=1),  # Use the color from the list, and set size of dots
                name=f'{column}-scatter'
            ) for i, column in enumerate(selected_columns)
        ] + [
            go.Bar(
                x=filtered_data_dates,
                y=filtered_data_columns[column],
                hoverinfo='all',
                marker=dict(color=color_list[i % len(color_list)], line=dict(width=1)),  # Use the color from the list
                name=f'{column}-bar',
                width=0.5,  # Adjust the width of the bars here
                visible='legendonly'  # Make the plot not visible by default
            ) for i, column in enumerate(selected_columns)      
        ],

        'layout': go.Layout(
            xaxis=dict(title='Date Time', showgrid=True, gridcolor='lightgray', gridwidth=0.5, tickwidth=1, ticks='inside'),
            yaxis=dict(title='[kWh]', showgrid=True, gridcolor='lightgray', gridwidth=0.5, tickwidth=1, ticks='inside'),
            barmode='group',
            title='Interactive Solextron Data Visualisation',
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(x=0, y=1.1, bgcolor='rgba(255, 255, 255, 0.8)',  # Make the legend background opaque
            # opacity=0.4,  # Make the legend entries semi-transparent
            font=dict(size=10),  # Change the legend text size to 14
            bordercolor='rgba(100, 100, 200, 0.5)',  # Make the legend border transparent
            borderwidth=2,  # Make the legend border width 1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
    }

    return figure

        #     # Create the 2d plot figure
        #     go.Bar(
        #         x=filtered_data_dates,
        #         y=filtered_data_columns[column],
        #         hoverinfo='all',
        #         marker=dict(color=color, line=dict(width=50)),
        #         name=f'{column}-bar'
        #     ) for column, color in zip(selected_columns, color_list)
        # ] + [
    






# @callback(
#     Output('url', 'pathname'),
#     [Input('subpage-link', 'pathname')],
#     [State('url', 'pathname')]
# )
# def navigate_to_page(subpage_pathname, current_pathname):
#     if subpage_pathname != current_pathname:
#         return subpage_pathname
#     return current_pathname

# @callback(
#     Output('subpage-info', 'children'),
#     [Input('url', 'pathname')]
# )
# def update_subpage_info(pathname):
#     if pathname == '/subpage':
#         return html.P("You are currently on the subpage.")
#     else:
#         return html.P("You are on the main page.")

# @callback(
#     Output('graphs-container', 'style'),
#     [Input('url', 'pathname')]
# )
# def hide_graphs_container(pathname):
#     if pathname == '/subpage':
#         return {'display': 'none'}
#     return {}


    
# @callback(Output('url', 'pathname'), [Input('url', 'pathname')], [State('url', 'pathname')])
# def go_back_to_main_page(current_pathname, previous_pathname):
#     if current_pathname == '/subpage' and previous_pathname == '/subpage':
#         return '/'
#     else:
#         return current_pathname
