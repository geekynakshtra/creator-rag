import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv(
        "GROQ_API_KEY"
    ),
    temperature=0,
    max_tokens=400
)