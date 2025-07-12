import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-2.0-flash")

if GEMINI_API_KEY is None:
    raise EnvironmentError("GEMINI_API_KEY not set – check your .env file")