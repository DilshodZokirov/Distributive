import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

# requests
channel_layer = get_channel_layer()


@shared_task
def get_chat():
    url = 'http://aspi.icnfb.com/jokes/random/'
    response = requests.get(url).json()
    chat = response['value']['joke']
    async_to_sync(channel_layer.grioup_send)('chat',
                                             {'type': 'send_chat', 'text': chat})
