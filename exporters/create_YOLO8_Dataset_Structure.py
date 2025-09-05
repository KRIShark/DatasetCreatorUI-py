import os
import json
import cv2
import numpy as np
import shutil

IMAGES_PATH = 'images/'
LABELS_PATH = 'labels/'

LABELS_NAMES_PATH = 'labels.txt'

def get_labls(labels_names: list) -> str:
    labels = ""
    for label in labels_names:
        labels += f"'{label}',"

    return labels[:-1]


def main(training_valid_ratio=0.8) -> None:

    current_path = os.getcwd()

    #creat directories dataset
    os.makedirs(os.path.join(current_path, "dataset"), exist_ok=True)
    os.makedirs(os.path.join(current_path,"dataset", "train"), exist_ok=True)
    os.makedirs(os.path.join(current_path,"dataset", "valid"), exist_ok=True)

    os.makedirs(os.path.join(current_path,"dataset", "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(current_path,"dataset", "train", "labels"), exist_ok=True)

    os.makedirs(os.path.join(current_path,"dataset", "valid", "images"), exist_ok=True)
    os.makedirs(os.path.join(current_path,"dataset", "valid", "labels"), exist_ok=True)

    images_for_train = []
    images_for_valid = []

    #get all images
    images = os.listdir(IMAGES_PATH)

    labels_names = []

    #get all labels names
    with open(LABELS_NAMES_PATH, 'r') as file:
        lines = file.readlines()
        for line in lines:
            labels_names.append(line.split(';')[1].replace('\n', ''))

    #get ramdom images for train and valid by the given percentage
    images_for_train = np.random.choice(images, int(len(images)*training_valid_ratio), replace=False)
    images_for_valid = [image for image in images if image not in images_for_train]

    #copy images to train
    for image in images_for_train:
        shutil.copy(os.path.join(IMAGES_PATH, image), os.path.join(current_path, "dataset", "train", "images" , image))

        label_name = image.replace('.jpg', '.txt')    

        shutil.copy(os.path.join(LABELS_PATH, label_name), os.path.join(current_path, "dataset", "train", "labels", label_name))

    #copy images to valid
    for image in images_for_valid:
        shutil.copy(os.path.join(IMAGES_PATH, image), os.path.join(current_path, "dataset", "valid", "images", image))

        label_name = image.replace('.jpg', '.txt')    

        shutil.copy(os.path.join(LABELS_PATH, label_name), os.path.join(current_path, "dataset", "valid", "labels", label_name))

    #create data.yml
    with open(os.path.join(current_path, "dataset", "data.yml"), 'w') as file: 
        training = os.path.join(current_path, 'dataset', 'train')
        validate = os.path.join(current_path, 'dataset', 'valid')

        training = training.replace('\\', '/') + '/images'
        validate = validate.replace('\\', '/') + '/images'

        file.write(f"train: {training}\n")
        file.write(f"val: {validate}\n")
        file.write("\n")
        file.write(f"nc: {len(labels_names)}\n")
        file.write(f"names: [{get_labls(labels_names)}]\n")


if __name__ == '__main__':
   training_valid_ratio = 0.8

   main(training_valid_ratio=training_valid_ratio)
