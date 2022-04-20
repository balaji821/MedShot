import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras import Model
from keras.preprocessing import image
from tensorflow import keras
import numpy as np
import file_utils as fu
import logging
import download

logger = logging.getLogger("medshot")

model: Model
img_width, img_height = 300, 300


def load_model(redownload, url):
    global model
    path = fu.get_model_path()
    if (not os.path.exists(path)) or redownload:
        download.download(url)
    model = keras.models.load_model(path)
    return model


# def make_prediction(image_path):
#     img = image.load_img(image_path, target_size=(img_width, img_height))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     images = np.vstack([x])
#
#     if model is None:
#         load_model()
#
#     return model.predict(images)

def make_prediction(img_path):
    img = image.load_img(img_path, target_size=(300, 300))
    img55 = image.img_to_array(img)
    img55 /= 255.0
    prediction_user = model.predict(np.array([img55]))
    print(prediction_user)
    return prediction_user
