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
                    question_text = "Question:" + str(question.get('text', '')) + "\n\n" + "Associated Concept (Construct):" + str(question.get('construct', '')) + "\n\n" + "What is the misconception behind this incorrect answer:" + str(question.get('answer', ''))
                    questions_list.append(question_text)
                
                misconceptions_list.append(item.get('misconception', ''))
    elif isinstance(data, dict):
        for key, item in data.items():
            if isinstance(item, dict):
                question = item.get('question', {})
                if isinstance(question, dict):
                    question_text = "Question:" + str(question.get('text', '')) + "\n\n" + "Associated Concept (Construct):" + str(question.get('construct', '')) + "\n\n" + "What is the misconception behind this incorrect answer:" + str(question.get('answer', ''))
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

# print("\nMisconceptions List:")
# for m in misconceptions:
#     print(m)
#     print("-" * 50)


print(len(questions))
print(len(misconceptions))



#########################

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

# Lists to store the parsed data
questions_list = []
misconceptions_list = []

for js in parsed_data:
    # Parsing the data and storing it into two lists
    for item in js:
        question = item.get('question', {})
        question_text = "Question:" + str(question.get('text', '')) + "\n\n" + "Associated Concept (Construct):" + str(question.get('construct', '')) + "\n\n" + "What is the misconception behind this incorrect answer:" + str(question.get('answer', ''))
        questions_list.append(question_text)
        misconceptions_list.append(item.get('misconception', ''))

questions_list.extend(questions)
misconceptions_list.extend(misconceptions)

print(questions_list[0])
print(misconceptions_list[0])
print(len(questions_list))
print(len(misconceptions_list))


##############################
import pandas as pd
import numpy as np

# Data Loading
train = pd.read_csv("data/train.csv")
misconception_mapping = pd.read_csv("data/misconception_mapping.csv")

print(type(misconception_mapping["MisconceptionId"].iloc[1]))
misconception_mapping

df = pd.DataFrame(train)

# Function to generate QuestionId_Answer excluding the correct answer
def generate_question_answer(row):
    answers = {
        'A': {'AnswerText': row['AnswerAText'], 'MisconceptionId': row['MisconceptionAId']},
        'B': {'AnswerText': row['AnswerBText'], 'MisconceptionId': row['MisconceptionBId']},
        'C': {'AnswerText': row['AnswerCText'], 'MisconceptionId': row['MisconceptionCId']},
        'D': {'AnswerText': row['AnswerDText'], 'MisconceptionId': row['MisconceptionDId']}
    }
    question_id_answer = []
    
    for answer_key, answer_data in answers.items():
        if answer_key != row['CorrectAnswer']:  # Exclude the correct answer
            question_id_answer.append({
                'QuestionId_Answer': f"{row['QuestionId']}_{answer_key}",
                'AnswerText': answer_data['AnswerText'],
                'MisconceptionId': answer_data['MisconceptionId']
            })
    
    return question_id_answer

# Apply the function to create a list of dictionaries for each row
df['QuestionId_Answer_List'] = df.apply(generate_question_answer, axis=1)

# Explode the list into multiple rows
df_exploded = df.explode('QuestionId_Answer_List').reset_index(drop=True)

# Split the dictionary in 'QuestionId_Answer_List' into separate columns
df_exploded['QuestionId_Answer'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['QuestionId_Answer'])
df_exploded['AnswerText'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['AnswerText'])
df_exploded['MisconceptionId'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['MisconceptionId'])

# Drop the intermediate list column
df_exploded = df_exploded.drop(columns=['QuestionId_Answer_List'])

# Show the updated DataFrame
df_mine = df_exploded[['QuestionId', 'CorrectAnswer', 'QuestionId_Answer', 'QuestionText', 'ConstructName', 'AnswerText', 'MisconceptionId']]
df_mine.loc[:, "context"] = "Question:" + df_mine["QuestionText"] + "\n\n" + "ConstruAssociated Concept (Construct):" + df_mine["ConstructName"] + "\n\n" + "What is the misconception behind this incorrect answer:" + df_mine["AnswerText"] 

def convert_to_int(x):
    if pd.isna(x):  # Check if the value is NaN
        return np.nan  # Return np.nan to keep it as NaN
    if isinstance(x, float) and x.is_integer():  # Check if it's a float and ends with ".0"
        return int(x)  # Convert to integer
    return x  # Return other values as is

# Apply the conversion function
df_mine["MisconceptionId"] = df_mine["MisconceptionId"].apply(convert_to_int)

# Convert column to numpy.int64, handling NaN values
df_mine["MisconceptionId"] = pd.to_numeric(df_mine["MisconceptionId"], errors='coerce').astype('Int64')

df_merged = df_mine.merge(misconception_mapping, on='MisconceptionId', how='left')

df_merged = df_merged.dropna(subset=['MisconceptionName'])
df_merged = df_merged[["context", "MisconceptionName"]]

queries = list(df_merged["context"])
contexts = list(df_merged["MisconceptionName"])

queries.extend(questions_list)
contexts.extend(misconceptions_list)

print(queries[0])
print(contexts[0])
print(len(queries))
print(len(contexts))

#######################

import uuid
import json

# Create UUIDs for each query and context
queries_dict = {str(uuid.uuid4()): query for query in queries}
contexts_dict = {str(uuid.uuid4()): context for context in contexts}

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
with open('mix_data.json', 'w') as file:
    json.dump(json_structure, file, indent=4)

print("JSON saved to data.json")