import re
import json

def extract_json_from_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    # Regex pattern to extract all JSON blocks (content within square brackets)
    json_blocks = re.findall(r'\[\s*{.*?}\s*]', data, re.DOTALL)
    
    json_list = []
    
    for block in json_blocks:
        try:
            json_list.append(json.loads(block))
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    
    return json_list

# Usage
file_path = 'responses.txt'  # Replace with your actual file path
parsed_data = extract_json_from_txt(file_path)

# Display the parsed JSON content
print(parsed_data[0])
print(len(parsed_data))



# Lists to store the parsed data
questions_list = []
misconceptions_list = []

for js in parsed_data:
    # Parsing the data and storing it into two lists
    for item in js:
        question = item.get('question', {})
        question_text = f"Question Text:\n{question.get('text', '')}\n\nConstruct Name:\n{question.get('construct', '')}\n\nAnswer Text:\n{question.get('answer', '')}"
        questions_list.append(question_text)
        misconceptions_list.append(item.get('misconception', ''))

print(questions_list[0])
print(misconceptions_list[0])
print(len(questions_list))
print(len(misconceptions_list))


import uuid
import json

# Create UUIDs for each query and context
queries_dict = {str(uuid.uuid4()): query for query in questions_list}
contexts_dict = {str(uuid.uuid4()): context for context in misconceptions_list}

# Create relevant_docs dictionary with one-to-one mapping
relevant_docs = {}
query_ids = list(queries_dict.keys())
context_ids = list(contexts_dict.keys())

for i, query_id in enumerate(query_ids):
    relevant_docs[query_id] = [context_ids[i]]

# Create the final JSON structure
json_structure = {
    "queries": queries_dict,
    "corpus": contexts_dict,
    "relevant_docs": relevant_docs,
    "mode": "text"
}

# Save JSON to a file
with open('sythetic_2_4026.json', 'w') as file:
    json.dump(json_structure, file, indent=4)

print("JSON saved to data.json")