#!/bin/bash
set -e

echo "------------------------------------------------------------------"
echo " STEP 1:"
echo " Using a Kafka topic as a source of training data "
echo "------------------------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py

echo ">> Train a machine learning model using training data from Kafka"
python 1_train_model.py
