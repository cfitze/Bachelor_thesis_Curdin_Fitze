
import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import os


#from variables import Variables

# Define the filename
filename_excel= 'BA_23FS_Curdin_Fitze_5_7_9_11_13_TSextract.xlsx'

# Main class
class MainClass:
    def __init__(self):
        self.import_excel = None

    def read_data_from_excel(self):

            name_without_extension = os.path.splitext(filename_excel)[0]
            print(name_without_extension)  # Output: data

            # Add a new extension to the filename
            filename_excel_cvs = name_without_extension + '.csv'
            print(filename_excel_cvs)  # Output: data.txt

            '''''
            self.import_excel = pd.read_excel(self.filename_excel,sheet_name= '15min')
            print("Data loaded from Excel sheet.")
            import_excel_DateTime = self.import_excel['DateTime']
            import_excel_self_consumption= self.import_excel['SelfConsumption [kWh]']
            '''''
            

            try:
                self.import_excel = pd.read_csv(filename_excel_cvs)
                print("Data loaded from CSV file.")
            except FileNotFoundError:
                # Read data from Excel sheet
                self.data = pd.read_excel(filename_excel,sheet_name= '15min')
                print("Data loaded from Excel sheet.")
                
                # Save the data as a CSV file
                self.data.to_csv(filename_excel_cvs, index=True)
                print("Data saved as CSV file for faster access.")

            #self.import_excel = pd.read_excel(filename_excel,sheet_name= '15min')
            print("Data loaded from Excel sheet.")
            import_excel_DateTime = self.import_excel['DateTime']
            import_excel_self_consumption= self.import_excel['SelfConsumption [kWh]']


            #return import_excel_self_consumption ,import_excel_DateTime

            self.plot_results(import_excel_DateTime, import_excel_self_consumption)

    def plot_results(self, import_excel_DateTime, import_excel_self_consumption):
        #plotFigure =plt.figure()
        plt.figure(figsize=(12, 8))  # Set the width and height of the figure window
        plt.plot(import_excel_DateTime, import_excel_self_consumption)
        plt.xlabel('Date Time') #Sets the label for the x-axis.
        plt.ylabel('Self consumption [kWh]') #Sets the label for the y-axis.
        plt.title('Plot figure') #Sets the title for the plot.
        plt.grid(True) #Adds a grid to the plot.

        # Set the position and size of the first figure window
        #plotFigure.canvas.manager.window.setGeometry(100, 100, 800, 600)

        #plt.show()

        # Toggle full-screen mode
        #plt.get_current_fig_manager().full_screen_toggle()
        # Create a plot and set the figure size

        #plotBar= plt.figure(figsize=(12, 8))  # Set the width and height of the figure window
        plt.figure(figsize=(12, 8))  # Set the width and height of the figure window
        plt.bar(import_excel_DateTime, import_excel_self_consumption)
        plt.xlabel('Date Time') #Sets the label for the x-axis.
        plt.ylabel('Self consumption [kWh]') #Sets the label for the y-axis.
        plt.title('Plot bar') #Sets the title for the plot.
        plt.grid(True) #Adds a grid to the plot.

        # Set the position and size of the second figure window
        #plotBar.canvas.manager.window.setGeometry(500, 100, 800, 600)

        plt.show()



# Create an instance of the MainClass
main_instance = MainClass()

# Call the method to process data using SubClass
#subclass_instance = Variables(main_instance)
#subclass_instance.process_data()

'''''
from os import path

file_path = path.join('my_directory', 'my_file.txt')
print(file_path)

if path.exists(file_path):
    print('File exists')
else:
    print('File does not exist')

'''''