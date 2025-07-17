import os
import asyncio
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubConsumerClient

HOST_NAME = os.getenv('HOST_NAME')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME')
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP')

credential = DefaultAzureCredential()

async def on_event(partition_context, event):
    print("Message Received: " + event.body_as_str())
    await partition_context.update_checkpoint(event)
    await asyncio.sleep(0.1)

async def main():
    consumer = EventHubConsumerClient(HOST_NAME, EVENT_HUB_NAME, CONSUMER_GROUP, credential)
    
    async with consumer:
        await consumer.receive(on_event=on_event)

if __name__ == "__main__":
    asyncio.run(main())