"""
Script Name: DataPrep_Combine_Individual_Jsons_To_COCO_AP_1.0.py
Description: A script that combines indiviual JSON files for segmentation into a single COCO JSON file structure.
Created Date: 2024-04
Author: Aleksandar Lukic, Ana Petrovic
Version: 1.0
Last Modified: 2024-05-21
Modified by: Ana Petrovic

Example Usage:
python DataPrep_Combine_Individual_Jsons_To_COCO_AP_1.0.py

Dependencies:
os, json, glob, argparse

"""
import os
import json
import glob
import argparse

# Function that combines multiple json files into a single json file with coco structure
def combine_jsons(folder_path, output_file):
    json_files = glob.glob(f'{folder_path}/*.json')

    coco_structure = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "cable"},
            {"id": 2, "name": "tower_lattice"},
            {"id": 3, "name": "tower_wooden"},
            {"id": 4, "name": "tower_tucohy"},
            {"id": 5, "name": "void"}
        ]
    }
    category_mapping = {"cable": 1, "tower_lattice": 2, "tower_wooden": 3, "tower_tucohy": 4, "void": 5}
    annotation_id = 1

    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)
            image_id = len(coco_structure["images"]) + 1
            coco_structure["images"].append({
                "width": 512,
                "height": 512,
                "id": image_id,
                "file_name": data.get("imagePath", "unknown"),
                # Add other image details as required
            })

            for shape in data.get("shapes", []):
                label = shape.get("label")
                if label in category_mapping:  # Ensure the label exists in TTPLA categories
                    coco_structure["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_mapping[label],
                        "segmentation": [list(sum(shape.get("points", []), []))],  # Flatten the points list
                        "bbox": [],  # Calculate bounding box if necessary
                        "ignore": 0,
                        "iscrowd": 0,
                        "area": 0,  # Calculate area if necessary
                    })
                    annotation_id += 1

    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write the combined COCO data to a new file
    with open(output_file, 'w') as f:
        json.dump(coco_structure, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine individual JSON files into a single COCO JSON file.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing input JSON files')
    parser.add_argument('output_file', type=str, help='Path to the output combined JSON file')

    args = parser.parse_args()

    combine_jsons(args.input_folder, args.output_file)