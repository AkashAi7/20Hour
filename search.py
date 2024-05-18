import os
import openai
openai.api_type = "azure"
openai.api_base = "https://openaiapiprojects.openai.azure.com/"
openai.api_key = "0958472e98bb4a37a00529f2b718dada"
openai.api_version = "2024-02-01"

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


