
import pickle
from Task import Task,os

Tasks=[
    Task(creator = '684630739',receivers = ['684630739','229091667'],how_often = 'daily',orgin_city = 'تهران',destination_city = 'اصفهان',date = '2023-09-27',start_time = '21:00:00',end_time = '23:59:59',),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='تهران',destination_city='اصفهان', date='2023-09-28', start_time='00:00:00', end_time='02:00:00', ),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='اصفهان',destination_city='تهران', date='2023-09-28', start_time='22:00:00', end_time='23:59:59', ),
    Task(creator='684630739', receivers=['684630739', '229091667'], how_often='daily', orgin_city='اصفهان',destination_city='تهران', date='2023-09-29', start_time='00:00:00', end_time='05:00:00', ),

]

for task in Tasks:
    task.get_data_ali_baba()
    task.get_data_snapp()
