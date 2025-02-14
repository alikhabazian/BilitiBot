
import pickle
from Task import Task,os

Tasks=[
    Task(creator = '684630739',receivers = ['684630739,229091667'],how_often = 'daily',orgin_city = 'تهران',destination_city = 'اصفهان',date = '2025-02-14',start_time = '17:00:00',end_time = '23:59:59',),

]

for task in Tasks:
    task.get_data_ali_baba()
    # task.get_data_snapp()
