from datetime import datetime, time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")
# 21310000 isf 11320000 teh
class Task:
    def __init__(self, creator, receivers, how_often,orginCityCode,destinationCityCode,date,start_time,end_time):
        self.creator = creator
        self.receivers = receivers
        self.how_often = how_often
        self.orginCityCode=orginCityCode
        self.destinationCityCode=destinationCityCode
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def get_url(self):
        return f'https://ws.alibaba.ir/api/v2/bus/available?orginCityCode={self.orginCityCode}&destinationCityCode={self.destinationCityCode}&requestDate={self.date}&passengerCount=1'
    
    def send_message(self,available):
        if available:
            for CHAT_ID in self.receivers:
                # API endpoint
                api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                deleted_value = {key: value for key, value in available.items() if key != 'proposalId'}
                message = "I found ticket for you\ncurrent time is "+str(datetime.now().time())+'\n'+str(deleted_value)
                message += '\n'+self.__str__()
                params = {
                    'chat_id': CHAT_ID,
                    'text': message
                }

                response = requests.post(api_url, json=params)

                if response.status_code == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message. Status code:", response.status_code)
                    print("Response:", response.text)
        else:
            for CHAT_ID in self.receivers:
                api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                message = "there is not any ticket available"
                message += '\n'+self.__str__()
                params = {
                        'chat_id': CHAT_ID,
                        'text': message
                }
                response = requests.post(api_url, json=params)
                if response.status_code == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message. Status code:", response.status_code)
                    print("Response:", response.text)

    def get_data(self):
        request = requests.get(self.get_url())
        data=request.json()['result']
        availableList=data['availableList']
        from_time_str = self.start_time
        from_time_obj = datetime.strptime(from_time_str, '%H:%M:%S').time()
        to_time_str = self.end_time
        to_time_obj = datetime.strptime(to_time_str, '%H:%M:%S').time()

        is_any=False
        for available in availableList:
            time_str=available['departureDateTime'].split('T')[1]
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            if time_obj>=from_time_obj and  time_obj<=to_time_obj:
                if available['availableSeats']>0:
                    is_any=True
                    self.send_message(available)
        if not is_any:
            pass
            #self.send_message(None)

    def __str__(self):
        return '\n'.join([
            f"Task created by {self.creator}, ",
            f"receivers: {', '.join(self.receivers)}, ",
            f"how often: {self.how_often}, ",
            f"origin city code: {self.orginCityCode}, ",
            f"destination city code: {self.destinationCityCode}, ",
            f"date: {self.date}, ",
            f"start time: {self.start_time}, ",
            f"end time: {self.end_time}"
        ])
        

