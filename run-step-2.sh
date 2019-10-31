#!/bin/bash
set -e

echo "------------------------------------------------------------------"
echo " STEP 2:"
echo " Try out an ML model trained using Kafka data "
echo "------------------------------------------------------------------"


echo ">> Getting the config from config.env"
set -a
source ./config.env
set +a
python config.py

echo ">> Train a machine learning model using training data from Kafka"
python 2_train_and_try_model.py

echo ">> Check the ML model's prediction by opening test.png"
