import pickle
import re
from uuid import uuid4
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
# from dash_bootstrap_templates import load_figure_template
from dash import DiskcacheManager, CeleryManager, Input, Output, html
from dash.long_callback import DiskcacheLongCallbackManager


def open_browser():
    # Check if the browser is already open
    if not webbrowser.get().open('http://127.0.0.1:8050/', new=0):
        print("Browser is already open.")

def show_cache_directory():
    with app.server.app_context():
        cache_directory = app.server.config['CACHE_DIR']
        return f"Cache Directory: {cache_directory}"

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    launch_uid = uuid4()
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app,
                                                cache_by=[lambda: launch_uid], expire=60
                                                )
else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    launch_uid = uuid4()
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache,
                                                    cache_by=[lambda: launch_uid], expire=60
                                                    )

# Initialize the Flask server
server = flask.Flask(__name__)

# # Set the cache directory
# server.config['CACHE_DIR'] = 'cache_directory'


#initialise the app
app = dash.Dash(__name__, background_callback_manager=background_callback_manager, server=server, use_pages=True, external_stylesheets=[dbc.themes.QUARTZ, "/assets/styles_BA.css", "/assets/items_BA.css", "/assets/animated_arrow.css", "assets/smooth-arrow-animation/dist/style.css"]) #, assets_folder='assets') #dbc.themes.SPACELAB
#CERULEAN , COSMO , CYBORG , DARKLY , FLATLY , JOURNAL , LITERA , LUMEN , LUX , MATERIA , MINTY , MORPH , PULSE , QUARTZ , SANDSTONE , SIMPLEX , SKETCHY , SLATE , SOLAR , SPACELAB , SUPERHERO , UNITED , VAPOR , YETI , ZEPHYR 

# load_figure_template('LUX')
                     
