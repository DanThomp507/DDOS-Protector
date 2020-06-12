from __future__ import print_function
import time
import json
import argparse
from kafka import KafkaProducer
from datetime import datetime
import requests

KAFKA_HOSTS = ['localhost:9092']
KAFKA_VERSION = (0, 10)
url = 'https://ddos-api.herokuapp.com/all'


def send_message(producer, topic):
    response = requests.get(url)
    logs = response.text
    parsed = json.loads(logs)['result']

    for dic in parsed:
        producer.send(topic, json.dumps({'remote_host': dic['clientip'],
                                         'time_received': dic['time'],
                                         'request_first_line': dic['uri'],
                                         'status': dic['status'],
                                         'size_bytes': dic['bytes'],
                                         }))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-rh', '--host', default='localhost:9092')
    parser.add_argument('-t', '--topic', default='demo')
    args = parser.parse_args()
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_HOSTS, api_version=KAFKA_VERSION)
    start = datetime.now()
    send_message(producer, args.topic)
    print('Time taken to send all the logs:', datetime.now()-start)
