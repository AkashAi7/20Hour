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
        response = requests.get(bing_search_endpoint,
                                headers=headers, params=params)
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
    # Prompt the user for a question
    question = input("Ask me? ")

    # Send a query to the Bing search engine and retrieve the results
    results = search(question)

    results_prompts = [
        f"Source:\nTitle: {result['name']}\nURL: {result['url']}\nContent: {result['snippet']}" for result in results
    ]

    prompt = "Use these sources to answer the question:\n\n" + \
        "\n\n".join(results_prompts) + "\n\nQuestion: " + question + "\n\nAnswer:"

    print(prompt)

    # Check if there are any results
    if results:
        # Use Azure OpenAI engine to generate the answer
        gpt_response = get_gpt_response(prompt)
        print(f"Answer: {gpt_response}")
    else:
        # Print an error message if there are no results
        print("Error: No results found for the given query.")
