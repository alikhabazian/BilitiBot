import requests
from datetime import datetime, time


BOT_TOKEN = '6470883702:AAFDbB8C1Al1IycmjEQECadSVZYWfli5gY8'

# Replace 'CHAT_ID' with the chat ID you want to send the message to
CHAT_ID = '684630739'








x = requests.get('https://ws.alibaba.ir/api/v2/bus/available?orginCityCode=21310000&destinationCityCode=11320000&requestDate=2023-08-25&passengerCount=1')
data=x.json()['result']
availableList=data['availableList']
# print(availableList)
# print(len(availableList))

other_time_str = '20:00:00'
other_time_obj = datetime.strptime(other_time_str, '%H:%M:%S').time()



for available in availableList:
    # if available['availableSeats']>0:
    #     print()
    time_str=available['departureDateTime'].split('T')[1]
    time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
    if time_obj>=other_time_obj:
        if available['availableSeats']>=0:
            # API endpoint
            api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            deleted_value = available.pop('proposalId')
            message = "I found ticket for you\ncurrent time is "+str(datetime.now().time())+'\n'+str(available)
            # Parameters for the API request
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
        print(available['availableSeats'])
        print(time_obj)