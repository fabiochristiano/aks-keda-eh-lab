import os
import random
import string
import time
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventData

HOST_NAME = os.getenv('HOST_NAME')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')

credential = DefaultAzureCredential()

def send_message(producer, content):
    event_data = EventData(content)
    producer.send_batch([event_data])
    print("Sent Message: " + content)

def main():
    producer = EventHubProducerClient(HOST_NAME, EVENT_HUB_NAME, credential)
    
    chars = string.digits
    
    try:
        while True:
            content = ''.join(random.choice(chars) for i in range(10))
            send_message(producer, content)
            time.sleep(0.1)
    finally:
        producer.close()

if __name__ == "__main__":
    main()