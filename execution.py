import json
import os

def is_valid_json_filename(filename):
    return filename.endswith(".json") and not filename.startswith("corrected_")

def correct_and_validate_json(input_dir):
    try:
        for filename in os.listdir(input_dir):
            if is_valid_json_filename(filename):
                input_file = os.path.join(input_dir, filename)
                output_file = os.path.join(input_dir, f"corrected_{filename}")

                with open(input_file, 'r') as infile:
                    corrected_data = []
                    for line in infile:
                        try:
                            data = json.loads(line)
                            corrected_data.append(data)
                        except json.JSONDecodeError:
                            print(f"Ignoring invalid JSON in {input_file}: {line}")

                corrected_json = json.dumps(corrected_data, indent=4)

                with open(output_file, 'w') as outfile:
                    outfile.write(corrected_json)

                print(f"JSON file {input_file} corrected and saved to {output_file}")

                try:
                    json.loads(corrected_json)
                    print(f"Corrected JSON in {output_file} is valid.")
                except json.JSONDecodeError as e:
                    print(f"Corrected JSON in {output_file} is not valid: {str(e)}")
    except FileNotFoundError as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    input_dir =  "/Users/PATH"  # Replace this with your directory path
    correct_and_validate_json(input_dir)



# if __name__ == "__main__":
#     input_dir = "/Users/shubham.patil1/Downloads/ANS/ANS2/" # Replace this with your directory path
#     correct_and_validate_json(input_dir)
