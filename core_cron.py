from crontab import CronTab
with CronTab(user=True) as cron:
    job = cron.new(command='/Users/ali/Documents/Alibaba/myenv/bin/python /Users/ali/Documents/Alibaba/bot_main.py')
    job.minute.every(1)
print('cron.write() was just executed')

with CronTab(user=True) as cron:
    # Remove all jobs that match the specified command
    cron.remove_all(command='/Users/ali/Documents/Alibaba/myenv/bin/python /Users/ali/Documents/Alibaba/bot_main.py')
print('Cron job(s) removed')