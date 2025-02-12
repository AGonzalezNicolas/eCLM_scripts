# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 2025

@author: Ana GNA

This script extracts data from model_timing.000 --> timing file from eCLM
and saves times into a "csv" file
"""


# Import modules

import re
import csv

# Define function to extract times

def find_times_and_sum(files, patterns, cores, output_csv):
    all_times = {}  # Dictionary to store times for each file
    #grand_total = 0  # Overall sum across all files

    for i, filename in enumerate(files):
        times = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if any(pattern in line for pattern in patterns):  # Check for multiple patterns
                        match = re.search(r'\d+\s+-\s+([\d.]+)', line)  # Match any number before '-'
                        if match:
                            times.append(float(match.group(1)))  # Convert to float
            
            file_total = sum(times)  # Sum for the current file
            all_times[filename] = {
                'cores': cores[i],  # Manually provided core count
                'times': times,
                'total': file_total
            }
            #grand_total += file_total  # Update grand total

        except FileNotFoundError:
            print(f"Warning: File '{filename}' not found.")

    # Save data to CSV
    save_to_csv(all_times, patterns, output_csv)

    return all_times #,grand_total  # Return dictionary with all file data + total sum


# Define function to save csv file with times

def save_to_csv(all_times, patterns, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Create header row: "cores" + patterns + "total_time"
        header = ["cores"] + patterns + ["total_time"]
        writer.writerow(header)

        # Write data for each file
        for file, data in all_times.items():
            row = [data['cores']] + data['times'] + [data['total']]  # Cores first, times, then total
            writer.writerow(row)            
            

## INPUT DATA

#file1 = 'C:/Users/Ana/Desktop/Cluster/eCLM_scalability/python_scaling/model_timing.000'

file0 = '../EU_CORDEX_64Tasks/timing/model_timing.00'
file1 = '../EU_CORDEX_1N/timing/model_timing.000'
file2 = '../EU_CORDEX_2N/timing/model_timing.000'
file3 = '../EU_CORDEX_4N/timing/model_timing.000'
file4 = '../EU_CORDEX_8N/timing/model_timing.0000'

files = [file0, file1, file2, file3, file4]              # List of files to process 
cores = [64, 128, 256, 516, 1032]  # Manually provided number of cores for each file
patterns = ["CPL:INIT", "CPL:RUN_LOOP_BSTART", "CPL:RUN_LOOP", "CPL:TPROF_WRITE", "CPL:RUN_LOOP_BSTOP","CPL:FINAL", "sync3_tprof", ]   # Add more patterns as needed

output_csv = "Output_times.csv"  # Output CSV filename

file_results = find_times_and_sum(files, patterns, cores, output_csv)

# Print results
print("\nData saved to", output_csv)
for file, data in file_results.items():
    print(f"\nFile: {file}")
    print("Cores used:", data['cores'])
    print("Extracted times:", data['times'])
    print("File sum of times:", data['total'])

