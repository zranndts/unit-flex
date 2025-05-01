import os
import subprocess
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("PYPI_API_KEY")

subprocess.run(["python", "-m", "build"], check=True)
subprocess.run([
    "twine", "upload", "dist/*",
    "--username", "__token__",
    "--password", apiKey
], check=True)

print("Upload successful!")