# external dependencies
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
# local dependencies
import train_model



print ("-->>> Train a machine learning model using training data from Kafka")
model = train_model.run()

print ("-->>> Get information about the Fashion MNIST dataset")
datasetinfo = tfds.builder('fashion_mnist').info.features['label']

print ("-->>> Choose a random item from the test set")
test, = tfds.load('fashion_mnist', split=["test"])
for features in test.shuffle(10000).batch(1).take(1):
    testdata = features["image"].numpy()[0]

    print ("-->>> Use the ML model to make a prediction for the test item")
    prediction = model.predict(testdata.reshape(1, 28, 28))
    prediction_idx = prediction.argmax()
    prediction_name = datasetinfo.int2str(prediction_idx)
    prediction_confidence = prediction[0][prediction_idx] * 100.0

    print ("-->>> Prediction : %s with %d%% confidence" %
        (prediction_name, prediction_confidence))

    print ("-->>> Saving random test item to test.png for verification")
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    testimage = testdata.reshape([-1, 28, 28, 1]) / 255
    plt.imshow(1 - testimage[0][:, :, 0], cmap='gray')
    plt.savefig("test.png")
