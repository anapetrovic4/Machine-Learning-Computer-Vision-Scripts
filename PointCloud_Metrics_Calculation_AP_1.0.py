"""
Script Name: PointCloud_Metrics_Calculation_AP_1.0.py
Description: A script that calculates the 2D area of a geo-referenced point cloud and estimates point density per square meter.
Created Date: 2024-05-27
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-27
Modified by: Ana Petrovic

Example Usage:
python PointCloud_Metrics_Calculation_AP_1.0.py /path/to/your/pointcloud.pcd

Dependencies:
open3d, numpy, tqdm, shapely, argparse

"""

import open3d as o3d
import numpy as np
from tqdm import tqdm
from shapely.geometry import Polygon, MultiPoint
import argparse

def main(input_file):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(input_file)

    print('Number of points:', len(pcd.points))

    # Extract x, y, z coordinates from point cloud
    points = np.asarray(pcd.points)
    points_xy = points[:, :2]

    # Convert to list of tuples
    points_xy_tuple = [tuple(row) for row in points_xy]

    # Create convex hull
    boundaries = MultiPoint(points_xy_tuple).convex_hull

    # Calculate area
    area = boundaries.area
    print('Area:', area)

    # Calculate density per square meter
    density_per_sq_m = len(pcd.points) / area
    print('Density per square meter:', density_per_sq_m)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Point cloud processing script.")
    parser.add_argument('input_file', type=str, help='Path to the input point cloud file')

    args = parser.parse_args()
    main(args.input_file)
