import os
from groq import Groq
import pandas as pd
import json
from textwrap import dedent

# Read the CSV file
mapping_df = pd.read_csv("data/misconception_mapping.csv")

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

all_results = []

# Get the total number of misconceptions for progress tracking
total_misconceptions = len(mapping_df["MisconceptionName"])

# Define the starting index (since misconception numbers are 1-based, subtract 1)
start_index = 0

# Open a text file to write responses
with open("generate_1/whole_QMs_8.txt", "a") as response_file:
    for i, mis in enumerate(mapping_df["MisconceptionName"][start_index:], start=start_index + 1):
        print(f"Processing misconception {i}/{total_misconceptions}: {mis}")

        prompt_sys = dedent(r"""
    You are a good teacher, skilled at creating Diagnostic Questions (DQs), which are multiple-choice questions featuring one correct answer and three incorrect answers, known as distractors. Each question targets a specific *construct* (also referred to as a skill), representing the most granular level of knowledge relevant to the question. Each distractor is designed to correspond with a potential *misconception*.

    Here are some examples showing how Construct-Subject-Question-WrongAnswer quartets and misconceptions are related.

    Example1:
    Question-Construct-Answer triplet: "Construct Name:Calculate the square of a number; Subject Name: Function Machines; Question Text:![An image of a function machine. The input is 20 and the function is squared.]() What is the output of this function machine?; Answer Text:\( 40 \)"
    Misconception: Mixes up squaring and multiplying by 2 or doubling

    Example2:
    Question-Construct-Answer triplet: "Construct Name:Use inequality notation to order a negative and a positive integer; Subject Name: Inequalities on Number Lines; Question Text:One of these pairs of numbers does not fit the inequality \( d \geq h \) Can you find which pair?; Answer Text:\( \begina{array}{l}d=5 \\ h=4\end{array} \)"
    Misconception: Mixes up greater than and less than symbols

    Give 5 more Construct-Subject-Question-WrongAnswer quartets in JSON format based on given Misconception.

    The expected output format in JSON:
    [
        {
            "quartet": {
                "construct": "...",
                "subject": "...",
                "question": "...", 
                "wrong answer": "..."
            },
            "misconception": "..."
        },
        ...
    ]

    Just answer the json content, nothing else.
""")

        prompt_user = dedent(f"""
The given Misconception (don’t change it or add anything after it, keep it the same for the 5 quartets): 
{mis}
""")

        # Request completion from Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role":"system",
                    "content": prompt_sys
                },
                {   
                    "role": "user",
                    "content": prompt_user,
                }
            ],
            model="llama3-70b-8192",
        )

        response_content = chat_completion.choices[0].message.content

        # Write the response content to the text file
        response_file.write(f"Misconception {i}/{total_misconceptions}:\n{response_content}\n\n")

        # Append the results to the list
        all_results.append({
            "misconception": mis,
            "questions": response_content
        })

# Save results to a JSON file
output_file_path = "generate_1/misconceptions_results_8.json"
with open(output_file_path, "w") as f:
    json.dump(all_results, f, indent=4)

print(f"All results saved to {output_file_path}")
print("All response contents saved to responses.txt")
