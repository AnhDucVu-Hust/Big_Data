import json
import base64
import hashlib
from json import dump
import pandas as pd
from io import StringIO
import pandas as pd
from confluent_kafka import Consumer
from hdfs import InsecureClient

c = Consumer({'bootstrap.servers': 'localhost:9092',
              'group.id': 'climate_data',
              'auto.offset.reset': 'earliest'})
c.subscribe(['climate_data'])
client_hdfs = InsecureClient('http://localhost:9870', user='root')

while True:
    msg = c.poll(1.0)
    print(msg)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    data_dict = json.loads(msg.value().decode('utf-8'))

    """
    columns = sorted(list(data_dict.keys()))
    for key in data_dict.keys():
        data_dict[key] = [data_dict[key]]
    df = pd.DataFrame.from_dict(data_dict)
    """
    try:
        url = str(data_dict['url'])
        #print(data_dict['climate_day'])
        hash_url = hashlib.md5(url.encode()).hexdigest()
        with client_hdfs.write('/Users/vuanhduc/climate_data_expand/{}.csv'.format(data_dict['name']), encoding='utf-8') as writer:
            writer.write(data_dict['climate_day'])
        print('Write {} to Hdfs successfully'.format(data_dict['url']))
    except:
        print('{} existed in hdfs'.format(data_dict['url']))

c.close()