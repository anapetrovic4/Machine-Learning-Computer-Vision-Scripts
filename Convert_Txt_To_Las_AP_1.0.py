"""
Script Name: Convert_Txt_To_Las_AP_1.0.py
Description: A script that converts a TXT file with point cloud data to a LAS file.
Created Date: 2024-05
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-31
Modified by: Ana Petrovic

Example Usage:
python Convert_Txt_To_Las_AP_1.0.py /path/to/input/directory /path/to/output/directory

Dependencies:
os, pandas, numpy, laspy, argparse
"""
import os
import numpy as np
import pandas as pd
import laspy
import argparse

fileNames = {   "birdfountain_station1_xyz_intensity_rgb" : "birdfountain1",
                "castleblatten_station1_intensity_rgb" : "castleblatten1",
                "castleblatten_station5_xyz_intensity_rgb" : "castleblatten5",
                "marketplacefeldkirch_station1_intensity_rgb" : "marketsquarefeldkirch1",
                "marketplacefeldkirch_station4_intensity_rgb" : "marketsquarefeldkirch4",
                "marketplacefeldkirch_station7_intensity_rgb" : "marketsquarefeldkirch7",
                "sg27_station3_intensity_rgb" : "sg27_3",
                "sg27_station6_intensity_rgb" : "sg27_6",
                "sg27_station8_intensity_rgb" : "sg27_8",
                "sg27_station10_intensity_rgb" : "sg27_10",
                "sg28_station2_intensity_rgb" : "sg28_2",
                "sg28_station5_xyz_intensity_rgb" : "sg28_5",
                "stgallencathedral_station1_intensity_rgb" : "stgallencathedral1",
                "stgallencathedral_station3_intensity_rgb" : "stgallencathedral3",
                "stgallencathedral_station6_intensity_rgb" : "stgallencathedral6",}

path = "D:/semantic3d/las"
files = os.listdir(path)
# files = ["bildstein_station1_xyz_intensity_rgb.txt"]



def SaveToLas(file_path, xyz, intensity = None, rgb = None, labels = None, scale_rgb_intensity = 65535, compress = False):
    """
    Expected pointcloud

    point_format=2
    X	    X (x for scaled)	long[1] (4)
    Y	    Y (y for scaled)	long[1] (4)
    Z	    Z (z for scaled)	long[1] (4)
    Intensity	intensity	unsigned short[1] (2)
    (Flag Byte)	flag_byte	unsigned byte[1] (1)
    (Classification Byte)	raw_classification	unsigned byte[1] (1)
    User Data	user_data	unsigned char[1] (1)
    Point Source Id	pt_src_id	unsigned short[1] (2)
    Red	red	unsigned short[1] (2)
    Green	green	unsigned short[1] (2)
    Blue	blue	unsigned short[1] (2)

    """
    new_las = laspy.create(file_version="1.4", point_format=8)
    new_las.header.are_points_compressed = compress
    new_las.header.offsets = list(np.floor(xyz.min(0)[:3]))
    new_las.header.scales = [
        0.001,
        0.001,
        0.001,
    ]  # scale lets you save decimal places. in this case 3 values after decimal point

    xyz = (xyz[:, :3] - np.array(new_las.header.offsets)) / np.array(new_las.header.scales)
    xyz = xyz.astype(np.float64)

    new_las.X = xyz[:, 0]
    new_las.Y = xyz[:, 1]
    new_las.Z = xyz[:, 2]

    if intensity is not None:
        new_las.intensity = (intensity * scale_rgb_intensity).flatten().astype(np.uint16)

    if rgb is not None:
        rgb = rgb * scale_rgb_intensity
        new_las.red = rgb[:, 0].astype(np.uint16)
        new_las.green = rgb[:, 1].astype(np.uint16)
        new_las.blue = rgb[:, 2].astype(np.uint16)

    if labels is not None:
        if labels.max() > 31:
            assert f"labels.max() == {labels.max()}. Las 1.4 supports up to 31 class number"

        new_las.classification = labels.flatten().astype(np.uint8)  # ubyte == uint8

    new_las.write(file_path)
    
def convert_txt_to_las(input_dir, output_dir):
    files = os.listdir(input_dir)

    for file in files:
        if file.endswith(".labels"):
            base_filename = file.replace(".labels", "")
            
            txtfile = os.path.join(input_dir, base_filename + ".txt")
            lblfile = os.path.join(input_dir, file)
            lasfile = os.path.join(output_dir, base_filename + ".las")
            
            if os.path.exists(lasfile):
                continue
            
            pointcloud = np.array(pd.read_csv(txtfile, sep=" ", dtype=np.float64, header=None), dtype=np.float64)        
            labels = np.array(pd.read_csv(lblfile, header=None))

            SaveToLas(lasfile, pointcloud[:, :3], pointcloud[:, 3], pointcloud[:, 4:7], labels)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a TXT file with point cloud data to a LAS file.")
    parser.add_argument('input_dir', type=str, help='Path to the input directory containing TXT and labels files.')
    parser.add_argument('output_dir', type=str, help='Path to the output directory where LAS files will be saved.')

    args = parser.parse_args()
    convert_txt_to_las(args.input_dir, args.output_dir)