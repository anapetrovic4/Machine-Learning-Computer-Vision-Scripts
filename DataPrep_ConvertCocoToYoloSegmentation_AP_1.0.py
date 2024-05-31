"""
Script Name: DataPrep_ConvertCocoToYoloSegmentation_AP_1.0.py
Description: Script that converts COCO JSON file to Yolo txt files for all images in the dataset for image segmentation tasks.
Created Date: 2024-04
Author: Ana Petrovic 
Version: 1.0
Last Modified: 2024-05-22
Modified by: Ana Petrovic

Example Usage:
python DataPrep_ConvertCocoToYoloSegmentation_AP_1.0.py path/to/your/coco/json path/to/output/folder

Dependencies:
json, argparse
"""
import json
import argparse

# Define input and output path that represent coco and yolo datasets

def convert_coco_to_yolo_segmentation(input_path, output_path):
    
    # Load JSON file
    with open(input_path) as f:
        data = json.load(f)

    norm_points = []
    
    counter = 0
    
    for image in data['images']:
        image_id = image['id']
        width = image['width']
        height = image['height']
        file_name = image['file_name']
        #file_name = file_name.rsplit('.', 1)[0] # Extract file name from its extension. This part can be adjusted to your needs.
        file_name = file_name.replace(".png", "")
        
        segmentation_and_category = []
        # Check if the image file name is the desired one ("1_00259")
        #if image_name != target_image_name:
        #    continue  # Skip the rest of the loop and move to the next image
            
        for annotation in data['annotations']:
            if(annotation['image_id'] == image_id): 
                counter += 1
                image_id = annotation['image_id']
                segmentation = annotation['segmentation']
                category_id = annotation['category_id']

                segmentation_and_category.append([category_id, segmentation])

        seg_counter = 0

        for segmentation_item in segmentation_and_category:
            seg_counter += 1
            #if(image_name == target_image_name):
            #    print(f"Seg num {seg_counter}, seg BEFORE norm: {segmentation_item}")
            cat_id = segmentation_item[0]
            seg_points = segmentation_item[1]

            #print(f"No {seg_counter}, cat id: {cat_id}, list of seg points: {seg_points}")

            # Normalize seg points for every segmentation item
            for list_of_points in seg_points:

                # Zip (x, y) coordinates
                seg_points_zip = zip(list_of_points[::2], list_of_points[1::2]) 

                # Perform normalization and round results to have 4 decimals
                # Check if there are any values > 1 or < 0, and then post-process them
                norm_points = [f"({(max(0.0, min(x/width, 1.0)))}, {(max(0.0, min(y/height, 1.0)))})" for x, y in seg_points_zip] 

                norm_points.insert(0, str(cat_id))
                #print('normalized points for each category id ', norm_points)

                # Format text to write in .txt file
                result = ' '.join(value.strip("(),") for item in norm_points for value in item.split())
                result += '\n'
                
                #if(image_name == target_image_name):
                #    print(f"Seg num {seg_counter}, seg AFTER norm: ", result)

                # Write objects in txt file
                with open(f"{output_path}/{file_name}.txt", "a") as file_object:
                    file_object.writelines(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO JSON file to Yolo txt files for all images in the dataset for image segmentation.")
    parser.add_argument('input_path', type=str, help="Path to the COCO JSON file")
    parser.add_argument('output_path', type=str, help="Path to the output folder where YOLO txt files will be saved")

    args = parser.parse_args()
    convert_coco_to_yolo_segmentation(input_path=args.input_path, output_path=args.output_path)