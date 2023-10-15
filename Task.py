from datetime import datetime, time
import requests
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()

BOT_TOKEN=bot_token = os.getenv("BOT_TOKEN")
# 21310000 isf 11320000 teh
class Task:
    def __init__(self, creator, receivers, how_often,orgin_city,destination_city,date,start_time,end_time,username=None,password=None,firstName=None,lastName=None,title='MR',nationalCode=None,notificationCellphoneNumber=None,alibabaToken=None,Task_id=None,mute=True):
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
        # -------------------
        self.mute=mute
        # -------------------
        self.username=username
        self.password=password
        self.firstName=firstName
        self.lastName=lastName
        self.title=title
        self.nationalCode=nationalCode
        self.notificationCellphoneNumber=notificationCellphoneNumber
        self.alibabaToken=alibabaToken
        self.Task_id=Task_id



    @staticmethod
    def get_task_fields():
        # This method returns a list of field names expected for a task.
        return [
            "creator",
            "receivers",
            "how_often",
            "orgin_city",
            "destination_city",
            "date",
            "start_time",
            "end_time"
        ]

    def get_CityCode_ali_baba(self,city):
        url = "https://ws.alibaba.ir/api/v1/bus/stations"
        querystring = {"filter":"containsall={ct:"+f"'{city}'"+"}"}
        response = requests.request("GET", url ,params=querystring)
        print(response.json())
        result=response.json()['result']['items']
        if len(result)>0:
            return result[0]['domainCode']

    def get_CityName_ali_baba(self,city):
        url = "https://ws.alibaba.ir/api/v1/bus/stations"
        querystring = {"filter":"containsall={ct:"+f"'{city}'"+"}"}
        response = requests.request("GET", url ,params=querystring)
        result=response.json()['result']['items']
        if len(result)>0:
            return result[0]['displayNames'][1]['value']

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
                if company=='alibaba':
                    try:
                        if self.username and self.password and self.firstName and self.lastName and self.title and self.nationalCode and self.notificationCellphoneNumber:

                            message += '\nit is url that I booked for you just pay it :'+self.book_ticket_alibaba(providerItemIds=available['proposalId'],username=self.username,password=self.password,firstName=self.firstName,lastName=self.lastName,title=self.title,nationalCode=self.nationalCode,notificationCellphoneNumber=self.notificationCellphoneNumber)

                    except Exception as e:
                        message += '\nthere is a problem in booking ticket for you'+str(e)

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
        # print(self.get_url_ali_baba())
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
        if not is_any and not self.mute:
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
        if not is_any and not self.mute:
            self.send_message(None,'snapp')



    def login_alibaba(self,username,password):
        # print('login_alibaba')
        url = "https://ws.alibaba.ir/api/v3/account/token"
        payload = {
            "emailOrPhone": f"{username}",
            "password": f"{password}"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        token = response.json()['result']['access_token']
        return token

    def get_last_ticket_alibaba(self,providerItemIds):
        # print('get_last_ticket_alibaba')
        url = f'https://ws.alibaba.ir/api/v1/bus/available/{providerItemIds}/seats'
        response = requests.request("GET", url)
        for item in response.json()['result']:
            if item['status'] == 'Available':
                # print(item['index'], item['status'])
                break
        return item['number']

    def poass_passenger_ddetail_alibaba(self,providerItemIds,token,firstName,lastName,title,seat,nationalCode):
        # print('poass_passenger_ddetail_alibaba')
        url = "https://ws.alibaba.ir/api/v1/coordinator/basket/items/bus"
        payload = {"providerItemIds": [f"{providerItemIds}"],
                   "firstName": firstName,
                   "lastName": lastName,
                   "firstNameEnglish": None,
                   "lastNameEnglish": None,
                   "title": title,
                   "seats": [seat],
                   "nationalCodes": [nationalCode]
                   }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.request("PUT", url, json=payload, headers=headers)
        basketId = response.json()['result']['basketId']
        return basketId

    def checkout_alibaba(self,token,basketId,notificationCellphoneNumber):
        # print('checkout_alibaba')
        url = f"https://ws.alibaba.ir/api/v2/coordinator/basket/{basketId}/checkout"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        payload = {"notificationEmail": "", "notificationCellphoneNumber": notificationCellphoneNumber}
        response = requests.request("POST", url, json=payload, headers=headers)
        orderId = response.json()['result']['orderId']
        return orderId


    def confirm_alibaba(self,token,orderId):
        # print('confirm_alibaba')
        url = f'https://ws.alibaba.ir/api/v1/coordinator/order/{orderId}/confirm'
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.request("POST", url, headers=headers)
        print(response.text)
        return response.json()["success"]

    def status_alibaba(self,token,orderId):
        # print('status_alibaba')
        url = f"https://ws.alibaba.ir/api/v2/coordinator/order/{orderId}/status"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        return response.json()["result"]['orderStatus']=="Confirmed"

    def pay_alibaba(self,orderId,token):
        # print('pay_alibaba')
        url = f'https://ws.alibaba.ir/api/v3/coordinator/order/{orderId}/pay-request'
        payload = {"redirectUrl": f"https://www.alibaba.ir/bus/{self.get_CityName_ali_baba(self.orgin_city)}-{self.get_CityName_ali_baba(self.destination_city)}/o6ti0e/{orderId}/issue",
                   "payRequestType": "PayByBank"}
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        return response.json()['result']['bankUrl']
    def book_ticket_alibaba(self,providerItemIds,username,password,firstName,lastName,title,nationalCode,notificationCellphoneNumber):
        if not self.alibabaToken:
            token=self.login_alibaba(username,password)
            print(token)
            try:
                mongodb_password = os.getenv("MONGODB_PASSWORD")
                uri = f"mongodb+srv://khabaziana:{mongodb_password}@cluster0.l4miazp.mongodb.net/?retryWrites=true&w=majority"
                client = MongoClient(uri, server_api=ServerApi('1'))
                #update token in mongo
                db = client.Biliti
                collection = db.Tasks
                collection.update_one({'_id':self.Task_id},{'$set':{'alibabaToken':token}})
                client.close()

            except:
                pass
            self.token=token
        else:
            token=self.alibabaToken
        print(token)
        seat=self.get_last_ticket_alibaba(providerItemIds)
        # print(seat)
        basketId= self.poass_passenger_ddetail_alibaba(providerItemIds,token,firstName,lastName,title,seat,nationalCode)
        # print(basketId)
        orderId=self.checkout_alibaba(token,basketId,notificationCellphoneNumber)
        # print(orderId)
        if self.confirm_alibaba(token,orderId):

            if self.status_alibaba(token,orderId):
                return self.pay_alibaba(orderId,token)








    

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
    task=Task(creator = '684630739',receivers = ['684630739'],how_often = 'daily',orgin_city = 'تهران',destination_city = 'اصفهان',date = '2023-10-17',start_time = '00:00:00',end_time = '23:59:59')
    task.get_data_ali_baba()
    

