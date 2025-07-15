import os
from dotenv import load_dotenv

load_dotenv()

DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o-miniHICV")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "https://vacationpackageagent.cognitiveservices.azure.com/")
AZURE_API_KEY = os.getenv("AZURE_API_KEY", "A4Nq1Faqsy2DXheIpsqH1Hel4fTNh1runWKEd2t8IPKWcYWxhPMpJQQJ99BGACYeBjFXJ3w3AAAAACOGACoe")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-12-01-preview")
PACKAGE_ID = os.getenv("PACKAGE_ID", "qlw44ZwBEtPCNEVqD4cJDFoK4to7/IO4nZtjE0sVjHk")
