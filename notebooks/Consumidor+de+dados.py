# consumer

import csv
import time
from google.cloud import pubsub_v1
import os


service_account_key = r'C:\Users\gabri\Desktop\Udemy\Apache GCP\dataflow-beam-voos-b1227139fe6e.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

subscription = 'projects/dataflow-beam-voos/subscriptions/MeusVoos-Sub'
subscriber = pubsub_v1.SubscriberClient()


def monstrar_msg(mensagem):
    print(('Mensagem: {}'.format(mensagem)))
    mensagem.ack()


subscriber.subscribe(subscription, callback=monstrar_msg)

while True:
    time.sleep(3)
