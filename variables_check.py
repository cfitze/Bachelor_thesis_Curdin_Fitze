import pandas as pd
import os

from plot_excel import PlotExcel
from Read_excel_main import MainClass

class VariablesCheck2(MainClass):

    def __init__(self, filename_excel):
        self.filename_excel = filename_excel


    def check_file(self):
        name_without_extension = os.path.splitext(self.filename_excel)[0]
        print(name_without_extension)  # Output: data

        # Add a new extension to the filename
        filename_excel_cvs = name_without_extension + '.csv'
        print(filename_excel_cvs)  # Output: data.txt

        try:
            import_excel = pd.read_csv(filename_excel_cvs)
            print("Data loaded from CSV file.")
        except FileNotFoundError:
            # Read data from Excel sheet
            import_excel = pd.read_excel(self.filename_excel, sheet_name='15min')
            print("Data loaded from Excel sheet.")

            # Save the data as a CSV file
            import_excel.to_csv(filename_excel_cvs, index=True)
            print("Data saved as CSV file for faster access.")

        return import_excel
    
    def get_plot_excel_instance(self):
        return PlotExcel()