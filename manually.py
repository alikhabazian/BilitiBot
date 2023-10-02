
import pickle
from Task import Task,os

Tasks=[
    Task(creator = '684630739',receivers = ['684630739','229091667'],how_often = 'daily',orgin_city = 'تهران',destination_city = 'اصفهان',date = '2023-10-02',start_time = '21:00:00',end_time = '23:59:59',),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='تهران',destination_city='اصفهان', date='2023-10-03', start_time='00:00:00', end_time='10:00:00', ),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='اصفهان',destination_city='تهران', date='2023-10-06', start_time='20:00:00', end_time='23:59:59', ),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='اصفهان',destination_city='تهران', date='2023-10-07', start_time='00:00:00', end_time='05:00:00', ),

]

for task in Tasks:
    task.get_data_ali_baba()
    task.get_data_snapp()
