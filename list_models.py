import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

try:
    models = client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error listing models: {e}")
