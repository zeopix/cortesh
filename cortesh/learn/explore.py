from cortesh.process.memory.memory import Memory

class Explorer:
    def __init__(self):
        self.memory = Memory('git')
        self.data = None

    def load_data(self):
        self.data = self.memory.get_all()  # Assuming this method exists to fetch all data

    def clear_data(self):
        self.data = None

    def display_data(self):
        if self.data is not None:
            print("Data:")
            for item in self.data:
                print(item)  # Display each item in the data
        else:
            print("No data available")
