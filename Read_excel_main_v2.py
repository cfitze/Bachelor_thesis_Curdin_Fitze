
import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
import tkinter as tk
from TkinterDnD2 import *
# Dash application with interactivity
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
# to save the import_excel Data from the Excel-file into a binary pickle file
import pickle  


#.mro() You can actually check a class’s MRO by calling the mro method on the class, which gives you the list of classes in the order of how a method is resolved.


# Main class
class MainClass:

    # Define the filename
    
    #filename_excel= 'BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.xlsx'
    #initial_path = '"C:/Users/cfitz/FHNW/P-6-23FS_M365 - General/04_Diverse/Github_repository"'
    #initial_path = '"C:/Users/cfitz"'
    #print(initial_path)
    # import_excel_csv_np = None
    
    def __init__(self):

        # self.filename_excel = None
        #self.initial_path = '"C:/Users/cfitz/FHNW/P-6-23FS_M365 - General/04_Diverse/Github_repository"'
        self.initial_path = '"C:/Users/cfitz"'
        self.directory_path = None
        self.import_excel = None

        self.import_excel_csv_np = None
        self.filename_excel_npy = None
        self.rownumber1 = None


        #print(self.initial_path)


    def select_directory(self):
        root_directory = tk.Tk()
        root_directory.withdraw()  # Hide the root window
        
        # Open directory dialog and allow the user to select a directory
        self.directory_path = filedialog.askdirectory(initialdir=self.initial_path, title="Choose the path where the Excel-file is that you want to read")
        #self.directory_path = filedialog.askdirectory(title="Choose the path where the Excel-file is that you want to read")
        #print(MainClass.initial_path)
        root_directory.destroy()  # Close the Tkinter window


    def select_file(self):
        if self.directory_path is None:
            print("No directory selected.")
            return
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Open file dialog and allow the user to select a file from the chosen directory
        self.filename_excel = filedialog.askopenfilename(initialdir=self.directory_path, title="Choose the Excel-file that you want to read", filetypes=[("Excel Files", "*.xlsx")])
        root.destroy()  # Close the Tkinter window

    

    def read_data_from_excel(self):
        #VariablesCheck.plot_re
        print("Es werden nun die Daten aus dem Excel-File eingelesen.")

        variables_check = VariablesCheck(self.filename_excel)
        MainClass.import_excel = variables_check.check_file()

        # VariablesCheck.check_file()
        # plot_excel_instance = PlotExcel()
        # plot_excel_instance.plot_results()


#Create an instance of the MainClass

#print(main_class.directory_path)
#print(main_class.filename)

#print(help(MainClass))

class PlotExcel(MainClass):

    # def __init__(self, filename_excel,import_excel_DateTime,import_excel_self_consumption):
    def __init__(self):
        super().__init__()

        # self.import_excel_csv_np = import_excel_csv_np
        self.import_excel_DateTime = None
        self.import_excel_self_consumption = None
        # self.filename_excel_npy

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
        # Assign the import_excel to the class variable
        # self.import_excel = import_excel

        columns_available = import_excel.columns.tolist()


        # Convert DateTime column to datetime format
        datetime_column = pd.to_datetime(import_excel['DateTime'])

        # subset_months = datetime_column[datetime_column.dt.year == 2023].dt.month


        # # Set initial values for the slider and dropdown menu

        initial_selected_columns = [import_excel.columns[1:]]  # Set the initial selected column except the first DateTime column

        # Get the first and last dates from the DateTime column
        first_date = import_excel['DateTime'].iloc[0]
        last_date = import_excel['DateTime'].iloc[-1]

        # Convert first and last dates to Swiss time format
        swiss_time_format = '%d.%b.%Y'
        initial_start_date_index = first_date.strftime(swiss_time_format)
        initial_end_date_index = last_date.strftime(swiss_time_format)

        # Create marks dictionary with English month names
        # month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        # Create marks dictionary with German month names
        month_names = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

