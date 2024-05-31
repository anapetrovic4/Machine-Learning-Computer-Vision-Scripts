"""
Script Name: Convert_PCD_To_Txt_AP_1.0.py
Description: A script that converts PCD file to TXT file.
Created Date: 2024-05
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-31
Modified by: Ana Petrovic

Example Usage:
python Convert_PCD_To_Txt_AP_1.0.py /path/to/input.pcd /path/to/output/directory

Dependencies:
os, numpy, open3d, argparse
"""
import os
import argparse
import open3d as o3d

def convert_pcd_to_txt(input_file, output_dir):
    # Read the point cloud data from the PCD file
    cloud = o3d.io.read_point_cloud(input_file)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_path = os.path.join(output_dir, "downsampled_output.txt")

    # Write point cloud data to text file
    with open(output_path, 'w') as f:
        for i in range(len(cloud.points)):
            # Extract RGB values
            rgb = cloud.colors[i]
            r = int(rgb[0] * 256)
            g = int(rgb[1] * 256)
            b = int(rgb[2] * 256)

            # Write the point cloud data to the file
            f.write(f"{cloud.points[i][0]} {cloud.points[i][1]} {cloud.points[i][2]} {r} {g} {b}\n")

    print("Saved point cloud in:", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a downsampled PCD file to a downsampled TXT file.")
    parser.add_argument('input_file', type=str, help='Path to the input PCD file.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory.')

    args = parser.parse_args()
    convert_pcd_to_txt(args.input_file, args.output_dir)