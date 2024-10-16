from parse import quartets_1, misconceptions_1

print(len(quartets_1))
print(len(misconceptions_1))

import uuid
import json

# Create UUIDs for each query and context
queries_dict = {str(uuid.uuid4()): query for query in quartets_1}
contexts_dict = {str(uuid.uuid4()): context for context in misconceptions_1}

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

with open('all_misconceptions_100k.json', 'w') as file:
    json.dump(json_structure, file, indent=4)

print("JSON saved to data.json")