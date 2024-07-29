from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Send a test message to the 'test' topic
producer.send('test', b'THIS IS FIRST ASDFG, asdfg')
producer.flush()
print("Message sent successfully")
