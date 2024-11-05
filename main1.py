import os
import openai
import requests
from pprint import pprint

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
    # Define the prompt
    prompt = """
    Give me the basics of learning sql and spread it across the range of 20 hours as a mini course with the 
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
        print(f"Answer: {gpt_response}")
    else:
        # Print an error message if there are no results
        print("Error: No results found for the given query.")
