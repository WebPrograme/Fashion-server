from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from PIL import Image
from rich.progress import Progress
from rich.console import Console
import io
import os
import tensorflow as tf

import requests
import pickle
import ast
import numpy as np
from numpy.linalg import norm

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
img_files_list = []
features_list = []
model = None

pick_store = False
product_status = False

print("Innitializing ResNet50 model...")

model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) 
model = Sequential([model, GlobalMaxPooling2D()]) # Faster but less accurate
        
img_files_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/img_filesWOMEN3.pkl').content)
features_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/image_features_embeddingWOMEN3.pkl').content)

def initialize_model(dev_model):
    global img_files_list, features_list, model
    
    console = Console()
    
    model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) 
    img_files_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/img_filesWOMEN3.pkl').content)
    features_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/image_features_embeddingWOMEN3.pkl').content)
    
    if not dev_model:
        console.log("Innitializing ResNet50 model...")
        
        features_list = []
        with Progress() as progress:
            task = progress.add_task("[green]Loading data...", total=63)
            for i in range(63):
                temp_data = pickle.loads(requests.get(f'https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/files/image_features_embeddingWOMEN{i}.pkl').content)
                features_list += temp_data
                progress.update(task, advance=1)
    else:
        console.log("Innitializing ResNet50 + Sequential model...")
        model = Sequential([model, GlobalMaxPooling2D()]) # Faster but less accurate

def process(url, headers, pageNumber):
    global pick_store, product_status, img_files_list, features_list, model
    features = extract_img_features(url, headers, model)
    print(len(features_list))
    img_distence, img_indicess = recommendd(features, features_list)
    results = []
    
    for result in img_indicess[0][(pageNumber*10)-10:pageNumber*10]:
        results.append(img_files_list[result])
        
    return results

def process_file(file, pageNumber):
    global pick_store, product_status
    img_files_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/img_filesWOMEN3.pkl').content)
    features_list = pickle.loads(requests.get('https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/img_data/image_features_embeddingWOMEN3.pkl').content)
    features = extract_img_features_from_file(file, model)
    img_distence, img_indicess = recommendd(features, features_list)
    results = []
    
    for result in img_indicess[0][(pageNumber*10)-10:pageNumber*10]:
        results.append(img_files_list[result])
        
    return results

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

def recommendd(features, features_list):
    #neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    # neighbors.fit(features_list)

    neighbors = NearestNeighbors(n_neighbors=len(
        features_list), algorithm='brute', metric='euclidean')
    neighbors.fit(features_list)
        
    distence, indices = neighbors.kneighbors([features])
    return distence, indices