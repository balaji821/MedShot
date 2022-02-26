from tensorflow import keras
from keras.preprocessing import image
import numpy as np
import logging
import file_utils as fu

logger = logging.getLogger("medshot")

model = None
img_width, img_height = 300, 300


def load_model():
    global model
    model = keras.models.load_model(fu.get_model_path())
    return model


def make_prediction(image_path):
    img = image.load_img(image_path, target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    if model is None:
        load_model()

    return model.predict(images)
