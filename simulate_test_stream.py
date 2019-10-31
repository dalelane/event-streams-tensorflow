# external dependencies
import tensorflow_datasets as tfds
from kafka import KafkaProducer
from time import sleep
# local dependencies
from schemas import get_schema, serialize, create_headers_for_schema
# config values
from config import SCHEMA_ID, SCHEMA_VERSION, CERT
from config import EVENT_STREAMS_REST_API, EVENT_STREAMS_API_KEY
from config import KAFKA_BOOTSTRAP, TRAINING_TOPIC_NAME, TEST_STREAM_TOPIC_NAME



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

print ("-->>> Download the test data to be used")
test, = tfds.load("fashion_mnist", split=["test"])

print ("-->>> Starting to create test events to %s every second" % TEST_STREAM_TOPIC_NAME)
for features in test.batch(1).take(-1):
    producer.send(TEST_STREAM_TOPIC_NAME,
                  serialize(schema, {
                      "ImageData" : features["image"].numpy()[0].tobytes(),
                      "Label" : int(features["label"].numpy()[0])
                  }),
                  None,
                  create_headers_for_schema(SCHEMA_ID, SCHEMA_VERSION))
    sleep(1)
producer.flush()

print ("-->>> Ran out of test data to use for generating events.")