# # Initialize the cache object
# cache = Cache(app.server, config={
#     'CACHE_TYPE': 'simple',  # Use the simple cache type
#     'CACHE_DEFAULT_TIMEOUT': 3600  # Cache timeout in seconds
# })


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
        id='main_store', storage_type='memory'
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


    # Function to sort the csv files for the dcc.Store
    def custom_sort_key_pickle(filename):
        # Define the desired order of filenames
        order = {
            'BA_23FS_Curdin_Fitze_5_TSextract.pickle': 0,
            'BA_23FS_Curdin_Fitze_7_9_11_TSextract.pickle': 1,
            'BA_23FS_Curdin_Fitze_13_daily_TSextract.pickle': 2,
            'BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle': 3,
        }
        # Return the corresponding order for the filename
        return order.get(filename, 999)  # Use 999 as a default value if the filename is not in the order dictionary

    # @cache.cached()
    def excel_computation():

        # # Check if the data is already cached
        # cached_data = cache.get('expensive_computation_data')
        # if cached_data is not None:
        # return cached_data

        pickel_files_path = 'Bachelor_Thesis_Applikation/assets/Solextron_export'
        pickle_files_list = os.listdir(pickel_files_path)
        # Sort the list of files using the custom_sort_key function
        pickle_files_list.sort(key=custom_sort_key_pickle)

        # Initialize an empty DataFrame to store all the data from the CSV files
        data_frames_stromdaten = pd.DataFrame()

        for file in pickle_files_list:
            if file.endswith('.pickle'):
                file_path_pickle = os.path.join(pickel_files_path, file)
                # Read the CSV file into a DataFrame
                pickle_load = pickle.load(open(file_path_pickle, "rb"))
                # Store the DataFrame in the data_frames dictionary using the file name as the key
            #     data_frames_stromdaten[file] = pickle_load
            #     data_frames_stromdaten_dict = data_frames_stromdaten.to_dict('list')
            # return data_frames_stromdaten_dict

        import_excel_full_path = os.path.join(pickel_files_path, 'BA_23FS_Curdin_Fitze_5_TSextract.pickle')
        #Import the data from the Excel file from Solextron via a pickle file
        import_excel = pickle.load(open(import_excel_full_path, "rb"))

        # Get the column names of the imported Excel file
        columns_available = import_excel.columns.tolist()

        # columns_available_without_datetime_inital = columns_available[1:6]
        columns_available_without_datetime = columns_available[1:]

        # Convert DateTime column to datetime format
        datetime_column = pd.to_datetime(import_excel['DateTime'])

        # Create a new dataframe with only the DateTime column
        datetime_column_frame = import_excel.iloc[:,[0]]

        # Convert datetime_column_frame to a string in Swiss format
        # datetime_column_frame_swiss_format = datetime_column_frame.dt.strftime('%d-%m-%Y %H:%M')

        # Convert datetime_column to a list of strings in ISO format
        datetime_column_serialized = datetime_column.dt.strftime('%d-%m-%Y %H:%M').tolist()
        
        # Convert datetime_column_frame to a dictionary with the DateTime column as a list
        datetime_column_frame_serialized = datetime_column_frame.to_dict(orient='list')




        # Store the variables in a dictionary
        results = {
            'columns_available': columns_available,
            'columns_available_without_datetime': columns_available_without_datetime,
            'datetime_column': datetime_column_serialized,
            'datetime_column_frame': datetime_column_frame_serialized,
        }

        # print(columns_available)

        # # Store the dictionary in the cache
        # cache.set('expensive_computation_data', results)

        # Return the results
        return results

    # Function to sort the csv files for the dcc.Store
    def custom_sort_key_csv(filename):
        # Define the desired order of filenames
        order = {
            'Riedgrabenstrasse5_Lastgang_15min.csv': 0,
            'Riedgrabenstrasse7_9_11_Lastgang_15min.csv': 1,
            'Riedgrabenstrasse13_Lastgang_15min.csv': 2,
            'Riedgrabenstrasse5_7_9_11_13_Lastgang_15min.csv': 3,
        }
        # Return the corresponding order for the filename
        return order.get(filename, 999)  # Use 999 as a default value if the filename is not in the order dictionary

    # Function to read CSV files and store them in the dcc.Store
    def read_and_store_csv_files():
        csv_files_path = 'Bachelor_Thesis_Applikation/assets/Stromdaten'
        csv_files = os.listdir(csv_files_path)
        # Sort the list of files using the custom_sort_key function
        csv_files.sort(key=custom_sort_key_csv)

        # Initialize an empty DataFrame to store all the data from the CSV files
        data_frames_stromdaten = pd.DataFrame()

        for file in csv_files:
            if file.endswith('.csv'):
                file_path = os.path.join(csv_files_path, file)
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                # Store the DataFrame in the data_frames dictionary using the file name as the key
                data_frames_stromdaten[file] = df
                data_frames_stromdaten_dict = data_frames_stromdaten.to_dict('list')

        # Return the data_frames dictionary to be stored in the dcc.Store
        return data_frames_stromdaten_dict

    # Function to split the time range into start and end time, now outiside of the set_el_cost function
    def split_time_range(time_range):
        start_time, end_time = time_range.split('-')
        start_time = start_time.strip()
        end_time = end_time.strip()
        return start_time, end_time
    
    # Function to extract numbers from a string
    def extract_numbers_from_string(input_string):

        # pattern = r'^[0-9]*[.,]{0,1}[0-9]*$'
        # pattern = r'\d+\.\d+'
        pattern = r'^[+-]?(\d+(\.\d+)?)'
        # pattern = r'\b\d+(\.\d+)?\b'

        numbers_list = re.findall(pattern, input_string)
        numbers_list = numbers_list[0] #only take the first match of the regex pattern
        # return [float(num) for num in numbers_list]
        return numbers_list

    # Function to set the electrical costs parameters
    def set_el_cost():

        #define the feedback costs, since they are all the same for the options
        feedback_costs = ['Rückspeisevergütung', '15.15 Rp./kWh', 'unter 300kVA / gleich für HT und NT (exkl. 7.7% MWST))']
        #define the options for the electrical costs
        options_data_el_cost = {
            'option1': [
                ['Grundpreis', '2.69 Fr./Mt.', 'inkl. 7.7% MwSt.'],
                ['Verbrauchspreise HT', '17.39 Rp./kWh.', 'inkl. 7.7% MwSt.'],
                ['Verbrauchspreise NT', '17.39 Rp./kWh.', 'inkl. 7.7% MwSt.'],
                ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                ['Tarifzeiten NT', 'übrige Zeit', ''],
                feedback_costs
            ],
            'option2': [
                ['Grundpreis', '5.5 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                ['Arbeitspreise HT', '5.17 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Arbeitspreise NT', '3.6 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                ['Tarifzeiten NT', 'übrige Zeit', ''],
                ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Leistungspreis', '5.1 Fr./kWh' , '(exkl. 7.7% MWST)'],
                feedback_costs
            ],
            'option3': [
                ['Grundpreis', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],           
                ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],             
                ['Tarifzeiten NT', 'übrige Zeit', ''],
                ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)'],
                feedback_costs
            ],
            'option4': [
                ['Grundpreis --> noch herausfinden', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                ['Tarifzeiten NT', 'übrige Zeit', ''],
                ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)'],
                ['Rückspeisevergütung', 'noch herausfinden', 'unter 300kVA / gleich für HT und NT (exkl. 7.7% MWST))']
            ],
            'option5': [
                ['Grundpreis', '59 Fr./Mt.', 'exkl. 7.7% MwSt.'],
                ['Arbeitspreise HT', '8.01 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Arbeitspreise NT', '5.30 Rp./kWh' , '(exkl. 7.7% MWST)'],  
                ['Tarifzeiten HT', 'Montag-Freitag / Samstag', '07:00-20:00 / 07:00-13:00'],
                ['Tarifzeiten NT', 'übrige Zeit', ''],
                ['Systemdienstleistungspreis SDL', '0.46 Rp./kWh' , '(exkl. 7.7% MWST)'],
                ['Leistungspreis', '9.5 Fr./kWh' , '(exkl. 7.7% MWST)'],
                feedback_costs
                # ['Preis für die Abrechnung','X X X [CHF]', 'Muss durch die Besitzer der Liegenschaften festgelegt werden.']
            ],

        }
        # print(options_data_el_cost.items())

        options_data_el_cost_new = {}
        for option, data_list in options_data_el_cost.items():
            option_data = {}
            for data in data_list:
                label, value_text, information = data[0], data[1], data[2] #later also add the third column with the info

                if label == 'Tarifzeiten HT':
                    # Split the value_text by '/' to extract date and time information
                    dates_HT, date_NT = value_text.split('/')
                    time_range1, time_range2 = information.split('/')
                    start_time1, end_time1 = split_time_range(time_range1)
                    start_time2, end_time2 = split_time_range(time_range2)
                    option_data[label] = {'value': [dates_HT.strip(), date_NT.strip()], 'factor_el_calc': [(start_time1, end_time1), (start_time2, end_time2)], 'info': information}
                    # option_data[label]['timeframes'] = [(start_time1, end_time1), (start_time2, end_time2)]
                elif label == 'Tarifzeiten NT':
                    option_data[label] = {'value': value_text, 'factor_el_calc': '1', 'info': information}
            
                else:
                    
                    try:
                        value_text = value_text.replace(',', '.')  # Replace "," with "."
                        value_number = extract_numbers_from_string(value_text)[0]  # Extract the number using regex
                    except (ValueError, IndexError):
                        value_number = value_text  # Return the original value_text if it cannot be converted to float

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

                    option_data[label] = {'value': value_number, 'factor_el_calc': factor_el_calc, 'info': info}

            #store the option_data in the options_data_el_cost_new dictionary
            options_data_el_cost_new[option] = option_data

            
        #return the options_data_el_cost and the options_data_el_cost_new from the 
        return options_data_el_cost, options_data_el_cost_new

        #call the function for the expensive computation
    
    def set_costs_simulation():

        #set the tabel_costs_simulation's first column names
        capex = 'Ivestitionskosten/CAPEX [CHF]'
        capex_EV = 'CAPEX mit Einmalvergütung [CHF]'
        spez_capex = 'Spez. Investitionskosten (CAPEX/kWP) [CHF/kWp]'
        opex = 'Betriebskosten/OPEX [CHF/Jahr]'
        payback_time = 'Amortisationszeit [Jahre]'
        el_costs = 'Stromkosten [CHF/kWh]'

        #define the options for the electrical simulation costs table
        tabel_costs_simulation = {
            'option1': [
                [capex, '100', '100'],
                [capex_EV, '100', '100'],
                [spez_capex, '100', '100'],
                [opex, '100', '100'],
                [payback_time, '100', '100'],
                [el_costs, '100', '100'],
                
            ],
            'option2': [
                [capex, '1', '2'],
                [capex_EV, '100', '100'],
                [spez_capex, '100', '100'],
                [opex, '100', '100'],
                [payback_time, '9.1', '12.8'],
                [el_costs, '9', '10']
            ],
            'option3': [
                [capex, 'X', 'Y'],
                [capex_EV, '100', '100'],
                [spez_capex, '100', '100'],
                [opex, '100', '100'],
                [payback_time, '9.1', '12.8'],
                [el_costs, '100', '100']
            ],
            'option4': [
                [capex, '!', '@'],
                [capex_EV, '100', '100'],
                [spez_capex, '100', '100'],
                [opex, '100', '100'],
                [payback_time, '9.1', '12.8'],
                [el_costs, '100', '100']
            ]
        }
        
        options_data_costs_simulation_new = {}
        for option, data_list in tabel_costs_simulation.items():
            option_data = {}
            for data in data_list:
                label, value_battery, value_no_battery = data[0], data[1], data[2] #later also add the third column with the info

                if label == capex:
                    #set the label_dict and information for the option_data
                    label_dict = 'CAPEX'
                    information = 'CHF'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                elif label == capex_EV:
                    #set the label_dict and information for the option_data
                    label_dict = 'CAPEX EV'
                    information = 'CHF'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                elif label == spez_capex:
                    #set the label_dict and information for the option_data
                    label_dict = 'CAPEX/kWP'
                    information = 'CHF/kWp'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                elif label == opex:
                    #set the label_dict and information for the option_data
                    label_dict = 'OPEX'
                    information = 'CHF/Jahr'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                elif label == payback_time:
                    #set the label_dict and information for the option_data
                    label_dict = 'Amortisationszeit'
                    information = 'Jahre'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                elif label == el_costs:
                    #set the label_dict and information for the option_data
                    label_dict = 'Stromkosten'
                    information = 'CHF/kWh'
                    option_data[label_dict] = {'value_battery': value_battery, 'value_no_battery': value_no_battery, 'info': information}
                else:
                    pass

            #store the option_data in the options_data_el_cost_new dictionary
            options_data_costs_simulation_new[option] = option_data

            
        #return the options_data_el_cost and the options_data_el_cost_new from the 
        return tabel_costs_simulation, options_data_costs_simulation_new
    
    # print(results_excel_computation)

    # Call the function to set the el_cost_calc data
    options_data_el_cost_table, options_data_el_cost_dict = set_el_cost()

    # Call the function to set the costs_simulation data
    costs_simulation_table, options_data_costs_simulation_dict = set_costs_simulation()
    # print(costs_simulation_table)
    # print(options_data_costs_simulation_dict)

    # print(options_data_el_cost_dict)
    # Function to recursively get all values from a nested dictionary
    def get_all_values(d):
        all_values = []
        for value in d.values():
            if isinstance(value, dict):
                all_values.extend(get_all_values(value))
            else:
                all_values.append(value)
        return all_values

    # Call the function to get all the values
    all_values = get_all_values(options_data_el_cost_dict)
    # print(all_values)

    # testing = read_and_store_csv_files()

    data_to_store = { 
        'options_data_el_cost_table': options_data_el_cost_table, 
        'options_data_el_cost_dict': options_data_el_cost_dict,
        'results_excel_computation': excel_computation(),   #call the fuction excel_computation to get the results from the excel file
        'data_frames': read_and_store_csv_files(),  #call the fuction read_and_store_csv_files to read the csv files and store them in the dcc.Store
        'costs_simulation_table' : costs_simulation_table,
        'options_data_costs_simulation_dict' : options_data_costs_simulation_dict,
        # Add other computed data as needed
    }
    

    #return the data to the dcc.Store
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




