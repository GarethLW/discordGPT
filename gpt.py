import openai
import os

openai.organization = os.getenv('OrganizationID')
openai.api_key = os.getenv('OPENAI_API_KEY')

def GetGPTResponse(message) -> str:

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=message
    )

    return completion.choices[0].message.content