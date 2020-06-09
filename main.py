from __future__ import print_function
import time
import json
import argparse
import read_log
from kafka import KafkaProducer
from datetime import datetime

KAFKA_HOSTS = ['localhost:9092']
KAFKA_VERSION = (0, 10)

def send_message(producer, topic, input):
    with open(input, 'r') as fo:
        rows = read_log.apache_log_row(fo)
        for message_raw in rows:
            producer.send(topic, json.dumps({'remote_host': message_raw[0],
                                                  'user-identifier': message_raw[1],
                                                  'frank': message_raw[2],
                                                  'time_received': message_raw[3],
                                                  'request_first_line': message_raw[4],
                                                  'status': message_raw[5],
                                                  'size_bytes': message_raw[6],
                                                  'request_header_referer': message_raw[7],
                                                  'request_header_user_agent': message_raw[8]}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-rh', '--host', default="localhost:9092")
    parser.add_argument('-t', '--topic', default='demo')
    parser.add_argument('-i', '--input', required=True)
    args = parser.parse_args()
    producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS, api_version=KAFKA_VERSION)
    start=datetime.now()
    send_message(producer, args.topic, args.input)
    print("Time taken to send all the logs:", datetime.now()-start)