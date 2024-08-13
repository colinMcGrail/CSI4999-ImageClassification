import numpy as np
from PIL import Image
import keras

def classifyOsteoarthritis(image, model):
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return model.predict(img_array)