# Yes, it is possible to create a second layout in a Dash app specifically designed for mobile devices. Dash provides a way to define different layouts for different screen sizes using the dash_responsive_grid_layout module.

# Here's how you can achieve this:

#     Install the dash-responsive-grid-layout module:

# bash

# pip install dash-responsive-grid-layout

#     Import the required modules in your Dash app:

# python

# import dash
# import dash_html_components as html
# from dash_responsive_grid_layout import DashResponsiveGridLayout

#     Define the layout for desktop devices as usual:

# python

# # Define the layout for desktop devices
# desktop_layout = html.Div(
#     [
#         # Your desktop layout components here...
#     ]
# )

#     Define the layout for mobile devices using the DashResponsiveGridLayout:

# python

# # Define the layout for mobile devices using DashResponsiveGridLayout
# mobile_layout = DashResponsiveGridLayout(
#     id="mobile-layout",
#     layout=[
#         # Your mobile layout components here...
#     ],
#     cols=12,  # Number of columns for the grid
#     rowHeight=100,  # Height of the rows
#     breakpoints={
#         # Specify breakpoints for different screen sizes
#         "xs": 0,  # Mobile devices
#         "sm": 576,  # Small tablets and larger mobile devices
#         "md": 768,  # Tablets and larger devices
#         "lg": 992,  # Desktops and larger devices
#         "xl": 1200,  # Larger desktops
#     },
# )

#     Create the Dash app and include both layouts:

# python

# app = dash.Dash(__name__)

# app.layout = html.Div(
#     [
#         # Include both desktop and mobile layouts in the main layout
#         desktop_layout,
#         mobile_layout,
#     ]
# )

# # ... (rest of the app code)

# With this setup, the DashResponsiveGridLayout will automatically switch to the appropriate layout based on the screen size of the device. You can define the mobile layout to be more suitable for smaller screens, making your app responsive and user-friendly on mobile devices.