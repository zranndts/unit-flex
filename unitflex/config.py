import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv("DEBUG", "False") == "True"