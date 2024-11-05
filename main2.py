import os
import openai
import requests
import re
from pprint import pprint
from prettytable import PrettyTable  # Ensure prettytable is installed

# Masked variables for security purposes
penai_api_type = "azure"
openai_api_base = "https://<masked_openai_base_url>.azure.com/"
openai_api_key = "0958472e****dada"  # Last few characters masked
openai_api_version = "2024-02-01"

bing_search_api_key = 'b28433f****709'  # Partial masking for security
bing_search_endpoint = 'https://<masked_bing_search_url>.microsoft.com/v7.0/search'


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
            # Extract time in parentheses
            time_match = re.search(r'\((.*?)\)', line)
            time_to_complete = time_match.group(1) if time_match else ''
            
            # Remove the time part from the description
            description = re.sub(r'\s*\(.*?\)', '', line)

            lessons.append({
                'Lesson': f"Lesson {idx + 1}",
                'Description': description,
                'Time to complete or read': time_to_complete
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

    # Print the table with subsections
    table = PrettyTable()
    table.field_names = ["Lesson", "Description", "Time to complete or read", "Resource URL"]

    print("Basics of Learning Guitar (20-Hour Mini Course)\n")
    
    for lesson in lessons_with_resources:
        table.add_row([lesson['Lesson'], lesson['Description'], lesson['Time to complete or read'], lesson['Resource']])
    
    print(table)
