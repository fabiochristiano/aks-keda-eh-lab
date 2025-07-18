import os
import time
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubConsumerClient

HOST_NAME = os.getenv('HOST_NAME')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP')

credential = DefaultAzureCredential()

def on_event(partition_context, event):
    print("Message Received: " + event.body_as_str())
    partition_context.update_checkpoint(event)
    time.sleep(0.1)

def main():
    consumer = EventHubConsumerClient(HOST_NAME, EVENT_HUB_NAME, CONSUMER_GROUP, credential)
    
    try:
        consumer.receive(on_event=on_event)
    finally:
        consumer.close()

if __name__ == "__main__":
    main()