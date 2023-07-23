import random
import pickle
from anyio import Event
import dash
import flask
import os  # Import the os module to access files
import pandas as pd
from dash import dcc, html, callback, Output, Input, State
import dash_bootstrap_components as dbc
import webbrowser
from threading import Timer
from flask_caching import Cache
from dash_bootstrap_templates import load_figure_template


def open_browser():
    # Check if the browser is already open
    if not webbrowser.get().open('http://127.0.0.1:8050/', new=0):
        print("Browser is already open.")

def show_cache_directory():
    with app.server.app_context():
        cache_directory = app.server.config['CACHE_DIR']
        return f"Cache Directory: {cache_directory}"

# Initialize the Flask server
server = flask.Flask(__name__)

# # Set the cache directory
# server.config['CACHE_DIR'] = 'cache_directory'


#initialise the app
app = dash.Dash(__name__, server=server, use_pages=True, external_stylesheets=[dbc.themes.QUARTZ, "/assets/styles_BA.css", "/assets/items_BA.css", "/assets/animated_arrow.css", "assets/smooth-arrow-animation/dist/style.css"]) #, assets_folder='assets') #dbc.themes.SPACELAB
#CERULEAN , COSMO , CYBORG , DARKLY , FLATLY , JOURNAL , LITERA , LUMEN , LUX , MATERIA , MINTY , MORPH , PULSE , QUARTZ , SANDSTONE , SIMPLEX , SKETCHY , SLATE , SOLAR , SPACELAB , SUPERHERO , UNITED , VAPOR , YETI , ZEPHYR 

#initialise the app
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB]) #, assets_folder='assets')
load_figure_template('LUX')
                     
# Initialize the cache object
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Use the simple cache type
    'CACHE_DEFAULT_TIMEOUT': 3600  # Cache timeout in seconds
})


# define the layout for the sidebar navigation bar
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(
                    page["name"],
                    className="sidebar"
                ),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="bg-transparent",
)


app.layout = dbc.Container(
    [
        # dcc.Input(id='dummy-trigger', style={'display': 'none'}, value='trigger'),
        dcc.Interval(id='trigger-expensive-computation', interval=1000 *1000, n_intervals=0),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "Python Dash Application meiner Bachelor Thesis",
                        className= "app-title"
                        
                    )
                )
            ]
        ),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2,
                style={
                    "position": "fixed",  # Fix the position
                    "top": "90px",  # Position below the title
                    "left": "0",  # Position at the left
                    "height": "calc(100vh - 100px)",  # Take full height minus title height
                    "overflowY": "auto",  # Enable vertical scrolling
                    "zIndex": "999",  # Set a high z-index to keep it on top
                    },

            ),
            dbc.Col(
                [
                    dash.page_container
                ],
                # xs=12, sm=12, md=9, lg=10, xl=10, xxl=10,  # Adjust the column widths
                xs=8, sm=8, md=10, lg=10, xl=10, xxl=10,  # Adjust the column widths
                style={
                    "marginLeft": "16%",  # Add left margin to accommodate the sidebar width
                    "marginRight": "5%",  # Add right margin to accommodate the sidebar width
                },
                
                
            )
        ]
    ),

    # Including the Store in the layout
    dcc.Store(
        id='main_store', 
        # data={

        #     'data_frames': data_frames_stromdaten_dict,  # Store the CSV data_frames in the Store
        #     'options_data_el_cost_table' : options_data_el_cost_table,
        #     'options_data_el_cost_dict' : options_data_el_cost_dict,
        #     # 'initial_data_without_datetime': initial_data_without_datetime.to_dict('records'),
        #     # 'datetime_column': datetime_column_frame.to_dict('records'),
        #     # 'initial_first_date': str(initial_first_date),
        #     # 'initial_last_date': str(initial_last_date),
        #     # 'initial_selected_columns': initial_selected_columns
        # }
    ),
    ], 
    fluid=True,
)

