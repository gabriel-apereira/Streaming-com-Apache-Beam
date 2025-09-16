# pip install google-cloud-pubsub
# producer

import csv
import time
from google.cloud import pubsub_v1
import os

service_account_key = r"C:\Users\gabri\Desktop\Udemy\Apache GCP\dataflow-beam-voos-b1227139fe6e.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key

topico = 'projects/dataflow-beam-voos/topics/MeusVoos'
publisher = pubsub_v1.PublisherClient()

entrada = r"C:\Users\gabri\Desktop\Udemy\Apache GCP\Inputs\voos_sample.csv"

with open(entrada, 'rb') as file:
    for row in file:
        print('Publishing in Topic')
        publisher.publish(topico, row)
        time.sleep(2)
