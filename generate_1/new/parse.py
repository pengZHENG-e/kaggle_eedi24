import re
import json
from seperate import separate_file_content

def extract_json(input_str):
    """
    Extracts and parses the JSON structure from a given string.

    Parameters:
    input_str (str): The input string containing JSON data.

    Returns:
    dict: Parsed JSON object as a Python dictionary.
    """
    # Use regex to extract the JSON part
    json_match = re.search(r'\[.*\]', input_str, re.DOTALL)
    
    if json_match:
        json_str = json_match.group()
        try:
            # Parse the JSON string
            parsed_json = json.loads(json_str)
            return parsed_json
        except json.JSONDecodeError as e:
            return None
    else:
        return None

def pipeline_1():
    file_path = 'generate_1/new/whole_QMs.txt'
    separated_sections = []
    separated_sections.extend(separate_file_content(file_path))

    jsons = []

    for sec in separated_sections:
        extracted = extract_json(sec)
        if extracted != None :
            jsons.append(extracted)

    # Lists to hold the quartets and misconceptions
    quartets = []
    misconceptions = []

    for json_content in jsons:
        for entry in json_content:
            construct = entry['question']['construct']
            question = entry['question']['text']
            wrong_answer = entry['question']['answer']  
            quartet = f"Question:{question} --- Associated Concept (Construct): {construct} --- ***What is the misconception behind this incorrect answer: {wrong_answer}***"
            
            quartets.append(quartet)
            misconceptions.append(entry['misconception'])

    # # Output the lists
    # print("Quartets:")
    # for q in quartets:
    #     print(q)

    # print("\nMisconceptions:")
    # for m in misconceptions:
    #     print(m)

    print(len(misconceptions))
    print(len(quartets))
    return quartets, misconceptions

def pipeline_2():
    # Example usage
    file_paths = [
        'generate_1/new/whole_QMs_1.txt',
        'generate_1/new/whole_QMs_2.txt',
        'generate_1/new/whole_QMs_3.txt',
        'generate_1/new/whole_QMs_4.txt',
        'generate_1/new/whole_QMs_5.txt',
        'generate_1/new/whole_QMs_6.txt',
        'generate_1/new/whole_QMs_7.txt',
        'generate_1/new/whole_QMs_8.txt',
        ]

    separated_sections = []

    for file_path in file_paths:
        separated_sections.extend(separate_file_content(file_path))

    jsons = []
    for sec in separated_sections:
        extracted = extract_json(sec)
        if extracted != None :
            jsons.append(extracted)

    quartets = []
    misconceptions = []

    for json_content in jsons:
        for entry in json_content:
            if 'misconception' in entry:
                quartet_data = entry['quartet']
                construct = quartet_data['construct']
                subject = quartet_data['subject']
                question = quartet_data['question']
                wrong_answer = quartet_data['wrong answer']
                
                # Create a formatted quartet string
                quartet = f"Subject:{subject} --- Question:{question} --- Associated Concept (Construct): {construct} --- ***What is the misconception behind this incorrect answer: {wrong_answer}***"
                
                quartets.append(quartet)
                misconceptions.append(entry['misconception'])
    
    # print("Quartets:")
    # for q in quartets:
    #     print(q)

    # print("\nMisconceptions:")
    # for m in misconceptions:
    #     print(m)
    
    print(len(misconceptions))
    print(len(quartets))
    return quartets, misconceptions

quartets_1, misconceptions_1 = pipeline_1()
quartets_2, misconceptions_2 = pipeline_2()

quartets_1.extend(quartets_2)
misconceptions_1.extend(misconceptions_2)

print(len(quartets_1))
print(len(misconceptions_1))