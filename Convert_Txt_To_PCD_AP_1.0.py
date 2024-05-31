"""
Script Name: Convert_Txt_To_PCD_AP_1.0.py
Description: A script that converts a TXT file with point cloud data to a PCD file.
Created Date: 2024-05
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-31
Modified by: Ana Petrovic

Example Usage:
python Convert_Txt_To_PCD_AP_1.0.py /path/to/input.txt /path/to/output.pcd

Dependencies:
os, pandas, numpy, open3d, argparse
"""
import os
import numpy as np
import open3d as o3d
import argparse

def convert_txt_to_pcd(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    data = []

    for line in lines:
        x, y, z, r, g, b = line.strip().split()
        
        x = float(x)
        y = float(y)
        z = float(z)
        
        r = int(r)
        g = int(g)
        b = int(b)
        
        data.append([x, y, z, r, g, b])

    data = np.array(data)
    points = data[:, :3]
    colors = data[:, 3:6] / 255.0  # Normalize RGB values to [0, 1]

    # Create Open3D PointCloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Save to PCD file
    o3d.io.write_point_cloud(output_file, pcd)
    print(f"Saved point cloud to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a TXT file with point cloud data to a PCD file.")
    parser.add_argument('input_file', type=str, help='Path to the input TXT file containing point cloud data.')
    parser.add_argument('output_file', type=str, help='Path to the output PCD file.')

    args = parser.parse_args()
    convert_txt_to_pcd(args.input_file, args.output_file)

    
