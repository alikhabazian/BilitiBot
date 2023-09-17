
import pickle
from Task import Task,os

Tasks=[
    Task(creator = '684630739',receivers = ['684630739','1952566514','229091667'],how_often = 'daily',orgin_city = 'تهران',destination_city = 'اصفهان',date = '2023-09-20',start_time = '20:00:00',end_time = '23:59:59',),
    Task(creator='684630739', receivers=['684630739','1952566514','229091667'], how_often='daily', orgin_city='تهران', destination_city='اصفهان',date='2023-09-21', start_time='00:00:00', end_time='02:00:00', ),
    Task(creator='684630739', receivers=['684630739','1952566514','229091667'], how_often='daily', orgin_city='اصفهان', destination_city='تهران', date='2023-09-22', start_time='20:00:00', end_time='23:59:59', ),
    Task(creator='684630739', receivers=['684630739','1952566514','229091667'], how_often='daily', orgin_city='اصفهان', destination_city='تهران',date='2023-09-23', start_time='00:00:00', end_time='02:00:00', ),

]

for task in Tasks:
    task.get_data_ali_baba()
    task.get_data_snapp()
