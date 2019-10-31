#!/bin/bash

echo "------------------------------------------------"
echo " CLEANUP"
echo "------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py

echo ">>> Removing the schema"
cloudctl es schema-remove --name $SCHEMA_NAME --force

echo ">>> Removing the topics"
cloudctl es topic-delete --name $TRAINING_TOPIC_NAME --force
cloudctl es topic-delete --name $TEST_ARCHIVE_TOPIC_NAME --force
cloudctl es topic-delete --name $TEST_STREAM_TOPIC_NAME --force

echo ">>> Removing downloaded client certificate"
rm -f es-cert.pem

echo ">>> Removing test files"
rm -f test.png
