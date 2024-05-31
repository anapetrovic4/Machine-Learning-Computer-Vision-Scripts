import json
import os
import numpy as np
import argparse

# From downsized_jsons, read each JSON file and extract unique values for the key 'label'

# Parse paths to desired folders
parser = argparse.ArgumentParser(description='Path to downsized jsons')
parser.add_argument('downsized_jsons', type=str, help='Path to downsized jsons')
args = parser.parse_args()
downsized_jsons = args.downsized_jsons

list_downsized_jsons = os.listdir(downsized_jsons)

labels = []

# Access keys that represent labels 
for file in list_downsized_jsons:
    file_path = os.path.join(downsized_jsons, file)
    with open(file_path, 'r') as json_file:
        current_json = json.load(json_file)
        
        shapes = current_json.get('shapes')
        
        if shapes:
        
            for shape in shapes:
                label_value = shape.get('label')

                if label_value:
                    labels.append(label_value)

print(len(labels))

# Convert list to numpy array to find unique values that represent classes
labels_arr = np.array(labels)        
unique_labels_arr = np.unique(labels_arr)
print(unique_labels_arr)