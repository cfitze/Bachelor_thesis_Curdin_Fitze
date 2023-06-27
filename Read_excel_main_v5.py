
import json
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
import tkinter as tk
from TkinterDnD2 import *
import dash # Dash application with interactivity
from dash import dcc # import dash_core_components as dcc
from dash import html  # import dash_html_components as html
import plotly.graph_objs as go
import pickle # to save the import_excel Data from the Excel-file into a binary pickle file
# import cProfile # to profile the code and see where it takes the most time


#.mro() You can actually check a class’s MRO by calling the mro method on the class, which gives you the list of classes in the order of how a method is resolved.


# Main class
class MainClass:

    #filename_excel= 'BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.xlsx'
    #initial_path = '"C:/Users/cfitz/FHNW/P-6-23FS_M365 - General/04_Diverse/Github_repository"'
    #initial_path = '"C:/Users/cfitz"'
    #print(initial_path)
    # import_excel_csv_np = None
    
    def __init__(self):

        pass #more code can come here later on that will have to be inheritet

    print('With this dash application you can show 3d Bar plots from a chosen Excel-File')
     

    
#print(main_class.directory_path)
#print(main_class.filename)

#print(help(MainClass))


# Subclass to plot the data
class PlotExcel(MainClass):

    # def __init__(self, filename_excel,import_excel_DateTime,import_excel_self_consumption):
    def __init__(self):
        super().__init__()



        self.import_excel_DateTime = None
        self.import_excel_self_consumption = None
        # self.app = dash.Dash(__name__)

    def plot_results(self,import_excel ,import_excel_csv_np, import_excel_csv_np_cols):


        print("Please wait...")

        # plotFigure =plt.figure()
        # plt.figure(figsize=(12, 8))  # Set the width and height of the figure window

        import_excel.plot(x="DateTime", y="Solar [kWh]", figsize=(14, 10),title= "DateTime vs. Solar")



        # x_column='x', y_column='y', plot_type='line',figsize=(8, 6), title='Line Plot', xlabel='X-axis', ylabel='Y-axis',
        # xlim=(0, 10), ylim=(0, 100), grid=True, legend=True, color='red',
        # alpha=0.5, linewidth=2.0, marker='o', markersize=8, cmap='viridis',
        # rot=45, logy=False)

        # plt.plot(import_excel["DateTime"], import_excel["Solar [kWh]"])

        # plt.plot(import_excel_csv_np[:,1], import_excel_csv_np[:,2])
        # print(import_excel_csv_np)
        # rows = np.arange(0,10000)
        # plt.scatter(import_excel_csv_np[rows,1], import_excel_csv_np[rows,2], s=1)
        # plt.plot(import_excel_csv_np_cols[rows,0], import_excel_csv_np_cols[rows,1])
        # plt.plot(import_excel_csv_np[rows,1], import_excel_csv_np[rows,2])
        # plt.plot(MainClass.import_excel_csv_np[:,1], MainClass.import_excel_csv_np[:,2])


        plt.xlabel('Date Time') #Sets the label for the x-axis.
        plt.ylabel('Self consumption [kWh]') #Sets the label for the y-axis.
        plt.title('Plot figure') #Sets the title for the plot.
        plt.grid(True) #Adds a grid to the plot.

        # Set the position and size of the first figure window
        #plotFigure.canvas.manager.window.setGeometry(100, 100, 800, 600)

        plt.show()

        # Toggle full-screen mode
        #plt.get_current_fig_manager().full_screen_toggle()
        # Create a plot and set the figure size

        # #plotBar= plt.figure(figsize=(12, 8))  # Set the width and height of the figure window
        # plt.figure(figsize=(12, 8))  # Set the width and height of the figure window
        # plt.bar(self.import_excel_DateTime, self.import_excel_self_consumption)
        # plt.xlabel('Date Time') #Sets the label for the x-axis.
        # plt.ylabel('Self consumption [kWh]') #Sets the label for the y-axis.
        # plt.title('Plot bar') #Sets the title for the plot.
        # plt.grid(True) #Adds a grid to the plot.

        # # Set the position and size of the second figure window
        # #plotBar.canvas.manager.window.setGeometry(500, 100, 800, 600)

        # # plt.show()

    def start_dash_plot(self, import_excel):

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
        initial_last_date = import_excel['DateTime'].iloc[-1]

        # Get the index of the first and last dates
        initial_start_date_index = datetime_column.index[0]
        initial_end_date_index = datetime_column.index[-1]

        # # Convert first and last dates to Swiss time format
        swiss_time_format = '%d.%b.%Y'
        initial_start_date_index_swiss = initial_first_date.strftime(swiss_time_format)
        initial_end_date_index_swiss = initial_last_date.strftime(swiss_time_format)

        # Create marks dictionary with English month names
        # month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        # Create marks dictionary with German month names
        month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

        # Year
        year = "2023"

        # Generate the marks for every month
        # marks = {i+1: {'label': month_names[i] + ' ' + year} for i in range(12)}

        # Create a list of months and years for marks
        date_range = pd.date_range(initial_start_date_index_swiss, initial_end_date_index_swiss, freq='M')
        # marks = {date: date.strftime('%b %Y') for date in date_range}


        # Create the Dash application
        self.app = dash.Dash(__name__)

        # Define the layout of the application
        self.app.layout = html.Div(children=[
            html.H1(children='3D Interactive Bar Plot', style={'textAlign': 'center'}),
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
            html.Br(),
            dcc.RangeSlider(
                id='date-slider',
                # marks=marks,
                # marks = {i: {'label': month_names[i-1]} for i in range(1, 13)},
                min=initial_start_date_index,
                max=initial_end_date_index,
                value=[initial_start_date_index, initial_end_date_index]  # Set initial range # step=10, # value=[30, 70],# allowCross=False,# pushable=20,
                # tooltip={'always_visible': True, 'placement': 'bottom'}
            ),
            html.Br(),
            html.Div(id='selected-dates-output'),  # Placeholder for displaying selected start and end dates
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
                value = initial_selected_columns,  # now this can be a list
                labelStyle={'display': 'block'},
                inputStyle={'margin-right': '5px'},
                inputClassName='check-input',
                className='check-container',
                persistence=True,
                persistence_type='session',
                inline=False,
                loading_state={'is_loading': False, 'component_name': 'check-items'},
                style={'color': 'blue', 'font-size': '14px'}
            ),
    
            html.Br(),
            dcc.Graph(
                id='3d-bar-plot',
                figure=self.create_plot_figure(initial_data_without_datetime, datetime_column ,initial_first_date, initial_last_date, initial_selected_columns)  # Pass the initial date and empty dataset list
            ),
            html.Div(id='graphs-container')
        ])

        # Callbacks
        @self.app.callback(
            dash.dependencies.Output('graphs-container', 'children'),
            [dash.dependencies.Input('date-slider', 'value'),
            dash.dependencies.Input('selected-date-checklist-items', 'value'),
            dash.dependencies.Input('store', 'data')]
        )
        def generate_plots(selected_date_range, selected_columns, stored_data):
            datetime_column = pd.to_datetime(pd.DataFrame(stored_data['datetime_column'])['DateTime'])
            start_date_index, end_date_index = selected_date_range
            start_date = datetime_column[start_date_index]
            end_date = datetime_column[end_date_index]
            initial_data_without_datetime = pd.DataFrame(stored_data['initial_data_without_datetime'])

            # Generate a dcc.Graph instance for each selected column
            plots = []
            for column in selected_columns:
                figure = self.create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, [column])
                plot = dcc.Graph(
                    id=f'{column}-bar-plot',
                    figure=figure
                )
                plots.append(plot)

            return plots

        # Callback to display the selected start and end dates
        @self.app.callback(
            dash.dependencies.Output('selected-dates-output', 'children'),
            [dash.dependencies.Input('date-slider', 'value'),
            dash.dependencies.Input('store', 'data')]
        )
        def display_selected_dates(selected_date_range, stored_data):
            datetime_column = pd.to_datetime(stored_data['datetime_column'])
            start_date_index, end_date_index = selected_date_range
            start_date = datetime_column[start_date_index]
            end_date = datetime_column[end_date_index]
            return f"Selected Date Range: {start_date} to {end_date}"



        # Run the Dash application
        # app.run_server(debug=True, mode='inline',dev_tools_ui=True,)

    def run_server(self):
        self.app.run_server(debug=True)
        # self.app.run_server()

        # sys.exit()
        # return
                        # dev_tools_hot_reload=True,  --> would be interesting to add later

                # debug=True, # port=8050, # host='0.0.0.0', # dev_tools_ui=True, # dev_tools_hot_reload=True, # ev_tools_hot_reload_interval=1000,
                # dev_tools_silence_routes_logging=False,# mode='inline'# )


    def create_plot_figure(self, data_without_datetime, datetime_column ,start_date, end_date, selected_columns):

        # Filter the data based on the selected date range
        filtered_data_dates = datetime_column[(datetime_column >= start_date) & (datetime_column <= end_date)]

        # filtered_data_columns = initial_data_without_datetime.loc[start_date_index:end_date_index]
        filtered_data_columns = data_without_datetime.loc[(datetime_column >= start_date) & (datetime_column <= end_date), :]


        # print("Filtered data per chosen columns: {}".format(filtered_data_columns))

        # Create the 2d plot figure
        figure = {
            'data': [
                go.Bar(
                    x=filtered_data_dates,
                    y=filtered_data_columns[column],
                    text='TestText',
                    hoverinfo='all',
                    marker=dict(color='blue'),
                    name=f'{column}'
                ) for column in selected_columns
            ],
            'layout': go.Layout(
                xaxis=dict(title='Date'),
                yaxis=dict(title='Value'),
                barmode='group',
                title='3D Interactive Bar Plot',
                margin=dict(l=0, r=0, t=40, b=0),
                legend=dict(x=0, y=1)
            )
        }

        return figure
    