# Define the callback for the "dummy" input to trigger the expensive computation
@app.callback(
    Output('main_store', 'data'),
    Input('trigger-expensive-computation', 'n_intervals'),
    prevent_initial_call=False  # Allow the callback to run on initial page load
    # State('main_store', 'data') #only needed if some data is already stored in the dcc.Store
)
def expensive_computation(dummy_trigger):

    # # Check if the data is already in the Store
    # data_in_store = dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'main_store.data'
    # if data_in_store:
    #     # Data is already in the Store, no need to recompute
    #     return dash.no_update
    # else:
    #     # Data is not in the Store, trigger the expensive computation
    #     # ... (existing callback code)

        # @cache.cached()
        def excel_computation():

            # Check if the data is already cached
            cached_data = cache.get('expensive_computation_data')
            if cached_data is not None:

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

            # Return the results
            return results

        #call the function for the expensive computation
        # results_excel_computation = excel_computation()

        # Function to read CSV files and store them in the dcc.Store
        def read_and_store_csv_files():
            csv_files_path = 'Bachelor_Thesis_Applikation/assets/Stromdaten'
            csv_files = os.listdir(csv_files_path)
            data_frames = {}
            data_frames_stromdaten = pd.DataFrame()
            for file in csv_files:
                if file.endswith('.csv'):
                    file_path = os.path.join(csv_files_path, file)
                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(file_path)
                    # Store the DataFrame in the data_frames dictionary using the file name as the key
                    data_frames_stromdaten[file] = df
                    data_frames_stromdaten_dict = data_frames_stromdaten.to_dict('list')
                    data_frames[file] = df.to_dict('records')

            # Return the data_frames dictionary to be stored in the dcc.Store
            return data_frames_stromdaten_dict

        # Call the function to read CSV files and store them in the dcc.Store
        data_frames_stromdaten_dict = read_and_store_csv_files()

        # Function to set the electrical costs parameters
        def set_el_cost():
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
                    ['Grundpreis --> noch herausfinden', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                    ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                    ['Tarifzeiten NT', 'übrige Zeit', ''],
                    ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)']
                ],
                'option5': [
                    ['Grundpreis', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                    ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                    ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                    ['Tarifzeiten NT', 'übrige Zeit', ''],
                    ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)'],
                    # ['Preis für die Abrechnung','X X X [CHF]', 'Muss durch die Besitzer der Liegenschaften festgelegt werden.']
                ],

            }

            # New dictionary with labels as keys and values as numbers of the el_cost_calc table
            options_data_el_cost_new = {}
            for option, data_list in options_data_el_cost.items():
                option_data = {}
                for data in data_list:
                    label, value_text = data[0], data[1]

                    # Check if the row is 'Tarifzeiten HT' or 'Tarifzeiten NT'
                    if label == 'Tarifzeiten HT' or label == 'Tarifzeiten NT':
                        # Split the value_text by '/' to extract date and time information
                        if value_text == 'übrige Zeit':
                                pass # Do nothing for now
                        else:
                            date_info, time_info = value_text.split('/')

                        # Store the date and time information as a list in the 'value' key
                        option_data[label] = {'value': [date_info.strip(), time_info.strip()], 'info': ''}
                    else:
                        # Extract numeric value from the 'value_text' string
                        value_number = float(''.join(filter(str.isdigit, value_text)))

                        # Determine the information (e.g., 'Rp./kWh', 'Fr./Mt.', 'Fr./kWh')
                        if 'Rp./kWh' in value_text:
                            factor_el_calc = 0.0025
                            info = 'Rp./kWh'
                        elif 'Fr./Mt.' in value_text:
                            factor_el_calc = 1
                            info = 'Fr./Mt.'
                        elif 'Fr./kWh' in value_text:
                            factor_el_calc = 0.25
                            info = 'Fr./kWh'
                        else:
                            info = ''  # Replace with an appropriate default value if needed

                        # Store the numeric value and information in the option_data dictionary
                        option_data[label] = {'value': value_number, 'factor_el_calc': factor_el_calc, 'info': info}

                options_data_el_cost_new[option] = option_data

            return options_data_el_cost, options_data_el_cost_new

        # Call the function to set the el_cost_calc data
        options_data_el_cost_table, options_data_el_cost_dict = set_el_cost()

            # Store the computed data in the dcc.Store
        data_to_store = {
            'data_frames': data_frames_stromdaten_dict,  # Add the actual computed data_frames_stromdaten_dict
            'options_data_el_cost_table': options_data_el_cost_table,  # Add the actual computed options_data_el_cost_table
            'options_data_el_cost_dict': options_data_el_cost_dict,  # Add the actual computed options_data_el_cost_dict
            # Add other computed data as needed
        }
        return data_to_store



# # Define routes
# @server.route("/open-browser")
# def route_open_browser():
#     open_browser()
#     return "Browser opened!"

# @server.route("/cache-directory")
# def route_cache_directory():
#     return show_cache_directory()


if __name__ == "__main__":
    # open_browser()  # Open the browser window without delay
    app.run(debug=True, dev_tools_ui=True)  # Run the app

    # debug=True, # port=8050, # host='0.0.0.0', # dev_tools_ui=True, ll dev_tools_hot_reload=True, # ev_tools_hot_reload_interval=1000,
    # dev_tools_silence_routes_logging=False,# mode='inline'# )
    # Run the Dash application
    # app.run_server(debug=True, mode='inline',dev_tools_ui=True,)


# # Get the path of the current file
# current_file_path = os.path.abspath(__file__)

# # Get the parent directory of the current file
# parent_directory = os.path.dirname(current_file_path)

# # Build the cache directory path
# cache_directory = os.path.join(parent_directory, ".dash-cache")

# print("Cache Directory:", cache_directory)

# import webapp2
# import webapp2_profiler

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         # Your code logic here

# app = webapp2.WSGIApplication([
#     ('/', MainHandler),
# ], debug=True)

# app = webapp2_profiler.ProfilerWSGIMiddleware(app)