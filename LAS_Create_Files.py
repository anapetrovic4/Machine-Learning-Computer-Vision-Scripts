"""
Script Name: LAS_Create_Files.py
Description: A script that converts a TXT file with point cloud data and labels to a LAS file.
Created Date: 2024-05
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-31
Modified by: Ana Petrovic

Example Usage:
python LAS_Create_Files.py /path/to/input.txt /path/to/labels.txt /path/to/output.las

Dependencies:
laspy, pandas, numpy, argparse
"""

import laspy
import numpy as np
import pandas as pd
import argparse

# Read txt and labels

def convert_txt_to_las(txt_file, labels_file, output_las_file):
    # Read txt and labels
    raw = pd.read_csv(txt_file, sep=' ', header=None).values
    labels = pd.read_csv(labels_file, header=None).values[:,0]

    # Extract coordinate, color, and intensity
    xyz = np.ascontiguousarray(raw[:,0:3], dtype='float32')
    rgb = np.ascontiguousarray(raw[:,3:6], dtype='uint8') * 256

    # Create header
    header = laspy.header.LasHeader(point_format=7)
    mins = np.floor(np.min(xyz,axis=0))
    header.offsets = mins
    header.scale = [0.01,0.01,0.01]

    # Create empty las file
    las = laspy.LasData(header)

    # Write dimensions to the las file
    las.x = xyz[:,0]
    las.y = xyz[:,1]
    las.z = xyz[:,2]
    las.red = rgb[:,0]
    las.green = rgb[:,1]
    las.blue = rgb[:, 2]
    las.classification = labels

    # Write to output las file
    las.write(output_las_file)

def main():
    parser = argparse.ArgumentParser(description="Converts txt and labels files to las format")
    parser.add_argument("txt_file", type=str, help="Path to the input txt file")
    parser.add_argument("labels_file", type=str, help="Path to the input labels file")
    parser.add_argument("output_las_file", type=str, help="Path to the output las file")
    args = parser.parse_args()

    convert_txt_to_las(args.txt_file, args.labels_file, args.output_las_file)

    # Read las file
    with laspy.open(args.output_las_file) as fh:
        print('Points from header ', fh.header.point_count)
        las = fh.read()
        print(las)
        print('Points from data ', len(las.points))
        ground_pts = las.classification == 2
        print('type of ground pts', type(ground_pts))
        print('shape of ground pts ', ground_pts.shape)
        bins, counts = np.unique(ground_pts, return_counts=True)
        print('Ground point return number distribution:')
        for r,c in zip(bins,counts):
            print('     {}:{}'.format(r,c))
            
    # Print basic information
    las_file = laspy.read(args.output_las_file)
    print("LAS Header:")
    print("Version:", las_file.header.version)
    print("Point format:", las_file.header.point_format)
    print("Number of points:", las_file.header.point_count)
    print("Number of points by return:", las_file.header.point_records_count)

    print("\nFirst 10 points:")
    for i in range(10):
        print("Point", i+1, ":", las_file.x[i], las_file.y[i], las_file.z[i], las_file.red[i], las_file.green[i], las_file.blue[i])

if __name__ == "__main__":
    main()
