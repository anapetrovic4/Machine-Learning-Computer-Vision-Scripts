"""
Script Name: Check_Class_Occurences_AP_1.0.py
Description: A script that processes text files in a directory to find unique first characters in each file.
Created Date: 2024-04
Author: Ana Petrovic
Version: 1.0
Last Modified: 2024-05-31
Modified by: Ana Petrovic

Example Usage:
python Check_Class_Occurences_AP_1.0.py /path/to/your/folder

Dependencies:
os, argparse
"""
import os
import argparse

def unique_first_chars(folder_path):
    unique_chars = {}
    files_first_appearance = {}

    # Iterate through all files in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                for line in file:
                    if line:  # Check if line is not empty
                        first_char = line[0]
                        if first_char not in unique_chars:
                            unique_chars[first_char] = True
                            files_first_appearance[first_char] = filename

    return list(unique_chars.keys()), files_first_appearance

def main(folder_path):
    unique_values, first_appearance_files = unique_first_chars(folder_path)
    print("Unique first characters:", unique_values)
    print("First appearance in files:", first_appearance_files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text files in a directory to find unique first characters.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing text files.')

    args = parser.parse_args()
    main(args.folder_path)