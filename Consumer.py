from __future__ import print_function
from kafka import KafkaConsumer
import time
from datetime import datetime
import json
import argparse

def print_log(message):
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

def get_ip(message):
  obj = json.loads(message.value)
  return obj["remote_host"]

def print_culprits(culprits, isDebug):
  filename = 'text-run.txt'
  open(filename, 'w').close()
  if not culprits:
    print("No culprits found")
  else:
    if isDebug:
      print('All Culprits:')

    print('Writing results to file:', filename)
    # Clear old contents
    open(filename, 'w').close()
    # Write to file per requirements
    with open(filename, 'w') as f:
      f.write("\n".join(culprits))

def process_messages(args, consumer):
  start=datetime.now()
  window = []
  kvs = {}
  culprits = set()

  print('Starting the process...')
  for message in consumer:
    ip = get_ip(message)

    # if sliding window is full, remove head, decrement dictionary, remove from dict no value
    if len(window) >= args.window:
      oldIp = window.pop(0)
      kvs[oldIp] = kvs[oldIp] - 1
      if kvs[oldIp] == 0:
        kvs.pop(oldIp)

    # add ip to end of window
    window.append(ip)

    # we need to sync up the dictionary with what's in the window
    if not ip in kvs:
      kvs[ip] = 0
    kvs[ip] = kvs[ip] + 1

    # set the limit to 2 (arbritrarily low), then add ip to culprits if exceeding limit
    if kvs[ip] >= 2:
      if not ip in culprits:
        print('FOUND CULPRIT IP:', ip)
        culprits.add(ip)

    # logging/debugging
    if args.debug:
      print('current ip: ', ip)
      print(window)
      print(kvs)
      print(culprits)
      print()
      time.sleep(5)
  print('Process ended.')
  print('Time taken:', datetime.now()-start)
  print_culprits(culprits, args.debug)
  

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-rh', '--host', default="127.0.0.1:9092")
  parser.add_argument('-t', '--topic', default='demo')
  parser.add_argument('-w', '--window', type=int, default=5000)
  parser.add_argument('-x', '--times', type=int, default=500)
  parser.add_argument('-d', '--debug', type=bool, default=False)
  args = parser.parse_args()
  consumer = KafkaConsumer(args.topic,
                         group_id='my-group',
                         bootstrap_servers=[args.host],
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         consumer_timeout_ms=1000)
  process_messages(args,consumer)