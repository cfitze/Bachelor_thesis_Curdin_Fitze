
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


        # Convert DateTime column to datetime format
        datetime_column = pd.to_datetime(import_excel['DateTime'])


        # Set initial values for the slider and dropdown menu

        initial_selected_columns = ['Solar [kWh]','SelfConsumption [kWh]', 'Demand [kWh]', 'Net Grid Import/Export [kWh]', 'Battery [kWh]']  # Set the initial selected columns as a list
        initial_data_without_datetime = import_excel.iloc[:, 1:]  # Exclude the first column (DateTime)


        # Get the first and last dates from the DateTime column
        initial_first_date = import_excel['DateTime'].iloc[0]
        initial_last_date = import_excel['DateTime'].iloc[-1]

        # Convert first and last dates to Swiss time format
        swiss_time_format = '%d.%b.%Y'
        initial_start_date_index = initial_first_date.strftime(swiss_time_format)
        initial_end_date_index = initial_last_date.strftime(swiss_time_format)

        # Create marks dictionary with English month names
        # month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        # Create marks dictionary with German month names
        month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']


        # Create the Dash application
        self.app = dash.Dash(__name__)

        # Define the layout of the application
        self.app.layout = html.Div(children=[
            html.H1(children='3D Interactive Bar Plot'),
            dcc.RangeSlider(
                id='date-slider',
                marks = {i: {'label': month_names[i-1]} for i in range(1, 13)},
                min=initial_start_date_index,
                max=initial_end_date_index,
                value=[initial_start_date_index, initial_end_date_index]  # Set initial range
                # step=10,
                # value=[30, 70],
                # allowCross=False,
                # pushable=20,
                # tooltip={'always_visible': True, 'placement': 'bottom'}
            ),
            html.Div(id='selected-dates-output'),  # Placeholder for displaying selected start and end dates
            # dcc.Dropdown(
            #     id='column-dropdown',
            #     options = [{'label': column, 'value': column} for column in initial_selected_columns],
            #     multi=True,  # Set multi=True to allow selecting multiple datasets
            #     value=initial_selected_columns  # Set the initial value to the first column
            # ),
            
            dcc.RadioItems(
                id='selected-radio-items',
                options=[{'label': column, 'value': column} for column in initial_selected_columns],
                value=initial_selected_columns,  # Set the initial value to the first column
                labelStyle={'display': 'block'},
                inputStyle={'margin-right': '5px'},
                inputClassName='radio-input',
                className='radio-container',
                persistence=True,
                persistence_type='session',
                persistence_expired=False,
                inline=False,
                switch=False,
                loading_state={'is_loading': False, 'component_name': 'radio-items'},
                style={'color': 'blue', 'font-size': '14px'}
            ),
            dcc.Graph(
                id='3d-bar-plot',
                figure=self.create_plot_figure(initial_data_without_datetime, datetime_column ,initial_first_date, initial_last_date, initial_selected_columns)  # Pass the initial date and empty dataset list
            )
        ])

        # Define the callback to update the plot on the selected columns
        @self.app.callback(
            dash.dependencies.Output('3d-bar-plot', 'options'),
            [dash.dependencies.Input('selected-radio-items', 'value')]
        )
        def update_datasets(selected_columns):
            options = []
            for column in selected_columns:
                selected_columns= initial_data_without_datetime[column]  # Get the data for the selected column
                options.extend([{'label': dataset, 'value': dataset} for dataset in selected_columns])
            return options

        # Define the callback to update the plot based on the selected date range
        @self.app.callback(
            dash.dependencies.Output('3d-bar-plot', 'figure'),
            [dash.dependencies.Input('date-slider', 'value')]
            # dash.dependencies.Input('3d-bar-plot', 'options')]
        )
        def update_plot(selected_date_range):
            start_date_index, end_date_index = selected_date_range
            start_date = datetime_column[start_date_index]
            end_date = datetime_column[end_date_index]
            selected_columns = dash.callback_context.inputs['column-dropdown.value']
            return self.create_plot_figure(initial_data_without_datetime, datetime_column, start_date, end_date, selected_columns)

        # Define the callback to display the selected start and end dates
        @self.app.callback(
            dash.dependencies.Output('selected-dates-output', 'children'),
            [dash.dependencies.Input('date-slider', 'value')]
        )
        def display_selected_dates(selected_date_range):
            start_date_index, end_date_index = selected_date_range
            start_date = datetime_column[start_date_index]
            end_date = datetime_column[end_date_index]
            return f"Selected Date Range: {start_date} to {end_date}"
            # return f"Selected Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"



        # Run the Dash application
        # app.run_server(debug=True, mode='inline',dev_tools_ui=True,)

    def run_server(self):
        # self.app.run_server(debug=True)
        self.app.run_server()

        # sys.exit()
        # return
                        # dev_tools_hot_reload=True,  --> would be interesting to add later

                # debug=True, # port=8050, # host='0.0.0.0', # dev_tools_ui=True, # dev_tools_hot_reload=True, # ev_tools_hot_reload_interval=1000,
                # dev_tools_silence_routes_logging=False,# mode='inline'# )


    def create_plot_figure(self, initial_data_without_datetime, datetime_column ,start_date, end_date, selected_columns):

        # Filter the data based on the selected date range
        filtered_data_dates = datetime_column[
            # (import_excel_figure['DateTime'] >= start_date) & (import_excel_figure['DateTime'] <= end_date)]
            (datetime_column >= start_date) & (datetime_column <= end_date)]
    

        # Filter the data based on the selected columns
        filtered_data_columns = initial_data_without_datetime.loc[(datetime_column >= start_date) & (datetime_column <= end_date), selected_columns]


        print("Filtered data per chosen columns: {}".format(filtered_data_columns))

        # Create the 3D bar plot figure
        figure = {
            'data': [
                go.Bar(
                    x=filtered_data_dates,
                    y=filtered_data_columns[column],
                    # z=filtered_data['z'],
                    text='TestText',
                    hoverinfo='all',
                    marker=dict(color='blue'),
                    name=f'{column}'
                ) for column in filtered_data_columns.columns
            ],
            'layout': go.Layout(
                scene=dict(
                    xaxis=dict(title='X-axis'),
                    yaxis=dict(title='Y-axis'),
                    zaxis=dict(title='Z-axis')
                ),
                barmode='group',    # Change this value to select the desired barmode option
                title='3D Interactive Bar Plot',
                yaxis=dict(title='Y-axis'),
                margin=dict(l=0, r=0, t=40, b=0),  # Adjust margins for better layout
                legend=dict(x=0, y=1)
            )
        }

        return figure

    

