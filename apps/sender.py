import os
import random
import string
import time
import asyncio
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventData

HOST_NAME = os.getenv('HOST_NAME')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')

credential = DefaultAzureCredential()

async def send_message(producer, content):
    event_data = EventData(content)
    await producer.send_batch([event_data])
    print("Sent Message: " + content)

async def main():
    producer = EventHubProducerClient(HOST_NAME, EVENT_HUB_NAME, credential)
    
    chars = string.digits
    
    async with producer:
        while True:
            content = ''.join(random.choice(chars) for i in range(10))
            await send_message(producer, content)
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())