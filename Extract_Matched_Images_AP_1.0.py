import os
from PIL import Image
import argparse
import shutil
import glob

parser = argparse.ArgumentParser(description='Paths to images and annotations')

parser.add_argument('original_jsons', type=str, help='Path to original jsons')
parser.add_argument('data_original_size', type=str, help='Path to data with original sizes')
parser.add_argument('original_images', type=str, help='Path to data with original jsons')
args = parser.parse_args()

# Accessing the values of the arguments
original_jsons = args.original_jsons
data_original_size = args.data_original_size
original_images = args.original_images

img_files = glob.glob(os.path.join(data_original_size, '*.jpg'))
print('Number of .jpg files:', len(img_files))
print(img_files[:10])

# Copy images in original images
for img_file in img_files:
    img_name = os.path.basename(img_file)
    print('basename ', img_name)
    img_path = os.path.join(data_original_size, img_name)
    if not os.path.exists(os.path.join(original_images, img_name)):
        shutil.copy(img_file, original_images)
    else:
        pass

img_to_delete = []

# Extract file name without extensions from original jsons
list_original_jsons = [os.path.splitext(json_file)[0] for json_file in os.listdir(original_jsons)]

# Check mismatched images by comparing file names in img files vs original jsons
for img_file in img_files:
    img_name = os.path.basename(img_file)
    if os.path.splitext(img_name)[0] not in list_original_jsons:
        img_to_delete.append(img_name)
        
print('Number of mismatched images to delete', len(img_to_delete))
print('List of original jsons ', list_original_jsons[:10])
print('List of original images ', img_files[:10])

list_original_images = os.listdir(original_images)

for file in img_to_delete:
    if file in list_original_images:
        path = os.path.join(original_images, file)
        if(os.path.exists(path)):
            os.remove(path)
        else:
            print('File already deleted ', path)