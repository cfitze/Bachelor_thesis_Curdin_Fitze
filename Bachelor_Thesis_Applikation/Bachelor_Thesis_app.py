import random
import pickle
import dash
import flask
import os  # Import the os module to access files
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import webbrowser
from threading import Timer
from flask_caching import Cache
from dash_bootstrap_templates import load_figure_template


def open_browser():
    # Check if the browser is already open
    if not webbrowser.get().open('http://127.0.0.1:8050/', new=2):
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
app = dash.Dash(__name__, server=server, use_pages=True, external_stylesheets=[dbc.themes.QUARTZ]) #, assets_folder='assets') #dbc.themes.SPACELAB
#CERULEAN , COSMO , CYBORG , DARKLY , FLATLY , JOURNAL , LITERA , LUMEN , LUX , MATERIA , MINTY , MORPH , PULSE , QUARTZ , SANDSTONE , SIMPLEX , SKETCHY , SLATE , SOLAR , SPACELAB , SUPERHERO , UNITED , VAPOR , YETI , ZEPHYR 

#initialise the app
# app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB]) #, assets_folder='assets')
load_figure_template('LUX')
                     
# Initialize the cache object
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Use the simple cache type
    'CACHE_DEFAULT_TIMEOUT': 3600  # Cache timeout in seconds
})


# @cache.cached()
def expensive_computation():

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
# expensive_computation()

# Function to read CSV files and store them in the dcc.Store
def read_and_store_csv_files():
    csv_files_path = 'Bachelor_Thesis_Applikation/assets/Stromdaten'
    csv_files = os.listdir(csv_files_path)
    data_frames = {}
    for file in csv_files:
        if file.endswith('.csv'):
            file_path = os.path.join(csv_files_path, file)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            # Store the DataFrame in the data_frames dictionary using the file name as the key
            data_frames[file] = df.to_dict('records')

    # Return the data_frames dictionary to be stored in the dcc.Store
    return data_frames

# Call the function to read CSV files and store them in the dcc.Store
data_frames_to_store = read_and_store_csv_files()


# define the layout for the sidebar navigation bar
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(
                    page["name"],
                    className="ms-2",
                    style={
                        "font-weight": "bold",
                        "font-size": "18px",
                    },
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
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        "Python Dash Application meiner Bachelor Thesis",
                        style={
                            "fontSize": 35,
                            "textAlign": "center",
                            "fontWeight": "bold",
                            "fontFamily": "Arial",
                            "background-color": "transparent",
                        },
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
                    "top": "100px",  # Position below the title
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
        data={

            'data_frames': data_frames_to_store  # Store the CSV data_frames in the Store
            # 'initial_data_without_datetime': initial_data_without_datetime.to_dict('records'),
            # 'datetime_column': datetime_column_frame.to_dict('records'),
            # 'initial_first_date': str(initial_first_date),
            # 'initial_last_date': str(initial_last_date),
            # 'initial_selected_columns': initial_selected_columns
        }
    ),
    ], 
    fluid=True,
    # style={'backgroundColor': 'white'}  # Set the background color to white
)






# Define routes
@server.route("/open-browser")
def route_open_browser():
    open_browser()
    return "Browser opened!"

@server.route("/cache-directory")
def route_cache_directory():
    return show_cache_directory()


if __name__ == "__main__":
    open_browser()  # Open the browser window without delay
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