# import pickle
import pickle
from Task import Task,os
# import os


# if os.path.exists('instance.pkl'):
#     with open('instance.pkl', 'w') as pkl:
#         loaded_tasks =  dill.load(pkl)
# else:
#     print('there is not any file')
#     loaded_tasks = []

# for task in loaded_tasks:
#     print(task)

# task=Task("684630739", ["684630739"], "daily", "21310000", "11320000", "2023-09-01", "18:00", "24:00"),

# if not task.__str__() in [i.__str__() for i in loaded_tasks]:
#     loaded_tasks.append(task)
#     print('add task manually')

# with open('instance.pkl', 'wb') as f:
#     dill.dump(loaded_tasks, f)

Tasks=[
    Task("684630739", ["684630739"], "daily", "21310000", "11320000", "2023-09-01", "18:00:00", "23:59:59"),
    Task("684630739", ["684630739"], "daily", "11320000", "21310000", "2023-08-31", "06:00:00", "12:00:00"),
    Task("684630739", ["684630739"], "daily", "21310000", "11320000", "2023-09-02", "00:00:00", "03:00:00"),
]
for task in Tasks:
    task.get_data()
