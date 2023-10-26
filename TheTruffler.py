import os
import subprocess
import json

def run_trufflehog_and_correct_json(directory_path):
    # List all paths in the directory
    all_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path)]

    # Create a dictionary to store the results
    results = {}

    for path in all_paths:
        command = f"trufflehog filesystem {path} --json"
        try:
            process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if process.returncode == 0:
                # Capture the standard output
                stdout = process.stdout
                results[path] = stdout

                # Save the result to a JSON file
                save_path = f"{path}.json"
                with open(save_path, "w") as json_file:
                    json_file.write(stdout)

                # Correct and validate the JSON
                corrected_json = correct_and_validate_json(save_path)
                if corrected_json:
                    results[path] = corrected_json
            else:
                # Handle errors from the trufflehog command
                print(f"Error running trufflehog for {path}: {process.stderr}")
        except Exception as e:
            # Handle general exceptions
            print(f"Error running trufflehog for {path}: {str(e)}")

    return results

def correct_and_validate_json(input_file):
    try:
        with open(input_file, 'r') as infile:
            corrected_data = []
            for line in infile:
                try:
                    data = json.loads(line)
                    corrected_data.append(data)
                except json.JSONDecodeError:
                    print(f"Ignoring invalid JSON: {line}")

        corrected_json = json.dumps(corrected_data, indent=4)
        return corrected_json
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")
        return None

directory_path = "/Users/PATH"
results = run_trufflehog_and_correct_json(directory_path)

# Print or further process the results dictionary
for path, result in results.items():
    print(f"Results for {path}:")
    print(result)
