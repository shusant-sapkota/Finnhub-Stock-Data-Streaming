import os
import time
import finnhub
from confluent_kafka import SerializingProducer
import simplejson as json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

finnhub_client = finnhub.Client(os.getenv('FINNHUB_API_KEY'))
print(finnhub_client)

# Stock candles
#res = finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)
#print(finnhub_client.aggregate_indicator('AAPL', 'D'))

#print(finnhub_client.quote(symbol='AAPL'))

def delivery_report(err,msg):
    if err is not None:
        print(f'Message delivery failed: {err}')

    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def data_to_broker(producer, topic):
    while True:
        data = finnhub_client.quote(symbol='AAPL')
        try:
            producer.produce(
                topic,
                key = str(data['t']),
                value = json.dumps(data).encode('utf-8'),
                on_delivery=delivery_report
            )
        except KeyboardInterrupt:
            print("Streaming Ended, Interrupted by User")
        except Exception as e:
            print(f'Error Encountered: {e}')
        time.sleep(5)


if __name__=="__main__":
    producer_config = {
        'bootstrap.servers': 'localhost:7071',
        'error_cb': lambda err: print(f'Kafka Error: {err}')
    }

    producer = SerializingProducer(producer_config)

    try:
        data_to_broker(producer, 'apple_data')
    except KeyboardInterrupt:
        print('Data Streaming Halted by User')
    except Exception as e:
        print(f'Unexpected Error Occured: {e}')



