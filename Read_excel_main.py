
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

    def start_dash_plot(self,import_excel):

        # From the VariablesCheck class and the check_file method
        self.import_excel = import_excel
        # 

        # processed_data = self.process_data()


        dates = import_excel["DateTime"]  # Get the dates from processed data

        # skip some DateTime members of the Array for no overloading  --        # skip_interval = # subset_dates = dates[::skip_interval]
        datetime_column = pd.to_datetime(import_excel['datetime_column'])


        subset_months = datetime_column[datetime_column.dt.year == 2023].dt.month

        # Create marks dictionary with English month names
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


        # # Get the datetime column as a Pandas Series and convert to desired format
        # datetime_column = pd.to_datetime(df['datetime_column'], format='%Y-%m-%d %H:%M:%S')

        # # Filter and retrieve the subset of datetimes for the year 2023
        # subset_datetimes = datetime_column[datetime_column.dt.year == 2023]

        # get the columns of the excel file
        columns = import_excel.columns.tolist()
        datasets = import_excel[columns].keys()  # Get the available datasets
        # data_array = df[column_name].tolist()

        # print(keys)

        # keys_list = list(keys)
        # print(keys_list)  # Output: ['name', 'age', 'city']

        # Create the Dash application
        app = dash.Dash(__name__)



        # Define the layout of the application
        app.layout = html.Div(children=[
            html.H1(children='3D Interactive Bar Plot'),
            dcc.RangeSlider(
                id='date-slider',
                # marks = {i: {'label': month_names[i-1]} for i in month_names},
                marks = {i: {'label': month_names[i-1]} for i in subset_months},
                # marks={i: {'label': date} for i, date in enumerate(dates)},
                min=0,
                max=len(dates) - 1,
                value=[0, len(dates) - 1]  # Set the initial range to include all dates
            ),
            html.Div(id='selected-dates-output'),  # Placeholder for displaying selected start and end dates
            dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': column, 'value': column} for column in columns],
                multi=False,  # Set multi=True to allow selecting multiple datasets
                value=columns[0]  # Set the initial value to the first column
            ),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[],
                multi=True  # Allow selecting multiple datasets
            ),
            dcc.Graph(
                id='3d-bar-plot',
                figure=self.create_plot_figure(processed_data, dates[0], [])  # Pass the initial date and empty dataset list
            )
        ])

        # Define the callback to update the available datasets based on the selected column
        @app.callback(
            dash.dependencies.Output('dataset-dropdown', 'options'),
            [dash.dependencies.Input('column-dropdown', 'value')]
        )
        def update_datasets(column):
            selected_data = processed_data['data'][column]  # Get the data for the selected column
            return [{'label': dataset, 'value': dataset} for dataset in selected_data]

        # Define the callback to update the plot based on the selected date range and datasets
        @app.callback(
            dash.dependencies.Output('3d-bar-plot', 'figure'),
            [dash.dependencies.Input('date-slider', 'value'),
             dash.dependencies.Input('dataset-dropdown', 'value')]
        )
        def update_plot(selected_date_range, selected_datasets):
            start_date_index, end_date_index = selected_date_range
            start_date = dates[start_date_index]
            end_date = dates[end_date_index]
            return self.create_plot_figure(processed_data, start_date, end_date, selected_datasets)

        # Define the callback to display selected start and end dates
        @app.callback(
            dash.dependencies.Output('selected-dates-output', 'children'),
            [dash.dependencies.Input('date-slider', 'value')]
        )
        def display_selected_dates(selected_date_range):
            start_date_index, end_date_index = selected_date_range
            start_date = dates[start_date_index]
            end_date = dates[end_date_index]
            return f'Selected Dates: {start_date} - {end_date}'

        # Run the Dash application
        app.run_server(debug=True,mode='inline',dev_tools_ui=True,)

                        # dev_tools_hot_reload=True,  --> would be interesting to add later

                # app.run_server(
                # debug=True,
                # port=8050,
                # host='0.0.0.0',
                # dev_tools_ui=True,
                # dev_tools_hot_reload=True,
                # ev_tools_hot_reload_interval=1000,
                # dev_tools_silence_routes_logging=False,
                # mode='inline'
                # )


    def create_plot_figure(self, processed_data, start_date, end_date, selected_datasets):
        filtered_data = processed_data['data']

        # Filter the data based on the selected date range
        filtered_data = {date: data for date, data in filtered_data.items() if start_date <= date <= end_date}

        # Filter the data based on the selected datasets
        filtered_data = {date: data for date, data in filtered_data.items() if data['dataset'] in selected_datasets}

        # Create the 3D bar plot figure
        figure = {
            'data': [
                go.Bar(
                    x=filtered_data[date]['x'],
                    y=filtered_data[date]['y'],
                    z=filtered_data[date]['z'],
                    text=filtered_data[date]['text'],
                    hoverinfo='text',
                    marker=dict(color='blue'),
                    name=f'Dataset - {date}'
                    # opacity=0.7 if dataset == selected_dataset else 0.3  # Set opacity based on the selected dataset
                ) for date in filtered_data
            ],
            'layout': go.Layout(
                scene=dict(
                    xaxis=dict(title='X-axis'),
                    yaxis=dict(title='Y-axis'),
                    zaxis=dict(title='Z-axis')
                ),
                barmode='group',
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

        folderpath = name_without_extension

        # Check if the folder already exists
        if not os.path.exists(folderpath):
            # Create the folder/directory
            os.mkdir(folderpath)
            print("Folder created:", base_filename_excel)
        else:
            print("Folder already exists:", base_filename_excel)


        # Add a new extension to the filename for .cvs
        # filename_excel_cvs = name_without_extension + '.csv'
        filename_excel_cvs = folderpath + '/' + base_filename_excel + '.csv'
        print(filename_excel_cvs)  # Output: data.txt

        # Add a new extension to the filename for .npy
        # filename_excel_npy = name_without_extension + '.npy'
        filename_excel_npy = folderpath + '/' + base_filename_excel + '.npy'
        print(filename_excel_npy)  # Output: data.txt

        # Add a new extension to the filename for .npy for the chosen rows
        rows_str = "_{}_{}".format(self.rownumber1, self.rownumber2)
        print(rows_str)
        filename_excel_npy_cols = folderpath + base_filename_excel + rows_str + '.npy'
        print(filename_excel_npy_cols)  # Output: data.txt

        try:
            import_excel = pd.read_csv(filename_excel_cvs)
            print("Data loaded from CSV file.")

            # change to a numpy array
            import_excel_csv_np = import_excel.to_numpy()

            print(np.shape(import_excel_csv_np))
            array_count = sum(len(row) for row in import_excel_csv_np)
            print(array_count)

            # Save the array
            np.save(filename_excel_npy, import_excel_csv_np)


            # change to a numpy array for the chosen rows
            import_excel_csv_np_cols = import_excel_csv_np[:,[self.rownumber1, self.rownumber2]]

             # Save the array fo the chosen rows
            np.save(filename_excel_npy_cols, import_excel_csv_np_cols)
            
        except FileNotFoundError:
            # Read data from Excel sheet
            # import_excel = pd.read_excel(self.filename_excel, sheet_name='15min')
            import_excel = pd.read_excel(filename_excel, sheet_name='15min')

            print("Data loaded from Excel sheet.")

            # Save the data as a CSV file
            import_excel.to_csv(filename_excel_cvs, index=True)
            print("Data saved as CSV file for faster access.")

            # Umwandlung in ein numpy-Array
            import_excel_csv_np = import_excel.to_numpy()


            # Save the array
            np.save(filename_excel_npy, import_excel_csv_np)

            # change to a numpy array for the chosen rows
            import_excel_csv_np_cols = import_excel_csv_np[:,[self.rownumber1, self.rownumber2]]
    

            # Save the array fo the chosen rows
            np.save(filename_excel_npy_cols, import_excel_csv_np_cols)



            # print(help(VariablesCheck))

        return import_excel, import_excel_csv_np, import_excel_csv_np_cols
    
    def get_plot_excel_instance(self):
        return PlotExcel()
    



print("Input the rows you want to plot; for now max 2")
main_class = MainClass()
plot_excel = PlotExcel()
print("filename", plot_excel.initial_path)
variables_check = VariablesCheck(1, 2)



main_class.select_directory()
main_class.select_file()
# main_class.create_folder()
import_excel, import_excel_csv_np, import_excel_csv_np_cols = variables_check.check_file(main_class.filename_excel)
# main_class.read_data_from_excel()


print("rows shape: ",np.shape(import_excel_csv_np_cols))
print("other shape", np.shape(import_excel_csv_np))


plot_excel.plot_results(import_excel, import_excel_csv_np, import_excel_csv_np_cols)
# plot_excel.start_dash_plot(import_excel)