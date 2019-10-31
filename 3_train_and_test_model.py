# external dependencies
import tensorflow_io.kafka as kafka_io
# local dependencies
import train_model
# config values
from config import EVENT_STREAMS_API_KEY, CERT
from config import KAFKA_BOOTSTRAP, TEST_ARCHIVE_TOPIC_NAME



print ("-->>> Train a machine learning model using training data from Kafka")
model = train_model.run()

print ("-->>> Prepare a test dataset using test data from Kafka")
dataset = kafka_io.KafkaDataset([ TEST_ARCHIVE_TOPIC_NAME + ":0"],
                                servers=KAFKA_BOOTSTRAP,
                                group="dalelane-tensorflow-test",
                                eof=True,
                                config_global=[
                                    "api.version.request=true",
                                    "sasl.mechanisms=PLAIN",
                                    "security.protocol=sasl_ssl",
                                    "sasl.username=token",
                                    "sasl.password=" + EVENT_STREAMS_API_KEY,
                                    "ssl.ca.location=" + CERT
                                ])
dataset = dataset.map(train_model.deserialize).batch(1)

print ("-->>> Evaluate the machine learning model using test data from Kafka")
model.evaluate(dataset)
