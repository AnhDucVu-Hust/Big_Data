from confluent_kafka import Producer
import pandas as pd
import json

# Read CSV file into a Pandas DataFrame
csv_file_path = '12.csv'
df = pd.read_csv(csv_file_path,header=None)
print(df.columns)
columns_keep = [0,1,2,3,4,5,6,7,8,9,15,16,17]
df = df[columns_keep]
df.columns= ['Day', 'T', 'TM2', 'Tm3', 'SLP', 'H', 'PP', 'VV', 'V', 'VM','Country','Month','Year']

df["Metadata"] = csv_file_path.replace(".csv","")

# Convert DataFrame to JSON format
json_data = df.to_json(orient='records')


# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker(s) information
    'client.id': 'python-producer'
}

# Kafka topic
kafka_topic = 'streaming'  # Replace with your Kafka topic

# Callback function to handle delivery reports from Kafka
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Create Kafka producer
producer = Producer(producer_config)

# Produce message to Kafka topic
producer.produce(kafka_topic, json_data, callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()


