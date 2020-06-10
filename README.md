# DDOS Protector

This solution is only run locally

## Requirements

1. Python 2.7+

2. Apache Kafka (Python API)

Ensure you have Kafka downloaded and configured.  

If you do not, instructions can be found here: <https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273>

## How To Start

1. Start your services

``` zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties ```

``` kafka-server-start /usr/local/etc/kafka/server.properties ```

2. Install requirements

``` pip install -r requirements.txt ```

3. Run both Producer and Consumer

``` python main.py -i apache_log_ddos.txt ```

``` python Consumer.py ```

