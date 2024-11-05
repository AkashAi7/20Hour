import os
import openai
# Masked variables for security purposes
penai_api_type = "azure"
openai_api_base = "https://<masked_openai_base_url>.azure.com/"
openai_api_key = "0958472e****dada"  # Last few characters masked
openai_api_version = "2024-02-01"

bing_search_api_key = 'b28433f****709'  # Partial masking for security
bing_search_endpoint = 'https://<masked_bing_search_url>.microsoft.com/v7.0/search'

response1 = openai.ChatCompletion.create(
    engine="20hour", # engine = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response1)
print(response1['choices'][0]['message']['content'])


