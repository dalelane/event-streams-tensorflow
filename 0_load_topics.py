# external dependencies
import tensorflow_datasets as tfds
from kafka import KafkaProducer
# local dependencies
from schemas import get_schema, serialize, create_headers_for_schema
# config values
from config import SCHEMA_ID, SCHEMA_VERSION, CERT
from config import EVENT_STREAMS_REST_API, EVENT_STREAMS_API_KEY
from config import KAFKA_BOOTSTRAP, TRAINING_TOPIC_NAME, TEST_ARCHIVE_TOPIC_NAME



print ("-->>> Get the schema to use to represent fashion MNIST data")
schema = get_schema(SCHEMA_ID, SCHEMA_VERSION, EVENT_STREAMS_REST_API, EVENT_STREAMS_API_KEY, CERT)

print ("-->>> Create a Kafka producer")
producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP],
                         security_protocol="SASL_SSL",
                         ssl_cafile=CERT,
                         ssl_check_hostname=False,
                         sasl_plain_username="token",
                         sasl_plain_password=EVENT_STREAMS_API_KEY,
                         sasl_mechanism="PLAIN",
                         client_id="dalelane-load-topics")

print ("-->>> Download the training data to be used")
train, test = tfds.load("fashion_mnist", split=["train", "test"])

print ("-->>> Sending training data to Kafka topic %s" % TRAINING_TOPIC_NAME)
for features in train.batch(1).take(-1):
    producer.send(TRAINING_TOPIC_NAME,
                  serialize(schema, {
                      "ImageData" : features["image"].numpy()[0].tobytes(),
                      "Label" : int(features["label"].numpy()[0])
                  }),
                  None,
                  create_headers_for_schema(SCHEMA_ID, SCHEMA_VERSION))
producer.flush()

print ("-->>> Sending test data to Kafka topic %s" % TEST_ARCHIVE_TOPIC_NAME)
for features in test.batch(1).take(4000):
    producer.send(TEST_ARCHIVE_TOPIC_NAME,
                  serialize(schema, {
                      "ImageData" : features["image"].numpy()[0].tobytes(),
                      "Label" : int(features["label"].numpy()[0])
                  }),
                  None,
                  create_headers_for_schema("TrainingData", "1"))
producer.flush()
