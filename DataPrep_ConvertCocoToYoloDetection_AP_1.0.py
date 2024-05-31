"""
Script Name: DataPrep_ConvertCocoToYoloDetection_AP_1.0.py
Description: Script that converts COCO JSON file to Yolo txt files for all images in the dataset for object detection tasks.
Created Date: 2024-04
Author: Ana Petrovic 
Version: 1.0
Last Modified: 2024-05-22
Modified by: Ana Petrovic

Example Usage:
python DataPrep_ConvertCocoToYoloDetection_AP_1.0.py path/to/your/coco/json path/to/output/folder

Dependencies:
json, argparse
"""
import json
import argparse

# Define input and output path that represent coco and yolo datasets
input_path = '/mnt/c/projects/useful-scripts/PlanetSoft_rooftops_dataset/coco.json'
output_path = '/mnt/c/projects/useful-scripts/yolo-detection'


def convert_from_coco_to_yolo_format(input_path, output_path):

    # Read JSON Annotation file
    f = open(input_path)
    data = json.load(f)

    # Read annotations for every image id
    bounding_boxes = []

    for annotation in data['annotations']:

        image_id = annotation['image_id']
        bounding_box = annotation['bbox']
        category_id = annotation['category_id']

        bounding_boxes.append([image_id, bounding_box, category_id])

    # Calculate midpoints for every image id, normalize them and then write objects in .txt file
    for image in data['images']:

        img_w = image['width']
        img_h = image['height']
        image_id = image['id']
        file_name = image['file_name']
        file_name = file_name.rsplit('.', 1)[0]

        lines_for_image_id = []

        for bbox_item in bounding_boxes:
            if bbox_item[0] == image_id:
                x = bbox_item[1][0]
                y = bbox_item[1][1]
                w = bbox_item[1][2]
                h = bbox_item[1][3]
                category_id = bbox_item[2]

                # Find midpoints
                x_center = x + (w / 2)
                y_center = y + (h / 2)

                # Normalization of midpoints
                x_center = x_center / img_w
                y_center = y_center / img_h
                w = w/img_w
                h = h/img_h

                # Fix number of decimal places
                x_center = format(x_center, '.6f')
                y_center = format(y_center, '.6f')
                w = format(w, '.6f')
                h = format(h, '.6f')

                line = f"{category_id} {x_center} {y_center} {w} {h}\n" 

                lines_for_image_id.append(line)
                

        # Write objects in txt file
        with open(f"{output_path}/{file_name}.txt", "a") as file_object:
            file_object.writelines(lines_for_image_id)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO JSON file to Yolo txt files for all images in the dataset.")
    parser.add_argument('input_path', type=str, help="Path to the COCO JSON file")
    parser.add_argument('output_path', type=str, help="Path to the output folder where YOLO txt files will be saved")

    args = parser.parse_args()
    convert_from_coco_to_yolo_format(input_path=args.input_path, output_path=args.output_path)

