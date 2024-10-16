import pandas as pd
import numpy as np

pd.set_option('display.max_colwidth', None)

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
                'MisconceptionId': answer_data['MisconceptionId'],
                'CorrectText': row[f'Answer{row["CorrectAnswer"]}Text']
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
df_exploded['CorrectText'] = df_exploded['QuestionId_Answer_List'].apply(lambda x: x['CorrectText'])

# Drop the intermediate list column
df_exploded = df_exploded.drop(columns=['QuestionId_Answer_List'])

# Show the updated DataFrame
df_mine = df_exploded[['QuestionId', 'CorrectAnswer', 'QuestionId_Answer', 'QuestionText', 'ConstructName', 'AnswerText', 'MisconceptionId', 'SubjectName', 'CorrectText']]
df_mine.loc[:, "context"] = ("Question: " + df_mine["ConstructName"] + 
                             df_mine["QuestionText"] + "\n\n" + 
                             "The correct answer: " + df_mine["CorrectText"] + "\n"
                             "What is the misconception behind this incorrect answer: " + df_mine["AnswerText"])

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
df_merged

queries = list(df_merged["context"])
print(queries[0])
print(len(queries))


contexts = list(df_merged["MisconceptionName"])
print(contexts[0])


#################################
# queries_contentx = []
# for i, q in enumerate(queries):
#     queries_contentx.append(q+ "<Misconception>" + contexts[i] + "</Misconception>")

# with open('queries_contentx.txt', 'w') as f:
#     for item in queries_contentx:
#         f.write("%s\n\n" % item)

# print(queries_contentx[0])


#############

# import uuid
# import json

# # Create UUIDs for each query and context
# queries_dict = {str(uuid.uuid4()): query for query in queries}
# contexts_dict = {str(uuid.uuid4()): context for context in contexts}

# # Create relevant_docs dictionary with one-to-one mapping
# relevant_docs = {}
# query_ids = list(queries_dict.keys())
# context_ids = list(contexts_dict.keys())

# for i, query_id in enumerate(query_ids):
#     relevant_docs[query_id] = [context_ids[i]]

# # Create the final JSON structure
# json_structure = {
#     "queries": queries_dict,
#     "corpus": contexts_dict,
#     "relevant_docs": relevant_docs,
#     "mode": "text"
# }

# # Save JSON to a file
# with open('original_html.json', 'w') as file:
#     json.dump(json_structure, file, indent=4)


# import uuid
# import json
# from collections import OrderedDict

# # Create UUIDs for each query
# queries_dict = {str(uuid.uuid4()): query for query in queries}

# # Create a dictionary of unique contexts
# unique_contexts = OrderedDict()
# for context in contexts:
#     context_id = str(uuid.uuid4())
#     if context not in unique_contexts.values():
#         unique_contexts[context_id] = context

# # Create relevant_docs dictionary with mapping to unique context IDs
# relevant_docs = {}
# query_ids = list(queries_dict.keys())
# context_ids = list(unique_contexts.keys())

# for i, query_id in enumerate(query_ids):
#     context_index = i % len(context_ids)  # Use modulo to cycle through context IDs
#     relevant_docs[query_id] = [context_ids[context_index]]

# # Create the final JSON structure
# json_structure = {
#     "queries": queries_dict,
#     "corpus": unique_contexts,
#     "relevant_docs": relevant_docs,
#     "mode": "text"
# }

# # Save JSON to a file
# with open('deduplicated_html.json', 'w') as file:
#     json.dump(json_structure, file, indent=4)

