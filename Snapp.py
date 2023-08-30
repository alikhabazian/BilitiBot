import requests
from datetime import datetime, time


BOT_TOKEN = '6470883702:AAFDbB8C1Al1IycmjEQECadSVZYWfli5gY8'

# Replace 'CHAT_ID' with the chat ID you want to send the message to
CHAT_IDs = ['684630739','229091667']

# URL: https://www.snapptrip.com/bus/api/listing/v1/availability/21310000/to/11320000/on/2023-09-02
# 21310000 isf
# 11320000 teh
url='https://www.snapptrip.com/bus/api/listing/v1/availability/41310000/to/11320000/on/2023-08-31'

x = requests.get(url)
availableList=x.json()['solutions']


other_time_str = '20:00:00'
other_time_obj = datetime.strptime(other_time_str, '%H:%M:%S').time()


is_any=False
for available in availableList:
    # if available['availableSeats']>0:
    #     print()
    time_str=available['departureTime']
    time_obj = datetime.strptime(time_str, '%H:%M').time()
    if time_obj>=other_time_obj:
        if available['capacity']>0:
            for CHAT_ID in CHAT_IDs:
                is_any=True
                # API endpoint
                api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                deleted_value = {key: value for key, value in available.items() if key != 'id'}
                message = "I found ticket for you\ncurrent time is "+str(datetime.now().time())+'\n'+str(deleted_value)
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

if not is_any:
    for CHAT_ID in CHAT_IDs:
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        message = "there is not any ticket available"
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
