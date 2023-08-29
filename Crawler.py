import pickle
from Task import Task
# Load the list of tasks from the pickle file
with open('tasks.pkl', 'rb') as f:
    loaded_tasks = pickle.load(f)

for task in loaded_tasks:
    Task.get_data()
