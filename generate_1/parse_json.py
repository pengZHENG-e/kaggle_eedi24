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
file_path = 'responses_extracted.json'
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