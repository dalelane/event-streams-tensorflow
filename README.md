# event-streams-tensorflow
**Example of using TensorFlow with IBM Event Streams, to explain how to get started creating machine learning applications using the data you have on Kafka topics.**

This is a simple demo app, not intended for production use (there is no error-handling at all, the ML model isn't hosted, etc.). The aim is to provide an easy-to-understand working example of how to integrate Kafka with TensorFlow.

I've explained how it all works in **https://dalelane.co.uk/blog/?p=3924** 

It's written for Python 3. To run it:

1. `pip install -r requirements.txt`
2. Edit `config.env` with the properties of your cluster 
3. Run `run-step-0.sh` to set up your Kafka topics
4. Run `run-step-1.sh` to train a machine learning model using data from a Kafka training topic
5. Run `run-step-2.sh` to train a machine learning model and use it to classify an image
6. Run `run-step-3.sh` to train a machine learning model and test it using data from a Kafka test topic
7. Run `run-step-4.sh` to use a machine learning model to classify a stream of events on a Kafka topic

To wipe everything if you want to start again, run `run-cleanup-99.sh`. 

<img src="https://live.staticflickr.com/65535/48982711946_5229953ea1_c.jpg">

