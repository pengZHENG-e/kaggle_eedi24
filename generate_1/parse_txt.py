# import re
# import json

# def extract_json_data(file_path):
#     json_list = []
    
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     # Use regex to extract the JSON parts within the brackets
#     json_strings = re.findall(r'\[(.*?)\]', content, re.DOTALL)

#     for json_string in json_strings:
#         # Wrap the string with square brackets to form a valid JSON array
#         json_string = f"[{json_string}]"
#         try:
#             # Load the JSON data into a Python list and append it to json_list
#             json_data = json.loads(json_string)
#             json_list.append(json_data)
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
    
#     return json_list

# # Provide the file path to the txt file
# file_path = 'responses.txt'
# json_data_list = extract_json_data(file_path)

# # json_data_list will now contain the extracted JSON data from the file
# # print(json_data_list)
# print(len(json_data_list))

import re
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(filename='json_extraction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_json(json_string):
    # Replace invalid escapes
    json_string = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', json_string)
    
    # Ensure all property names are quoted
    json_string = re.sub(r'(\w+)(?=\s*:)', r'"\1"', json_string)
    
    # Remove control characters
    json_string = ''.join(ch for ch in json_string if ord(ch) >= 32)
    
    return json_string

def extract_json_data(file_path):
    json_list = []
    error_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regex to extract the JSON parts within the brackets
    json_strings = re.findall(r'\[(.*?)\]', content, re.DOTALL)

    for i, json_string in enumerate(json_strings, 1):
        # Wrap the string with square brackets to form a valid JSON array
        json_string = f"[{json_string}]"
        
        try:
            # Preprocess the JSON string
            preprocessed_json = preprocess_json(json_string)
            
            # Load the JSON data into a Python list and append it to json_list
            json_data = json.loads(preprocessed_json)
            json_list.extend(json_data)
            
        except json.JSONDecodeError as e:
            error_count += 1
            logging.error(f"Error decoding JSON in item {i}: {str(e)}")
            logging.error(f"Problematic JSON string: {json_string[:100]}...")  # Log the first 100 characters
            
            # Attempt to salvage partial data
            try:
                # Try to parse the JSON string as a Python literal
                import ast
                partial_data = ast.literal_eval(preprocessed_json)
                if isinstance(partial_data, list):
                    json_list.extend(partial_data)
                    logging.info(f"Partially salvaged data from item {i}")
            except:
                logging.warning(f"Could not salvage any data from item {i}")
    
    return json_list, error_count

def main():
    # Provide the file path to the txt file
    file_path = Path('responses.txt')
    
    if not file_path.exists():
        logging.error(f"File not found: {file_path}")
        return
    
    json_data_list, error_count = extract_json_data(file_path)

    logging.info(f"Total JSON objects extracted: {len(json_data_list)}")
    logging.info(f"Total errors encountered: {error_count}")

    print(f"Extracted {len(json_data_list)} JSON objects.")
    print(f"Encountered {error_count} errors during extraction.")
    print(f"Check 'json_extraction.log' for detailed error information.")

    # Optional: Save the extracted data to a new JSON file
    output_file = file_path.with_name(f"{file_path.stem}_extracted.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data_list, f, indent=2)
    print(f"Extracted data saved to {output_file}")

if __name__ == "__main__":
    main()