#print(help(PlotExcel))

class VariablesCheck(MainClass):

    # def __init__(self, filename_excel):
    def __init__(self):

        super().__init__()

    
        self.CONFIG_FILE = "config.json"
        self.filename_excel = None
        self.initial_path = '"C:/Users/cfitz/FHNW/P-6-23FS_M365 - General/04_Diverse/Github_repository"'
        # self.initial_path = '"C:/Users/cfitz"'
        self.directory_path = None
        self.import_excel = None

        # initalize the config as an empty dict
        self.config = {}

    # load the config file if it's already saved
    def load_config(self):
        try:
            with open(self.CONFIG_FILE, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
        return self.config
    

    def select_file(self):

        # Check if file path is already set in the configuration
        if "file_path" not in self.config:

            root_directory = tk.Tk()
            root_directory.withdraw()  # Hide the root window
            
            # Open directory dialog and allow the user to select a directory
            self.directory_path = filedialog.askdirectory(initialdir=self.initial_path, title="Choose the path where the Excel-file is that you want to read")
            #self.directory_path = filedialog.askdirectory(title="Choose the path where the Excel-file is that you want to read")
            #print(MainClass.initial_path)
            root_directory.destroy()  # Close the Tkinter window

            if self.directory_path is None:
                print("No directory selected.")
                return
            
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            
            # Open file dialog and allow the user to select a file from the chosen directory
            # self.filename_excel = filedialog.askopenfilename(initialdir=self.directory_path, title="Choose the Excel-file that you want to read", filetypes=[("Excel Files", "*.xlsx")])
            self.config["file_path"] = filedialog.askopenfilename(initialdir=self.directory_path, title="Choose the Excel-file that you want to read", filetypes=[("Excel Files", "*.xlsx")])
            
            # safe the filename into the filename_excel variabel 
            self.filename_excel = self.CONFIG_FILE['file_path']  
            root.destroy()  # Close the Tkinter window

            self.check_save_file(self.filename_excel)
            self.save_config()  # Save the updated configuration
            
                # Use the selected file path in further processing
            #print(f"Selected File: {self.config['file_path']}")
            print(f"Selected File: {self.config}")


    # save the new config file
    def save_config(self):
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self.config, f)    

    def check_save_file(self,filename_excel):
        name_without_extension = os.path.splitext(filename_excel)[0]
        print(name_without_extension)  # Output: data

        base_filename_excel = os.path.basename(name_without_extension)
        print(base_filename_excel)

        folder_path = name_without_extension

        # file path for the pickle file made out of the folder_path and the base_filename_excel variables
        file_path = f'{folder_path}/{base_filename_excel}.pkl'

        # Check if the folder already exists
        if not os.path.exists(folder_path):
            # Create the folder/directory
            os.mkdir(folder_path)
            print("Folder created:", base_filename_excel)
        else:
            print("Folder already exists:", base_filename_excel)

    
        try:
            # Try to load the DataFrame from the saved pickle file
            with open(file_path, 'rb') as file:
                import_excel = pickle.load(file)
                print('Loaded DataFrame from pickle file.')
                print("Import excel type: {}".format(type(import_excel)))

        except FileNotFoundError:
            # If the pickle file doesn't exist, read the Excel file
            try:
                import_excel = pd.read_excel(filename_excel, sheet_name='15min')
                print('Read DataFrame from Excel file.')
                # print("Import excel type {}".format(type(import_excel)))

                # Save the DataFrame to a binary file using pickle
                with open(file_path, 'wb') as file:
                    pickle.dump(import_excel, file)
                    # print('Saved DataFrame to pickle file.')

            except Exception as e:
                print(f'Error occurred: {e}')


        # print(help(VariablesCheck))



        return import_excel
    


# Start the code running #

if __name__ == '__main__':
    main_class = MainClass()
    plot_excel = PlotExcel()
    # print("filename", plot_excel.initial_path)
    variables_check = VariablesCheck()
        # try to load the config.json file
    variables_check.load_config()

    # main_class.select_directory()
    variables_check.select_file()
    import_excel = variables_check.check_save_file(variables_check.filename_excel)


    # plot_excel.plot_results(import_excel, import_excel_csv_np, import_excel_csv_np_cols)

# if __name__ == '__main__':

    plot_excel.start_dash_plot(import_excel)
    plot_excel.run_server()
