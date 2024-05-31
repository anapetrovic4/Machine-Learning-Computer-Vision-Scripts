"""
Script Name: PointCloud_ConcaveHull_Calculation_AP_1.0.py
Description: This script calculates the area of concave hull. 
Created Date: 2024-05-30
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-30
Modified by: Ana Petrovic

Example Usage:
python PointCloud_ConcaveHull_Calculation_AP_1.0.py /path/to/your/pointcloud.pcd --voxel_size 0.02 (If you want to perform downsampling)
python PointCloud_ConcaveHull_Calculation_AP_1.0.py /path/to/your/pointcloud.pcd --no_downsample (If you don't want to perform downsampling)

Dependencies:
open3d, numpy, alphashape, time, argparse
"""
import open3d as o3d
import numpy as np
import alphashape
from time import time
import argparse

# load pcd
def main(pcd_path, voxel_size, downsample):
    pcd = o3d.io.read_point_cloud(pcd_path)

    # down sample
    if downsample:
        print(f'downsampling with voxel size: {voxel_size}')
        pcd = pcd.voxel_down_sample(voxel_size)

    # convert to numpy
    points = np.asarray(pcd.points)
    length = len(points)

    print(f'length is {length}')

    # convert to list of x,y tuples
    points_xy = points[:, :2]

    coordinates = [tuple(row) for row in points_xy]
    print(coordinates[:5])

    # apply alphashape
    t0 = time()

    a = alphashape.alphashape(coordinates, 0.1)
    print(f'alphashape done in {time() - t0}s')
    print(type(a))

    area = a.area
    print(f'area is {area}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process point cloud data to calculate concave hull using alphashape.")
    parser.add_argument("point_cloud_path", type=str, help="Path to the point cloud file (.pcd).")
    parser.add_argument("--voxel_size", type=float, default=0.02, help="Voxel size for downsampling the point cloud.")
    parser.add_argument("--no_downsample", action="store_true", help="Disable downsampling of the point cloud.")
    
    args = parser.parse_args()
    downsample = not args.no_downsample
    main(args.point_cloud_path, args.voxel_size, downsample)