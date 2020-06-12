# DDOS Protector

This solution is only run locally.

Data is ingested from the following API: <https://github.com/DanThomp507/DDOS-API>

## Requirements

1. Python 2.7+

2. Apache Kafka (Python API)

Ensure you have Kafka downloaded and configured.  

If you do not, instructions can be found here: <https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273>

## How To Start

1. Clone the repo

``` git clone https://github.com/DanThomp507/DDOS-Protector.git ```

After cloning the repo:

2. Start your services (each in a separate terminal tab)

``` zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties ```

``` kafka-server-start /usr/local/etc/kafka/server.properties ```

3. Install requirements

``` pip install -r requirements.txt ```

4. Run both Producer and Consumer

``` python main.py ```

``` python Consumer.py ```