#print(help(PlotExcel))

class VariablesCheck:
    def __init__(self):
        self.config = {}

    def no_filedialog(self):

        # filename = "BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.xlsx"

        # import_excel = pd.read_excel(filename, sheet_name="15min")
        import_excel = pickle.load(open("BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.pickle", "rb"))

        # import_excel = pd.DataFrame(import_excel)

        return import_excel

    def select_file_and_create_folder(self):
        try:
            excel_file_path = self.config.get("file_path")
            excel_data = None

            # Check if the config.json file exists
            if excel_file_path and os.path.exists(excel_file_path):
                # Load the config dictionary from the config.json file
                folder_path = os.path.dirname(excel_file_path)
                config_file_path = os.path.join(folder_path, "config.json")
                with open(config_file_path, "r") as config_file:
                    self.config = json.load(config_file)

                # Check if the folder and pickle file exist
                pickle_file_path = os.path.join(folder_path, os.path.splitext(os.path.basename(excel_file_path))[0] + ".pickle")
                if os.path.exists(pickle_file_path):
                    use_pickle = input("A pickle file exists in the same folder. Do you want to load data from the pickle file? (y/n): ")
                    if use_pickle.lower() == "y":
                        try:
                            print("Loading data from pickle file...")
                            with open(pickle_file_path, "rb") as pickle_file:
                                excel_data = pickle.load(pickle_file)
                            # Process the loaded data as needed
                            print("Data loaded successfully!")
                        except EOFError:
                            print("The pickle file is empty or corrupted. Loading data from Excel file instead.")

                if excel_data is None:
                    # Process the Excel file and create a new pickle file
                    excel_data = pd.read_excel(excel_file_path)  # Read Excel file as DataFrame
                    with open(pickle_file_path, "wb") as pickle_file:
                        pickle.dump(excel_data, pickle_file)
                    # Process the Excel data as needed
                    # ...

            else:
                # If no Excel file has been loaded previously, prompt the user to select a file
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(title="Choose a file", filetypes=[("Excel Files", "*.xlsx"), ("Pickle Files", "*.pickle")])
                
                # Determine the file type
                file_extension = os.path.splitext(file_path)[1]
                if file_extension == ".xlsx":
                    excel_file_path = file_path
                    pickle_file_path = os.path.join(os.path.dirname(excel_file_path), os.path.splitext(os.path.basename(excel_file_path))[0] + ".pickle")

                    if os.path.exists(pickle_file_path):
                        use_pickle = input("A pickle file exists in the same folder. Do you want to load data from the pickle file? (y/n): ")
                        if use_pickle.lower() == "y":
                            try:
                                print("Loading data from pickle file...")
                                with open(pickle_file_path, "rb") as pickle_file:
                                    excel_data = pickle.load(pickle_file)
                                # Process the loaded data as needed
                                print("Data loaded successfully!")
                            except EOFError:
                                print("The pickle file is empty or corrupted. Loading data from Excel file instead.")

                    if excel_data is None:
                        # Process the Excel file and create a new pickle file
                        excel_data = pd.read_excel(excel_file_path, sheet_name='15min')  # Read Excel file as DataFrame
                        with open(pickle_file_path, "wb") as pickle_file:
                            pickle.dump(excel_data, pickle_file)
                        # Process the Excel data as needed
                        # ...

                elif file_extension == ".pickle":
                    pickle_file_path = file_path
                    try:
                        print("Loading data from pickle file...")
                        with open(pickle_file_path, "rb") as pickle_file:
                            excel_data = pickle.load(pickle_file)
                        # Process the loaded data as needed
                        print("Data loaded successfully!")
                    except EOFError:
                        print("The pickle file is empty or corrupted. Please select a valid file.")

                else:
                    print("Invalid file type. Please select an Excel file or a pickle file.")

            return pd.DataFrame(excel_data) if excel_data is not None else None

        except IOError as e:
            print("Error:", str(e))


# Start the code running #

if __name__ == '__main__':

    # profiler = 
    main_class = MainClass()
    plot_excel = PlotExcel()
    # print("filename", plot_excel.initial_path)
    variables_check = VariablesCheck()
    # excel_data = variables_check.select_file_and_create_folder()  # try to load the config.json and pickle file
    excel_data = variables_check.no_filedialog()


    # plot_excel.plot_results(import_excel, import_excel_csv_np, import_excel_csv_np_cols)

# if __name__ == '__main__':

    plot_excel.start_dash_plot(excel_data)
    plot_excel.run_server()







    # # Check if the app is running --> #for the VariablesCheck class
    # if app.debug:
    #     print("App is running")
    # else:
    #     print("App is not running")






# import webapp2
# import webapp2_profiler

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         # Your code logic here

# app = webapp2.WSGIApplication([
#     ('/', MainHandler),
# ], debug=True)

# app = webapp2_profiler.ProfilerWSGIMiddleware(app)