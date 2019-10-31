#!/bin/bash
set -e

echo "------------------------------------------------------------------"
echo " STEP 0:"
echo " Preparing Kafka topics with data for an machine learning project "
echo "------------------------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py

echo ">> Creating the schema for the training and test data used in this project"
cloudctl es schema-add --file $SCHEMA_FILE_NAME --name $SCHEMA_NAME --version 1.0.0

echo ">> Creating the topics that will be used for this project"
cloudctl es topic-create $TRAINING_TOPIC_NAME --partitions 1 --replication-factor 3
cloudctl es topic-create $TEST_ARCHIVE_TOPIC_NAME --partitions 1 --replication-factor 3

echo ">> Downloading a client certificate"
cloudctl es certificates --format pem --force

echo ">> Populating Kafka topics with training and test data"
python 0_load_topics.py
