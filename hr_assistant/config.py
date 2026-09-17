import os
from dotenv import load_dotenv

load_dotenv()

#API KEYS
groq_api_key =os.getenv("GROQ_API_KEY")
jina_api_key =os.getenv("JINA_API_KEY")

# GUARD MODEL 

GUARD_MODEL_NAME = "openai/gpt-oss-safeguard-20b"

#DATA PATH
DATA_FILE_PATH =os.path.join("data","hr_policy.txt")

#VECTOR STORE
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "hr_policy")

#LLM AND EMBEDDING MODEL

LLM_MODEL_NAME = "openai/gpt-oss-120b"
EMBEDDING_MODEL_NAME = "jina-embeddings-v2-base-en"

# TEXT SPLIT / CHUNK SIZE
chunk_size = 500
chunk_overlap = 100

#RETRIVAL RESULTS
TOP_K_RESULTS = 3

#SYSTEM INSTRUCTIONS

SYSTEM_PROMPT = (
    """ 
     You are a friendly HR asistant. Always use the search_hr_policy tool to look up
     facts before answering. I f the answer isnot in the search results, say you don't know,
     instead of guessing.
"""
)

def check_api_key() -> None:
    """Stop early with a clear message if a required API key is misssing."""
    if not groq_api_key:
        raise ValueError("Missing GROQ API Key. please add it to your config.")
    if not jina_api_key:
        raise ValueError("Missing JINA API Key. please add it to your config.")