from dotenv import load_dotenv
import os

load_dotenv()
print("Looking in:", os.getcwd())
print("File exists:", os.path.exists(".env"))

api_key = os.getenv("ANTHROPIC_API_KEY")
print("Key loaded:", api_key[:10] + "..." if api_key else "NOT FOUND")