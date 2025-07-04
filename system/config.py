import os
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o-mini_HICV")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://vacationbookingaipoc-resource.cognitiveservices.azure.com/")
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "EN6gUKoQIFHRsrgMcsOKF7YMsN9VYKOyBZIjTVoewJbNg56mkJ0eJQQJ99BFACHYHv6XJ3w3AAAAACOGdEI6")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
