
import matplotlib.pyplot as plt

from variables_check import VariablesCheck
from Read_excel_main import MainClass

class PlotExcel(MainClass):

    def __init__(self, filename_excel):
        self.filename_excel = filename_excel

    def plot_results(self, import_excel_DateTime, import_excel_self_consumption):

        variables_common_instance = VariablesCheck(self.filename_excel)
        import_excel = variables_common_instance.check_file()

        import_excel_DateTime = import_excel['DateTime']
        import_excel_self_consumption = import_excel['SelfConsumption [kWh]']
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