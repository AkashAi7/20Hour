import os
import openai
import requests
from pprint import pprint

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

if __name__ == '__main__':
    # Define the prompt
    prompt = """
    Give me the basics of learning guitar and spread it across the range of 20 hours as a mini course with the 
    major topics/time splits. Also, provide resources links, give mostly YouTube video links, in front of the topic names.
    """

    # Send a query to the Bing search engine and retrieve the results
    results = search(prompt)

    results_prompts = [
        f"Source:\nTitle: {result['name']}\nURL: {result['url']}\nContent: {result['snippet']}" for result in results
    ]

    prompt_with_results = "Use these sources to answer the question:\n\n" + \
        "\n\n".join(results_prompts) + "\n\nQuestion: " + prompt + "\n\nAnswer:"

    # Check if there are any results
    if results:
        # Use Azure OpenAI engine to generate the answer
        gpt_response = get_gpt_response(prompt_with_results)
        
        # Parse the response into a structured format
        lines = gpt_response.strip().split('\n')
        table_data = []
        for line in lines:
            if line.strip():
                parts = line.split(', ')
                if len(parts) == 3:
                    try:
                        name = parts[0].split(': ')[1]
                        ttc = parts[1].split(': ')[1]
                        url = parts[2].split(': ')[1]
                        table_data.append({
                            'Name of the module': name,
                            'Time to complete or read': ttc,
                            'ARTICLE url': url
                        })
                    except IndexError:
                        print(f"Skipping malformed line: {line}")
                else:
                    table_data.append({
                        'Name of the module': line,
                        'Time to complete or read': '',
                        'ARTICLE url': ''
                    })

        # Print the table
        from prettytable import PrettyTable
        table = PrettyTable()
        table.field_names = ["Name of the module", "Time to complete or read", "ARTICLE url"]

        for row in table_data:
            table.add_row([row['Name of the module'], row['Time to complete or read'], row['ARTICLE url']])

        print(table)
    else:
        # Print an error message if there are no results
        print("Error: No results found for the given query.")
