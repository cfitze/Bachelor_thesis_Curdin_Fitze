
import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from TkinterDnD2 import *

# from tkinterdnd2 import DND_FILES, TkinterDnD
# import tkinterdnd2 as tk2
# from tkinterdnd2 import DnD

# import tkinterdnd2
# try:
#     from Tkinter import *
# except ImportError:
#     from tkinter import *


#.mro() You can actually check a class’s MRO by calling the mro method on the class, which gives you the list of classes in the order of how a method is resolved.

#from variables import Variables

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

    def plot_results(self,import_excel_csv_np):

        #variables_common_instance = VariablesCheck(self.filename_excel)
        #import_excel = variables_common_instance.check_file()
        # import_excel = VariablesCheck.check_file()

        print("Please wait...")

        #plotFigure =plt.figure()
        plt.figure(figsize=(12, 8))  # Set the width and height of the figure window

        # plt.plot(self.import_excel_DateTime, self.import_excel_self_consumption)
        # plt.plot(import_excel_csv_np[:,1], import_excel_csv_np[:,2])
        # print(import_excel_csv_np)
        rows = np.arange(0,10000)
        plt.scatter(import_excel_csv_np[rows,1], import_excel_csv_np[rows,2], s=1)
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
        filename_excel_npy_rows = folderpath + base_filename_excel + rows_str + '.npy'
        print(filename_excel_npy_rows)  # Output: data.txt

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
            import_excel_csv_np_rows = import_excel_csv_np[:,[self.rownumber1, self.rownumber2]]

             # Save the array fo the chosen rows
            np.save(filename_excel_npy_rows, import_excel_csv_np_rows)
            
        except FileNotFoundError:
            # Read data from Excel sheet
            import_excel = pd.read_excel(self.filename_excel, sheet_name='15min')

            print("Data loaded from Excel sheet.")

            # Save the data as a CSV file
            import_excel.to_csv(filename_excel_cvs, index=True)
            print("Data saved as CSV file for faster access.")

            # Umwandlung in ein numpy-Array
            import_excel_csv_np = import_excel.to_numpy()


            # Save the array
            np.save(filename_excel_npy, import_excel_csv_np)



            # print(help(VariablesCheck))

        return import_excel_csv_np
    
    def get_plot_excel_instance(self):
        return PlotExcel()
    



print("Input the rows you want to plot; for now max 2")
main_class = MainClass()
plot_excel = PlotExcel()
variables_check = VariablesCheck(1, 2)
# variables_check.check_file()
# plot_excel = PlotExcel()

main_class.select_directory()
main_class.select_file()
# main_class.create_folder()
import_excel_csv_np = variables_check.check_file(main_class.filename_excel)
# main_class.read_data_from_excel()

# plot_excel = PlotExcel()
plot_excel.plot_results(import_excel_csv_np)




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