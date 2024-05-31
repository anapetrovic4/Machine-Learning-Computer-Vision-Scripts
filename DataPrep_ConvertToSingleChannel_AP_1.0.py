"""
Script Name: DataPrep_ConvertToSingleChannel_AP_1.0.py
Description: Script that converts multi-channel images to single-channel images based on a predefined mapping.
Created Date: 2024-04
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-22
Modified by: Ana Petrovic

Example Usage:
python DataPrep_ConvertToSingleChannel_AP_1.0.py /path/to/input/dir /path/to/output/dir

Dependencies:
cv2, os, numpy, matplotlib, argparse
"""
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Create dictionary
single_channel = {
    (0, 0, 0) : 0,
    (1, 1, 1) : 1,
    (2, 2, 2) : 2,
    (3, 3, 3) : 3,
    (4, 4, 4) : 4,
    (5, 5, 5) : 5,
    (6, 6, 6) : 6,
    (7, 7, 7) : 7,
    (8, 8, 8) : 8,
    (9, 9, 9) : 9,
}

def convert_to_single_channel(input_dir, output_dir, map):
    
    # Iterate through files of masks
    for filename in os.listdir(input_dir):
        # Only include files that end with .png and create paths for input and output 
        if filename.endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Load each image
            image = cv2.imread(input_path)
            
            # If there is an image, create new matrix with single channel in 3rd dimension, and make it store integers
            if image is not None:
                single_channel_image = np.zeros_like(image[:,:,0], dtype=np.uint8)
                # Iterate through dictionary
                for key, value in single_channel.items():
                    # For all occurences check if image is equal to dict. key (we convert it in numpy array), and if it is True, we store boolean values in mask array
                    mask = np.all(image == np.array(key), axis=2)
                    # When the condition is met, assing the value to the array (Boolean indexing NumPy)
                    single_channel_image[mask] = value
                    
                cv2.imwrite(output_path, single_channel_image)
            
            else:
                print(f'Failed to load image from {input_path}')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert multi-channel images to single-channel images based on a predefined mapping.")
    parser.add_argument('input_dir', type=str, help="Path to the input directory containing the images")
    parser.add_argument('output_dir', type=str, help="Path to the output directory where the converted images will be saved")

    args = parser.parse_args()
    
    convert_to_single_channel(args.input_dir, args.output_dir, single_channel)