#!/bin/bash
set -e

echo "------------------------------------------------------------------"
echo " STEP 4:"
echo " Using an ML model to make predictions about a stream of Kafka events"
echo "------------------------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py


echo ">> Re-creating the topic for the stream of events to classify"
cloudctl es topic-delete $TEST_STREAM_TOPIC_NAME --force
sleep 5
cloudctl es topic-create $TEST_STREAM_TOPIC_NAME --partitions 1 --replication-factor 1

echo ">> Train a machine learning model and test using the stream of events from Kafka"
trap 'kill $BGPID; exit' INT    # exit the background Python process when this script is killed
python 4_train_and_stream_model.py &
BGPID=$!
sleep 50

echo ">> Start simulating a stream of events"
python simulate_test_stream.py

