import numpy as np
from sklearn.model_selection import train_test_split
import os
import argparse
import shutil

# Read images and labels from folders and then split them in train test folders in 80:20 ratio

parser = argparse.ArgumentParser(description='Paths to images and annotations')

parser.add_argument('downsized_images', type=str, help='Path to downsized images')
parser.add_argument('downsized_jsons', type=str, help='Path to downsized jsons')

args = parser.parse_args()

downsized_images = args.downsized_images
downsized_jsons = args.downsized_jsons

list_images = os.listdir(downsized_images)
list_labels = os.listdir(downsized_jsons)

arr_images = np.array(list_images)
arr_labels = np.array(list_labels)

X_train, X_test, y_train, y_test = train_test_split(arr_images, arr_labels,
                                                    random_state=104,
                                                    test_size=0.2,
                                                    shuffle=True)

# Create output folders
train_images = '/mnt/c/projects/ttpla-dataset-yolo-segmentation/dataset/train/images'
test_images = '/mnt/c/projects/ttpla-dataset-yolo-segmentation/dataset/test/images'
train_labels = '/mnt/c/projects/ttpla-dataset-yolo-segmentation/dataset/train/labels'
test_labels = '/mnt/c/projects/ttpla-dataset-yolo-segmentation/dataset/test/labels'

# Copy files in corresponding folders

for img_file in X_train:
    shutil.copy(os.path.join(downsized_images, img_file), train_images)

for img_file in X_test:
    shutil.copy(os.path.join(downsized_images, img_file), test_images)
    
for lbl_file in y_train:
    shutil.copy(os.path.join(downsized_jsons, lbl_file), train_labels) 
       
for lbl_file in y_test:
    shutil.copy(os.path.join(downsized_jsons, lbl_file), test_labels)