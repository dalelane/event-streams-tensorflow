# external dependencies
import tensorflow_io.kafka as kafka_io
from tensorflow import keras
import tensorflow as tf
# internal dependencies
from schemas import get_schema
# config values
from config import SCHEMA_ID, SCHEMA_VERSION, CERT
from config import EVENT_STREAMS_REST_API, EVENT_STREAMS_API_KEY
from config import KAFKA_BOOTSTRAP, TRAINING_TOPIC_NAME



schemaobj = get_schema(SCHEMA_ID, SCHEMA_VERSION,
                       EVENT_STREAMS_REST_API, EVENT_STREAMS_API_KEY,
                       CERT)
schemastr = str(schemaobj)



def deserialize(kafkamessage):
    trainingitem = kafka_io.decode_avro(kafkamessage,
                                        schema=schemastr,
                                        dtype=[tf.string, tf.int32])

    image = tf.io.decode_raw(trainingitem[0], out_type=tf.uint8)
    image = tf.reshape(image, [28, 28])
    image = tf.image.convert_image_dtype(image, tf.float32)

    label = tf.reshape(trainingitem[1], [])

    return image, label



def run():
    dataset = kafka_io.KafkaDataset([ TRAINING_TOPIC_NAME + ':0' ],
                                    servers=KAFKA_BOOTSTRAP,
                                    group="dalelane-tensorflow-train",
                                    config_global=[
                                        "api.version.request=true",
                                        "sasl.mechanisms=PLAIN",
                                        "security.protocol=sasl_ssl",
                                        "sasl.username=token",
                                        "sasl.password=" + EVENT_STREAMS_API_KEY,
                                        "ssl.ca.location=" + CERT
                                    ])

    dataset = dataset.map(deserialize).batch(1)

    # neural net definition taken from
    #  https://www.tensorflow.org/tutorials/keras/classification#set_up_the_layers

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(10, activation="softmax")
    ])

    model.compile(optimizer="adam",
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"])

    model.fit(dataset, epochs=4, steps_per_epoch=1000)

    return model
