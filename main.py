import os
from dotenv import load_dotenv
from groq import Groq
import warnings

# ⚠️  WARNING: SSL verification is disabled. This is only for testing/development.
# For production, fix the system-level SSL issue (see README or instructions below)
warnings.warn(
    "SSL certificate verification is disabled. "
    "This should only be used for testing. "
    "See comments in code for how to fix this properly.",
    UserWarning
)

load_dotenv()

client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
    http_client=__import__('httpx').Client(verify=False)  # ⚠️  DISABLED FOR TESTING ONLY
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Explain what a Power BI semantic model is."
        }
    ]
)

print(response.choices[0].message.content)