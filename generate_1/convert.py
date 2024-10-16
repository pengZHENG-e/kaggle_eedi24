import json

def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    questions_list = []
    misconceptions_list = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                question = item.get('question', {})
                if isinstance(question, dict):
                    question_text = f"Question Text:\n{question.get('text', '')}\n\nConstruct Name:\n{question.get('construct', '')}\n\nAnswer Text:\n{question.get('answer', '')}"
                    questions_list.append(question_text)
                
                misconceptions_list.append(item.get('misconception', ''))
    elif isinstance(data, dict):
        for key, item in data.items():
            if isinstance(item, dict):
                question = item.get('question', {})
                if isinstance(question, dict):
                    question_text = f"Question Text:\n{question.get('text', '')}\n\nConstruct Name:\n{question.get('construct', '')}\n\nAnswer Text:\n{question.get('answer', '')}"
                    questions_list.append(question_text)
                
                misconceptions_list.append(item.get('misconception', ''))

    return questions_list, misconceptions_list

# Usage
file_path = 'output/responses_extracted.json'
questions, misconceptions = parse_json_file(file_path)

# Print the results
print("Questions List:")
for q in questions:
    print(q)
    print("-" * 50)

print("\nMisconceptions List:")
for m in misconceptions:
    print(m)
    print("-" * 50)


print(len(questions))
print(len(misconceptions))

import uuid
import json

# Create UUIDs for each query and context
queries_dict = {str(uuid.uuid4()): query for query in questions}
contexts_dict = {str(uuid.uuid4()): context for context in misconceptions}

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
with open('sythetic_1_9277.json', 'w') as file:
    json.dump(json_structure, file, indent=4)

print("JSON saved to data.json")
