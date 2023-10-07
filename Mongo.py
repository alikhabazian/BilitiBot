
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Task import Task
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the password variable
mongodb_password = os.getenv("MONGODB_PASSWORD")

# Use the password in your connection string or wherever needed
uri = f"mongodb+srv://khabaziana:{mongodb_password}@cluster0.l4miazp.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# try:
#     # Access a specific database (replace 'your_database' with the actual database name)
#     db = client.Biliti
#
#     # Access a specific collection within the database (replace 'your_collection' with the actual collection name)
#     collection = db.Tasks
#
#     # Example: Insert a document into the collection
#     document = {
#         "creator": "684630739",
#         "receivers": [
#             '684630739','229091667'
#         ],
#         "how_often": "daily",
#         "orgin_city": 'تهران',
#         "destination_city":'اصفهان',
#         "date":'2023-10-02',
#         "start_time":'21:00:00',
#         "end_time":'23:59:59'
#     }
#     collection.insert_one(document)
#
#     print("Document inserted successfully!")
#
# except Exception as e:
#     print(e)
#
# finally:
#     # Close the connection when you're done
#     client.close()


try:
    # Access a specific database (replace 'your_database' with the actual database name)
    db = client.Biliti

    # Access a specific collection within the database (replace 'your_collection' with the actual collection name)
    collection = db.Tasks

    # Example: Retrieve all items from the collection
    cursor = collection.find()

    # Print each item in the result set
    tasks = []
    for document in cursor:
        task = Task(
            creator=document['creator'],
            receivers=document['receivers'],
            how_often=document['how_often'],
            orgin_city=document['orgin_city'],
            destination_city=document['destination_city'],
            date=document['date'],
            start_time=document['start_time'],
            end_time=document['end_time']
        )
        # print(task)
        tasks.append(task)

    for task in tasks:
        # print(task)
        try:
            task.get_data_ali_baba()
        except Exception as e:
            print(e)
        try:
            task.get_data_snapp()
        except Exception as e:
            print(e)

except Exception as e:
    print(e)

finally:
    # Close the connection when you're done
    client.close()