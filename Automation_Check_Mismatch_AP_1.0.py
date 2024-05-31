"""
Script Name: Automation_Check_Mismatch_AP_1.0.py
Description: A script that checks if there are mismatches in images vs masks and deletes those mismatches.
Created Date: 2024-04
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-20
Modified by: Ana Petrovic

Example Usage:
python Automation_Check_Mismatch_AP_1.0.py /path/to/your/images/folder /path/to/your/masks/folder

***Note***:
Image name format: image_X_XX
Mask name format: mask_X_XX

Compare image and mask name by X_XX. If your images and annotations have different formats, the code needs to be updated for you specific case.

Dependencies:
os, argparse

"""

import os
import argparse

# Extract substrings from images and masks names, check if there is a mismatch and then delete those files
def check_mismatch(images_folder, masks_folder):

    images_dir = [i for i in os.listdir(images_folder) if i.endswith(('.jpg'))]
    masks_dir = [i for i in os.listdir(masks_folder) if i.endswith(('.tif'))]

    # Extract image and labels names
    image_names = [os.path.splitext(i)[0] for i in images_dir]
    mask_names = [os.path.splitext(i)[0] for i in masks_dir]

    substring_images = [i[5:10] for i in image_names]
    substring_masks = [i[4:9] for i in mask_names]

    mismatched_images = [image for image in substring_images if image not in substring_masks]
    mismatched_masks = [mask for mask in substring_masks if mask not in substring_images]

    print(mismatched_images)
    print(mismatched_masks)


    for mismatched_image in mismatched_images:
        mismatched_image_filename = f'image{mismatched_image}.jpg'
        mismatched_image_path = os.path.join(images_folder, mismatched_image_filename)
        if os.path.exists(mismatched_image_path):
            os.remove(mismatched_image_path)
            print(f"Deleted: {mismatched_image_filename}")

    for mismatched_mask in mismatched_masks:
        mismatched_mask_filename = f'mask{mismatched_mask}.tif'
        mismatched_mask_path = os.path.join(masks_folder, mismatched_mask_filename)
        if os.path.exists(mismatched_mask_path):
            os.remove(mismatched_mask_path)
            print(f"Deleted: {mismatched_mask_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for checking mismatches in images vs masks and deleting those mismatches.")
    parser.add_argument("images_folder", type=str, help="Path to the folder containing images.")
    parser.add_argument("masks_folder", type=str, help="Path to the folder containing masks.")
    args = parser.parse_args()

    check_mismatch(args.images_folder, args.masks_folder)
