from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'apple_data',
    bootstrap_servers = ['localhost:7071'],
    auto_offset_reset='earliest',       # Start from earliest messages
    enable_auto_commit=True,            # Automatically commit the read offset
    group_id='apple_data_id'
)

for message in consumer:
    print(message.value.decode('utf-8'))