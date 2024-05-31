"""
Script Name: PointCloud_Filtering_NoiseReduction.py
Description: This script applies various filtering techniques (e.g., statistical outlier removal, radius outlier removal) to clean up the point cloud data.
Created Date: 2024-05-27
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-27
Modified by: Ana Petrovic

Example Usage:
python PointCloud_Filtering_NoiseReduction_AP_1.0.py /path/to/your/pointcloud.pcd --voxel_size 0.02 --nb_neighbors 20 --std_ratio 2.0 --nb_points 20 --radius 1.0 --func False

Dependencies:
open3d, numpy, matplotlib, argparse
"""
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Prepare input data
counter = 0

# Function to visualize point cloud
def visualize_point_cloud(points):
    global counter

    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')

    z = points[:, 2]

    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=z, cmap='viridis', marker='o')

    color_bar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    color_bar.set_label('Z Coordinate')

    plt.show()

    filename = f'image_{counter}.png'

    counter += 1

    plt.savefig(filename)

# Downsample 
def down_sample(pcd, voxel_size):
    voxel_down_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
    return voxel_down_pcd

# Statistical outlier removal
def stat_outlier_removal(pcd, voxel_size, nb_neighbors, std_ratio, apply_downsample):
    if apply_downsample:
        pcd = down_sample(pcd, voxel_size)
    cloud, id = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio, print_progress=True)
    return cloud

# Radius outlier removal
def rad_outlier_removal(pcd, voxel_size, nb_points, radius, apply_downsample):
    if apply_downsample:
        pcd = down_sample(pcd, voxel_size)
    cloud, id = pcd.remove_radius_outlier(nb_points=nb_points, radius=radius, print_progress=True)
    return cloud

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Filter and reduce noise in point cloud data.")
    parser.add_argument('input_file', type=str, help='Path to the input point cloud file')
    parser.add_argument('--voxel_size', type=float, default=0.02, help='Voxel size for downsampling')
    parser.add_argument('--nb_neighbors', type=int, default=20, help='Number of neighbors for statistical outlier removal')
    parser.add_argument('--std_ratio', type=float, default=2.0, help='Standard deviation ratio for statistical outlier removal')
    parser.add_argument('--nb_points', type=int, default=20, help='Number of points for radius outlier removal')
    parser.add_argument('--radius', type=float, default=1.0, help='Radius for radius outlier removal')
    parser.add_argument('--func', type=bool, default=True, help='Make downsampling optional')
    args = parser.parse_args()

    # Load the point cloud
    pcd = o3d.io.read_point_cloud(args.input_file)

    stat_cleaned_cloud = stat_outlier_removal(pcd=pcd, voxel_size=args.voxel_size, nb_neighbors=args.nb_neighbors, std_ratio=args.std_ratio, apply_downsample=args.func)
    visualize_point_cloud(points=np.asarray(stat_cleaned_cloud.points))

    radius_cleaned_cloud = rad_outlier_removal(pcd=pcd, voxel_size=args.voxel_size, nb_points=args.nb_points, radius=args.radius, apply_downsample=args.func)
    visualize_point_cloud(points=np.asarray(radius_cleaned_cloud.points))

    print('Done!')