#!/bin/bash
set -e

echo "------------------------------------------------------------------"
echo " STEP 3:"
echo " Using a Kafka topic as a source of test data "
echo "------------------------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py

echo ">> Train a machine learning model and test using test data from Kafka"
python 3_train_and_test_model.py
