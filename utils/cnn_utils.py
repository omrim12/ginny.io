import logging
import numpy as np
import tensorflow as tf
from keras import layers
from termcolor import cprint
from tensorflow import keras
from utils.data_utils import load_food_101
from utils.tag_utils import get_labels_list
from constants import (
    IMAGE_SIZE,
    CONV_TYPE,
    EPOCH,
    KERNEL_SIZE,
    FILTERS
)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def classify_client_input(image_array: np.array, cnn_model) -> str:
    # pass image in cnn_model to predict compatible food item
    food_predict = cnn_model.predict(np.array([image_array]))

    # Return corresponding food item
    return get_labels_list()[np.argmax(food_predict)]


def train_by_type(
        X_train, y_train,
        X_valid, y_valid,
        X_test, y_test,
        conv_type,
        epoch=20,
        batch_size=128,
        layer_act='relu',
        output_act='softmax',
        num_types=101
):
    # Init CNN inputs tensor
    inputs = keras.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 1))

    # Run convolution & max-pooling
    X = layers.Conv2D(
        filters=FILTERS,
        kernel_size=(KERNEL_SIZE, KERNEL_SIZE),
        activation=layer_act, padding=conv_type)(inputs)
    X = layers.MaxPooling2D(pool_size=2)(X)
    X = layers.Conv2D(
        filters=FILTERS * 2,
        kernel_size=(KERNEL_SIZE, KERNEL_SIZE),
        activation=layer_act, padding=conv_type)(X)
    X = layers.MaxPooling2D(pool_size=2)(X)
    X = layers.Conv2D(
        filters=FILTERS * 2,
        kernel_size=(KERNEL_SIZE, KERNEL_SIZE),
        activation=layer_act, padding=conv_type)(X)

    # Flatten output layer (a KerasTensor) from CNN to pass output data
    # to NN output dense layer (knows only to receive a vector)
    X = layers.Flatten()(X)

    # Adding a Dense layer
    X = layers.Dense(units=IMAGE_SIZE ** 2,
                     activation=layer_act)(X)

    # Calculating outputs from NN dense layer
    outputs = layers.Dense(
        num_types,
        activation=output_act)(X)

    # Initialize model from feature maps results
    # and other defined layers
    model = keras.Model(inputs=inputs, outputs=outputs)

    # Summarize results from CNN
    model.summary()

    # Training CNN model based on optimization techniques
    model.compile(optimizer='rmsprop',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(X_train, y_train,
              epochs=epoch, batch_size=batch_size,
              validation_data=(X_valid, y_valid))

    # Computing loss & accuracy over the entire test set
    test_loss, test_acc = model.evaluate(X_test, y_test)

    return model, test_loss, test_acc


def cnn_train(num_types=None, mode='cpu'):
    cprint('\nAbout to train a new genie!', "blue")

    # load train + valid + test datasets
    if num_types:
        X_train, X_valid, X_test, \
            y_train, y_valid, y_test, \
            food_types = load_food_101(num_types=num_types)
    else:
        X_train, X_valid, X_test,\
            y_train, y_valid, y_test, \
            food_types = load_food_101()

    # Adapting GPU/CPU usage
    if mode == 'gpu':
        if tf.test.gpu_device_name():
            LOGGER.info(f"Found GPU device: {tf.test.gpu_device_name()}")
            physical_devices = tf.config.experimental.list_physical_devices('GPU')
            tf.config.experimental.set_memory_growth(physical_devices[0], True)
        else:
            LOGGER.info(f"No GPU device found. running with CPU")

    # Training CNN using the food 101 dataset
    LOGGER.info(f"--- Running CNN '{CONV_TYPE}' learning session ---")
    model, model_loss, model_acc = train_by_type(X_train, y_train,
                                                 X_valid, y_valid,
                                                 X_test, y_test,
                                                 conv_type=CONV_TYPE,
                                                 epoch=EPOCH)
    return model, model_loss, model_acc, food_types
