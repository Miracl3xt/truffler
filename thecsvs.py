import os
import json
import csv

# Define the input directory containing JSON files
input_directory = "/Users/path/"  # Replace with the actual path

# Function to recursively extract fields from a JSON object
def extract_fields(json_obj, parent_key='', separator='.'):
    items = {}
    for key, value in json_obj.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(extract_fields(value, new_key, separator))
        else:
            items[new_key] = value
    return items

# Iterate through JSON files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_directory, filename)
        
        # Read JSON data from the file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Create a list to store CSV data
        csv_data = []
        
        # Iterate through each object in the JSON data
        for item in data:
            # Extract all fields for the current JSON object
            csv_entry = extract_fields(item)
            csv_data.append(csv_entry)
        
        # Define the CSV file name
        csv_file_name = os.path.splitext(filename)[0] + '.csv'
        csv_file_path = os.path.join(input_directory, csv_file_name)
        
        # Get all unique field names from the JSON objects
        fieldnames = set()
        for entry in csv_data:
            fieldnames.update(entry.keys())
        
        # Write the data to a CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(fieldnames))
            writer.writeheader()
            for entry in csv_data:
                writer.writerow(entry)
        
        print(f"Data from {filename} has been parsed and saved to {csv_file_name}")
