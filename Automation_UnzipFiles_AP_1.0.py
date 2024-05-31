"""
Script Name: Automation_UnzipFiles_AP_1.0.py
Description: A script that unzips files from one directory and places extracted files to a new directory.
Created Date: 2024-04
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-20
Modified by: Ana Petrovic

Example Usage:
python Automation_UnzipFiles_AP_1.0.py /path/to/your/zip/folder /path/to/your/output/folder

Dependencies:
os, py7zr, argparse
"""

import os
from py7zr import SevenZipFile
import argparse


# List all zipped files, extract them and save them in a new folder
def unzip_files(zip_dir, output_dir):

    extension = '.7z'
    files = os.listdir(zip_dir)

    for file in files:
        if file.endswith(extension):
            file_path = os.path.join(zip_dir, file)
            with SevenZipFile(file_path, 'r') as zip:
                zip.extractall(output_dir)

    print('Unzipping successful')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unzip files from one directory and place extracted files to a new directory.")
    parser.add_argument("zip_dir", type=str, help="Path to the directory containing zip files")
    parser.add_argument("output_dir", type=str, help="Path to the output directory for the extracted files")
    args = parser.parse_args()

    if not os.path.isdir(args.zip_dir):
        print(f"The provided zip directory does not exist: {args.zip_dir}")
        exit(1)

    if not os.path.isdir(args.output_dir):
        print(f"The provided output directory does not exist: {args.output_dir}")
        exit(1)

    unzip_files(args.zip_dir, args.output_dir)