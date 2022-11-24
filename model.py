from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
import os
import tensorflow as tf

import json
import requests
import pickle
import ast
import numpy as np
from numpy.linalg import norm

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


model = ResNet50(weights="imagenet", include_top=False,
                 input_shape=(224, 224, 3))
#model.trainable = True
model = Sequential([model, GlobalMaxPooling2D()]) # Faster but less accurate

pick_store = False
product_status = False

def process(url, headers, pageNumber):
    global pick_store, product_status
    img_files_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/img_filesWOMEN3.pkl').content)
    features_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/image_features_embeddingWOMEN3.pkl').content)
    features = extract_img_features(url, headers, model)
    img_distence, img_indicess = recommendd(features, features_list)
    results = []
    
    for result in img_indicess[0][(pageNumber*10)-10:pageNumber*10]:
        results.append(img_files_list[result])
        
    return results

def extract_img_features(url, headers, model):
    try:
        if headers != '':
            print(url)
            if type(headers) == str:
                headers = ast.literal_eval(headers)
            image_reader = tf.image.decode_image(
                requests.get(url, headers=headers).content, channels=3)
        else:
            image_reader = tf.image.decode_image(
                requests.get(url).content, channels=3)
        image_reader = tf.image.resize_with_pad(image_reader, 224, 224)
        img = tf.cast(image_reader, tf.float32)
        img_array = np.array(img)
        img_array.setflags(write=1)
        #expand_img = np.expand_dims(img_array, axis=0)
        expand_img = np.resize(img_array, (1, 224, 224, 3))
        preprocessed_img = preprocess_input(expand_img)
        result_to_resnet = model.predict(preprocessed_img)
        flatten_result = result_to_resnet.flatten()
        # normalizing
        result_normlized = flatten_result / norm(flatten_result)
        return result_normlized
    except Exception as e:
        print(e)
        return None

def recommendd(features, features_list):
    #neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    # neighbors.fit(features_list)

    neighbors = NearestNeighbors(n_neighbors=len(
        features_list), algorithm='brute', metric='euclidean')
    neighbors.fit(features_list)
        
    distence, indices = neighbors.kneighbors([features])
    return distence, indices