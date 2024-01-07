""" code that predicts a word image """

import base64
from tensorflow.keras.layers.experimental.preprocessing import StringLookup
from tensorflow import keras
from tensorflow.keras.models import load_model

import tensorflow as tf
import numpy as np
import os

tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(1)

image_width = 128
image_height = 32
max_len = 21
characters = ['!', '"', '#', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
char_to_num = StringLookup(vocabulary=list(characters), mask_token=None)
num_to_char = StringLookup(
    vocabulary=char_to_num.get_vocabulary(),mask_token = None, invert=True
)


def distortion_free_resize(image, img_size):
  w, h = img_size
  image = tf.image.resize(image, size= (h,w), preserve_aspect_ratio=True)
  pad_height = h - tf.shape(image)[0]
  pad_width = w - tf.shape(image)[1]

  if pad_height % 2 != 0:
    height = pad_height // 2
    pad_height_top = height + 1
    pad_height_bottom = height
  else:
    pad_height_top = pad_height_bottom = pad_height//2

  if pad_width % 2 !=0:
    width = pad_width //2
    pad_width_left = width +1
    pad_width_right = width
  else:
    pad_width_left = pad_width_right = pad_width // 2

  image = tf.pad(
      image,
      paddings = [
          [pad_height_top, pad_height_bottom],
          [pad_width_left, pad_width_right],
          [0,0],
      ],
  )

  image = tf.transpose(image, perm=[1,0,2])
  image = tf.image.flip_left_right(image)
  return image

def decode_batch_predictions(pred):
  input_len = np.ones(pred.shape[0])*pred.shape[1]
  results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
      :, :max_len
  ]
  output_text=[]
  for res in results:
    res = tf.gather(res,tf.where(tf.math.not_equal(res,-1)))
    res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
    output_text.append(res)
  return output_text

# def preprocess_image(image_path, img_size=(image_width, image_height)):
#   image = tf.io.read_file(image_path)
#   image = tf.image.decode_png(image,1)
#   image = distortion_free_resize(image,img_size)
#   image = tf.cast(image, tf.float32)/255.0
#   return image

def preprocess_base64_image(base64_image, img_size=(image_width, image_height)):
    image_data = base64.b64decode(base64_image)
    image = tf.image.decode_png(image_data, channels=1)
    image = distortion_free_resize(image, img_size)
    image = tf.cast(image, tf.float32) / 255.0
    return image
  
  
# def predict_image(model, image_path):
#     preprocessed_image = preprocess_image(image_path)
#     input_image = tf.expand_dims(preprocessed_image, axis=0)
#     predictions = model.predict(input_image)
#     decoded_text = decode_batch_predictions(predictions)[0]
#     return decoded_text
    
def predict_base64_image(model, base64_image):
    preprocessed_image = preprocess_base64_image(base64_image)
    input_image = tf.expand_dims(preprocessed_image, axis=0)
    predictions = model.predict(input_image)
    decoded_text = decode_batch_predictions(predictions)[0]
    return decoded_text
    
class CTCLayer(keras.layers.Layer):
  def __init__(self, name=None):
    super().__init__(name=name)
    self.loss_fn = keras.backend.ctc_batch_cost
    

# def word_img_to_text(model_path, image_path):
#     # model_path = "/content/drive/MyDrive/7th_sem/proj/htr_model-label-fixed.h5"
#     # image_path = "/content/test.png"
    
#     loaded_model = load_model(model_path, custom_objects={"CTCLayer": CTCLayer})

#     prediction_model = keras.models.Model(
#         loaded_model.get_layer(name="image").input,
#         loaded_model.get_layer(name="dense2").output
#     )

#     prediction = predict_image(prediction_model, image_path)
#     print(prediction)
#     return prediction

def predict_handwritten_text(base64_image, model_path="htr-Conv-v2.h5"):
    loaded_model = load_model(model_path, custom_objects={"CTCLayer": CTCLayer})

    prediction_model = keras.models.Model(
        loaded_model.get_layer(name="image").input,
        loaded_model.get_layer(name="dense2").output
    )
    prediction = predict_base64_image(prediction_model, base64_image)
    return prediction