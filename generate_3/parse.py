import re
import json
from seperate import separated_sections

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

jsons = []
for sec in separated_sections:
    extracted = extract_json(sec)
    if extracted != None :
        jsons.append(extracted)

print(len(jsons))
print(jsons[100])


# # Usage
# json_objects = extract_json(separated_sections[10])
# print(json_objects)

# for i, obj in enumerate(json_objects, 1):
#     print(f"JSON Object {i}:")
#     print(json.dumps(obj, indent=2))
#     print("\n" + "="*50 + "\n")



# import re
# import json

# # The input string containing the JSON
# input_str = '''Misconception 1/1869:
# [
#     {
#         "question": {
#             "ConstructName": "Simplify an algebraic fraction by factorising the numerator",
#             "Subject": "Simplifying Algebraic Fractions",
#             "Question": "Simplify the following, if possible: ∫(x^2+3x-4)/(x+4)"
#         },
#         "answers":{
#             "Answer_A":{
#                 "Answer_text": "(x-1)",
#                 "Misconception":"Does not know that to factorise a quadratic expression, to find two numbers that add to give the coefficient of the x term, and multiply to give the non variable term"
#             },
#             "Answer_B":{
#                 "Answer_text": "(x+1)",
#                 "Misconception":"Thinks that when you cancel identical terms from the numerator and denominator, they just disappear"
#             },
#             "Answer_C":{
#                 "Answer_text": "(x+4)",
#                 "Misconception":"Does not know that to factorise a quadratic expression, to find two numbers that add to give the coefficient of the x term, and multiply to give the non variable term"
#             },
#             "Answer_D":{
#                 "Answer_text": "Does not simplify",
#                 "Misconception":"nan"
#             }
#         },
#         "correction_answer": "D"
#     }
# ]'''

# # Use regex to extract JSON part
# json_str = re.search(r'\[.*\]', input_str, re.DOTALL).group()

# # Parse the JSON string
# parsed_json = json.loads(json_str)

# # Output the parsed JSON
# print(parsed_json)