# Start the Application
        # Create the Dash application
        app = dash.Dash(__name__)

        # Define the layout of the application
        app.layout = html.Div(children=[
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
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': column, 'value': column} for column in import_excel.columns[1:]],
                multi=True,  # Set multi=True to allow selecting multiple datasets
                value=initial_selected_columns  # Set the initial value to the first column
            ),
            dcc.Graph(
                id='3d-bar-plot',
                figure=self.create_plot_figure(import_excel, datetime_column ,initial_start_date_index, initial_end_date_index, initial_selected_columns)  # Pass the initial date and empty dataset list
            )
        ])

        # Define the callback to update the plot on the selected columns
        @app.callback(
            dash.dependencies.Output('3d-bar-plot', 'options'),
            [dash.dependencies.Input('column-dropdown', 'value')]
        )
        def update_datasets(selected_columns):
            options = []
            for column in selected_columns:
                selected_columns= import_excel[column]  # Get the data for the selected column
                options.extend([{'label': dataset, 'value': dataset} for dataset in selected_data])
            return options

        # Define the callback to update the plot based on the selected date range
        @app.callback(
            dash.dependencies.Output('3d-bar-plot', 'figure'),
            [dash.dependencies.Input('date-slider', 'value')]
            # dash.dependencies.Input('3d-bar-plot', 'options')]
        )
        def update_plot(selected_date_range):
            start_date_index, end_date_index = selected_date_range
            start_date = datetime_column[start_date_index]
            end_date = datetime_column[end_date_index]
            selected_columns = dash.callback_context.inputs['column-dropdown.value']
            return self.create_plot_figure(import_excel, datetime_column, start_date, end_date, selected_columns)

        # Define the callback to display the selected start and end dates
        @app.callback(
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
        app.run_server(debug=True, mode='inline', dev_tools_ui=True)


    def create_plot_figure(self, import_excel_figure, datetime_column ,start_date, end_date, selected_columns):

        # Filter the data based on the selected date range
        filtered_data_dates = datetime_column[
            # (import_excel_figure['DateTime'] >= start_date) & (import_excel_figure['DateTime'] <= end_date)]
            (datetime_column >= start_date) & (datetime_column <= end_date)]
        

        import_excel_figure_without_datetime = import_excel_figure[1:]

        # Filter the data based on the selected columns
        filtered_data_columns = filtered_data[filtered_data['dataset'].isin(selected_columns)]

        # Create the 3D bar plot figure
        figure = {
            'data': [
                go.Bar(
                    x=filtered_data_dates,
                    y=filtered_data_columns,
                    z=filtered_data['z'],
                    text=filtered_data['text'],
                    hoverinfo='text',
                    marker=dict(color='blue'),
                    name=f'Dataset - {date}'
                ) for date in filtered_data['DateTime']
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
    def __init__(self, rownumber1, rownumber2):

        super().__init__()

        self.rownumber1 = rownumber1
        self.rownumber2 = rownumber2

    def check_file(self,filename_excel):
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

        # # Add a new extension to the filename for .cvs
        # # filename_excel_cvs = name_without_extension + '.csv'
        # filename_excel_cvs = folder_path + '/' + base_filename_excel + '.csv'
        # print(filename_excel_cvs)  # Output: data.txt

        
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

        # try:

        #     # Read data from Excel sheet  
        #     import_excel = pd.read_excel(filename_excel, sheet_name='15min')
        #     print("Data loaded from xlsx file.")

            
        # except FileNotFoundError:

        #     print("The File could not be found.")

        #     # print(help(VariablesCheck))



        return import_excel
    


# Start the code running #
print("Input the rows you want to plot; for now max 2")
main_class = MainClass()
plot_excel = PlotExcel()
print("filename", plot_excel.initial_path)
variables_check = VariablesCheck(1, 2)



main_class.select_directory()
main_class.select_file()
# main_class.create_folder()
import_excel = variables_check.check_file(main_class.filename_excel)
# main_class.read_data_from_excel()


# print("rows shape: ",np.shape(import_excel_csv_np_cols))
# print("other shape", np.shape(import_excel_csv_np))


# plot_excel.plot_results(import_excel, import_excel_csv_np, import_excel_csv_np_cols)
plot_excel.start_dash_plot(import_excel)