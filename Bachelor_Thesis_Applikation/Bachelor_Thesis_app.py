import random
import pickle
import dash
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import webbrowser
from threading import Timer
from flask_caching import Cache


def open_browser():
    # Check if the browser is already open
    if not webbrowser.get().open('http://127.0.0.1:8050/', new=2):
        print("Browser is already open.")


#initialise the app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB]) #, assets_folder='assets')

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache_directory',
    'CACHE_DEFAULT_TIMEOUT': 3600  # Cache timeout in seconds
})

@cache.cached()
def expensive_computation():

    # Check if the data is already cached
    cached_data = cache.get('expensive_computation_data')
    if cached_data is not None:

        # Access the cache directory path
        cache_directory = cache.cache_dir
        print("Cache Directory:", cache_directory)
        return cached_data
    
    
    #Import the data from the Excel file from Solextron via a pickle file
    import_excel = pickle.load(open("BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle", "rb"))

    # Get the column names of the imported Excel file
    columns_available = import_excel.columns.tolist()

    # columns_available_without_datetime_inital = columns_available[1:6]
    columns_available_without_datetime = columns_available[1:]

    # Convert DateTime column to datetime format
    datetime_column = pd.to_datetime(import_excel['DateTime'])

    # Create a new dataframe with only the DateTime column
    datetime_column_frame = import_excel.iloc[:,[0]]

    #Get the initial selected columns and the initail data without the DateTime column
    initial_selected_columns = ['Solar [kWh]','SelfConsumption [kWh]', 'Demand [kWh]', 'Net Grid Import/Export [kWh]', 'Battery [kWh]']  # Set the initial selected columns as a list
    initial_data_without_datetime = import_excel.iloc[:, 1:]  # Exclude the first column (DateTime)

    # Get the first and last dates from the DateTime column
    initial_first_date = import_excel['DateTime'].iloc[0]
    initial_last_date = import_excel['DateTime'].iloc[10000]

    initial_start_date_index = int(initial_first_date.timestamp())
    initial_end_date_index = int(initial_last_date.timestamp())


    # # Convert first and last dates to Swiss time format
    swiss_time_format = '%d.%b.%Y'
    initial_start_date_index_swiss = initial_first_date.strftime(swiss_time_format)
    initial_end_date_index_swiss = initial_last_date.strftime(swiss_time_format)

    # month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    # Create marks dictionary with German month names
    month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

    # List of colors to be used in the bar plots
    # color_list = ['#0000FF', '#FF0000', '#008000', '#FFFF00', '#800080', '#000000', '#FFA500']
    color_list = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9A6324', '#800000']
    # Year
    year = "2023"
    # Define the marks for the slider
    date_range = pd.date_range(initial_first_date, initial_last_date, freq='D')
    slider_marks = {date.timestamp(): {'label': date.strftime('%b %Y'), 'style': {'color': "#{:06x}".format(random.randint(0, 0xFFFFFF))}} for date in date_range}

    # Store the variables in a dictionary
    results = {
        'columns_available': columns_available,
        'columns_available_without_datetime': columns_available_without_datetime,
        'datetime_column': datetime_column,
        'datetime_column_frame': datetime_column_frame,
        'initial_selected_columns': initial_selected_columns,
        'initial_data_without_datetime': initial_data_without_datetime,
        'initial_first_date': initial_first_date,
        'initial_last_date': initial_last_date,
        'initial_start_date_index': initial_start_date_index,
        'initial_end_date_index': initial_end_date_index,
        'initial_start_date_index_swiss': initial_start_date_index_swiss,
        'initial_end_date_index_swiss': initial_end_date_index_swiss,
        'month_names': month_names,
        'color_list': color_list,
        'year': year,
        'slider_marks': slider_marks
    }

    # Store the dictionary in the cache
    cache.set('expensive_computation_data', results)

    # Access the cache directory path
    cache_directory = cache.cache_dir
    print("Cache Directory:", cache_directory)

    # Return the results
    return results



sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)



app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Python Dash Application meiner Bachelor Thesis",
                         style={'fontSize':30, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    ),

    # Including the Store in the layout
    # dcc.Store(
    #     id='main_store', 
    #     data={
    #         'initial_data_without_datetime': initial_data_without_datetime.to_dict('records'),
    #         'datetime_column': datetime_column_frame.to_dict('records'),
    #         'initial_first_date': str(initial_first_date),
    #         'initial_last_date': str(initial_last_date),
    #         'initial_selected_columns': initial_selected_columns
    #     }
    # ),
], fluid=True)

if __name__ == "__main__":
    open_browser()  # Open the browser window without delay
    app.run(debug=False, dev_tools_ui=False)  # Run the app

    # debug=True, # port=8050, # host='0.0.0.0', # dev_tools_ui=True, ll dev_tools_hot_reload=True, # ev_tools_hot_reload_interval=1000,
    # dev_tools_silence_routes_logging=False,# mode='inline'# )
    # Run the Dash application
    # app.run_server(debug=True, mode='inline',dev_tools_ui=True,)



# import webapp2
# import webapp2_profiler

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         # Your code logic here

# app = webapp2.WSGIApplication([
#     ('/', MainHandler),
# ], debug=True)

# app = webapp2_profiler.ProfilerWSGIMiddleware(app)