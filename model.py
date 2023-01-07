# Description: This file contains the model

# Importing the libraries
import ast
import io
import os
import pickle

import numpy as np
import requests
import tensorflow as tf
from numpy.linalg import norm
from PIL import Image
from rich.console import Console
from rich.progress import Progress
from sklearn.neighbors import NearestNeighbors
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.models import Sequential

# Initializing the variables
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
img_files_list = []
features_list = []
model = None

pick_store = False
product_status = False

# Used to initialize the model (With or without the Sequential model)
def initialize_model(dev_model):
    global img_files_list, features_list, model
    
    console = Console()
    
    model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) 
    img_files_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/img_filesWOMEN3.pkl').content)
    features_list = []
    
    if not dev_model:
        console.log("Innitializing ResNet50 model...")
        
        with Progress() as progress:
            task = progress.add_task("[green]Loading data...", total=69)
            for i in range(69):
                temp_data = pickle.loads(requests.get(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/files/image_features_embeddingWOMEN_small{i}.pkl').content)
                features_list += temp_data
                progress.update(task, advance=1)
    else:
        console.log("Innitializing ResNet50 + Sequential model...")
        for i in range(2):
            temp_data = pickle.loads(requests.get(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/files/image_features_embeddingWOMEN{i}.pkl').content)
            features_list += temp_data
        model = Sequential([model, GlobalMaxPooling2D()]) # Faster but less accurate

# This function is the main function when the input is a url
def process(url, headers, pageNumber):
    global pick_store, product_status, img_files_list, features_list, model
    features = extract_img_features(url, headers, model)
    img_distence, img_indicess = recommend(features, features_list)
    results = []
    
    for result in img_indicess[0][(pageNumber*10)-10:pageNumber*10]:
        results.append(img_files_list[result])
        
    return results

# This function is the main function when the input is a file
def process_file(file, pageNumber):
    global pick_store, product_status, img_files_list, features_list, model
    features = extract_img_features_from_file(file, model)
    img_distence, img_indicess = recommend(features, features_list)
    results = []
    
    for result in img_indicess[0][(pageNumber*10)-10:pageNumber*10]:
        results.append(img_files_list[result])
        
    return results

# Used to extract the features from the given file
def extract_img_features_from_file(file, model):
    img = Image.open(io.BytesIO(file))
    img = tf.image.resize(img, (224, 224))
    img_array = np.array(img)
    img_array.setflags(write=1)
    expand_img = np.resize(img_array, (1, 224, 224, 3))
    preprocessed_img = preprocess_input(expand_img)
    result_to_resnet = model.predict(preprocessed_img)
    flatten_result = result_to_resnet.flatten()
    # normalizing
    result_normlized = flatten_result / norm(flatten_result)
    return result_normlized

# Used to extract the features from the given url
def extract_img_features(url, headers, model):
    try:
        if headers != '':
            if type(headers) == str:
                headers = ast.literal_eval(headers)
            image_reader = tf.image.decode_image(
                requests.get(url, headers=headers).content, channels=3)
        else:
            file = requests.get(url).content
            img = Image.open(io.BytesIO(file))
            img = tf.image.resize(img, (224, 224))
            img_array = np.array(img)
            img_array.setflags(write=1)
            expand_img = np.resize(img_array, (1, 224, 224, 3))
            preprocessed_img = preprocess_input(expand_img)
            result_to_resnet = model.predict(preprocessed_img)
            flatten_result = result_to_resnet.flatten()
            # normalizing
            result_normlized = flatten_result / norm(flatten_result)
            return result_normlized
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

# Used to find the nearest neighbors
def recommend(features, features_list):
    neighbors = NearestNeighbors(n_neighbors=len(features_list), algorithm='brute', metric='euclidean')
    neighbors.fit(features_list)
        
    distence, indices = neighbors.kneighbors([features])
    return distence, indices