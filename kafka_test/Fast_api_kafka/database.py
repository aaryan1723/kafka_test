from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json
from kafka.errors import TopicAlreadyExistsError

Kafka_connect = 'localhost:9092'
Topic_name = 'first'

producer = KafkaProducer(bootstrap_servers=Kafka_connect,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

consumer = KafkaConsumer(Topic_name, bootstrap_servers=Kafka_connect,
                         auto_offset_reset='earliest', 
                         enable_auto_commit=False,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

admin_client = KafkaAdminClient(bootstrap_servers=Kafka_connect)

try:
    admin_client.create_topics([NewTopic(name=Topic_name, num_partitions=1, replication_factor=1)])
except TopicAlreadyExistsError:
    pass
