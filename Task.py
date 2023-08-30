from datetime import datetime, time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")
# 21310000 isf 11320000 teh
class Task:
    def __init__(self, creator, receivers, how_often,orgin_city,destination_city,date,start_time,end_time):
        self.creator = creator
        self.receivers = receivers
        self.how_often = how_often
        # self.orginCityCode=orginCityCode
        # self.destinationCityCode=destinationCityCode
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.orgin_city=orgin_city
        self.destination_city=destination_city

    def get_CityCode_ali_baba(self,city):
        url = "https://ws.alibaba.ir/api/v1/bus/stations"
        querystring = {"filter":"containsall={ct:"+f"'{city}'"+"}"}
        response = requests.request("GET", url ,params=querystring)
        result=response.json()['result']['items']
        if len(result)>0:
            return result[0]['domainCode']

    def get_CityCode_snapp(self,city):
        url = "https://www.snapptrip.com/bus/api/listing/v1/cities"

        querystring = {"query":city}

        response = requests.request("GET", url, params=querystring)
        result=response.json()
        if len(result)>0:
            return  (result[0]['id'])
        



    def get_url_ali_baba(self):
        return f'https://ws.alibaba.ir/api/v2/bus/available?orginCityCode={self.get_CityCode_ali_baba(self.orgin_city)}&destinationCityCode={self.get_CityCode_ali_baba(self.destination_city)}&requestDate={self.date}&passengerCount=1'
    
    def get_url_snapp(self):
        return f'https://www.snapptrip.com/bus/api/listing/v1/availability/{self.get_CityCode_snapp(self.orgin_city)}/to/{self.get_CityCode_snapp(self.destination_city)}/on/{self.date}'
    
    def send_message(self,available,company):
        if available:
            for CHAT_ID in self.receivers:
                # API endpoint
                api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                deleted_value = {key: value for key, value in available.items() if key != 'proposalId'}
                message = f"I found ticket for you in {company}\ncurrent time is "+str(datetime.now().time())+'\n'+str(deleted_value)
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
                message = f"there is not any ticket available in {company}"
                message += '\n'+self.__str__()
                params = {
                        'chat_id': CHAT_ID,
                        'text': message,
                        'disable_notification': True
                }
                response = requests.post(api_url, json=params)
                if response.status_code == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message. Status code:", response.status_code)
                    print("Response:", response.text)

    
    
    def get_data_ali_baba(self):
        # print(self.get_url_ali_baba())
        request = requests.get(self.get_url_ali_baba())
        data=request.json()['result']
        # print(data)
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
                    self.send_message(available,'alibaba')
        if not is_any:
            self.send_message(None,'alibaba')
    
    def get_data_snapp(self):
        request = requests.get(self.get_url_snapp())
        data=request.json()
        availableList=data['solutions']
        from_time_str = self.start_time
        from_time_obj = datetime.strptime(from_time_str, '%H:%M:%S').time()
        to_time_str = self.end_time
        to_time_obj = datetime.strptime(to_time_str, '%H:%M:%S').time()

        is_any=False
        for available in availableList:
            time_str=available['departureTime']
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            if time_obj>=from_time_obj and  time_obj<=to_time_obj:
                if available['capacity']>0:
                    is_any=True
                    self.send_message(available,'snapp')
        if not is_any:
            self.send_message(None,'snapp')

    

    def __str__(self):
        return '\n'.join([
            f"Task created by {self.creator}, ",
            f"receivers: {', '.join(self.receivers)}, ",
            f"how often: {self.how_often}, ",
            f"origin city code: {self.orgin_city}, ",
            f"destination city code: {self.destination_city}, ",
            f"date: {self.date}, ",
            f"start time: {self.start_time}, ",
            f"end time: {self.end_time}"
        ])
        

if __name__ == "__main__":
    task=Task("684630739", ["684630739",'229091667'], "daily", "21310000",'اصفهان' ,"11320000", "2023-09-08", "18:00:00", "23:59:59")
    a=task.get_CityCode_snapp('اصفهان')
    print(a,type(a))
    

