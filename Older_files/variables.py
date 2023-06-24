#from Testing_1 import MainClass

'''''
class SubClass(MainClass):
    def __init__(self):
        super().__init__()

'''''
# Subclass variables
class Variables:
    def __init__(self, main_instance):
        self.main_instance = main_instance
        
    def process_data(self):
        # Check if 'data' variable is available in the subclass
        if self.main_instance.import_excel is None:
            print("Data not available in subclass. Reading from Excel sheet...")
            self.main_instance.read_data_from_excel()
        
        # Perform further processing on the data
        print("Data processing completed.")