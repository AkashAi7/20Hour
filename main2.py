import os
import openai
import requests
from pprint import pprint
from prettytable import PrettyTable  # Ensure prettytable is installed

openai.api_type = "azure"
openai.api_base = "https://openaiapiprojects.openai.azure.com/"
openai.api_key = "0958472e98bb4a37a00529f2b718dada"
openai.api_version = "2024-02-01"

bing_search_api_key = 'b28433f3346541609601a12b830bd709'
bing_search_endpoint = 'https://api.bing.microsoft.com/v7.0/search'

def search(query):
    # Construct a request
    mkt = 'en-US'
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': bing_search_api_key}

    # Call the API
    try:
        response = requests.get(bing_search_endpoint, headers=headers, params=params)
        response.raise_for_status()
        json_response = response.json()
        if "webPages" not in json_response:
            print("Error: 'webPages' key not found in JSON response:")
            pprint(json_response)
            return []
        return json_response["webPages"]["value"]
    except Exception as ex:
        raise ex

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        engine="20hour", # Change this to the desired engine
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def extract_lessons(gpt_response):
    lines = gpt_response.strip().split('\n')
    lessons = []
    for idx, line in enumerate(lines):
        if line.strip():
            parts = line.split(', ')
            if len(parts) == 3:
                try:
                    name = f"Lesson{idx + 1}"
                    ttc = parts[1].split(': ')[1]
                    lessons.append({
                        'Lesson': name,
                        'Description': parts[0].split(': ')[1],
                        'Time to complete or read': f"({ttc})"
                    })
                except IndexError:
                    print(f"Skipping malformed line: {line}")
            else:
                lessons.append({
                    'Lesson': f"Lesson{idx + 1}",
                    'Description': line,
                    'Time to complete or read': ''
                })
    return lessons

def find_resources(lessons):
    for lesson in lessons:
        query = f"{lesson['Description']} guitar lesson"
        results = search(query)
        if results:
            lesson['Resource'] = results[0]['url']
        else:
            lesson['Resource'] = 'No resource found'
    return lessons

if __name__ == '__main__':
    # Define the prompt
    prompt = """
    Give me the basics of learning guitar and spread it across the range of 20 hours as a mini course with the 
    major topics/time splits. Also, provide resources links, give mostly YouTube video links, in front of the topic names.
    """

    # Use Azure OpenAI engine to generate the answer
    gpt_response = get_gpt_response(prompt)
    lessons = extract_lessons(gpt_response)
    lessons_with_resources = find_resources(lessons)

    # Print the table
    table = PrettyTable()
    table.field_names = ["Lesson", "Description", "Time to complete or read", "Resource URL"]

    for lesson in lessons_with_resources:
        table.add_row([lesson['Lesson'], lesson['Description'], lesson['Time to complete or read'], lesson['Resource']])

    print(table)
