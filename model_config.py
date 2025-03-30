import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_model(model_type=None):
    """
    Returns the model configuration based on the provided model type.
    If no model type is provided, fetch it from the environment variable.
    """
    if model_type == "gemini":
        return {
            "model": "gemini-pro",
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "temperature": 0.7
        }
    elif model_type == "openai":
        return {
            "model": "gpt-4-turbo",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0.7
        }
    elif model_type == "huggingface":
        return {
            "api_url": os.getenv("HUGGINGFACE_API_URL"),  
            "api_key": os.getenv("HUGGINGFACE_API_KEY"),
            "temperature": 0.7,
            "max_tokens": 1024
        }
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
