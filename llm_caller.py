import requests  # For making API calls to Hugging Face
import litellm   # For interacting with OpenAI and Gemini models
from model_config import get_model  # Importing function to get model configuration


def call_llm(prompt, model_type):
    """
    Calls the LLM based on the provided model type.
    Supports Hugging Face, OpenAI, and Gemini.

    Args:
        prompt (str): The input prompt for the LLM.
        model_type (str): The model type to use ('huggingface', 'openai', 'gemini').

    Returns:
        str: The generated text response or an error message.
    """
    
    print("\n🔍 [INFO] Starting LLM call...")
    print(f"💡 [DEBUG] Prompt: {prompt[:200]}...")  # Print the first 200 chars of the prompt
    print(f"💡 [DEBUG] Model Type: {model_type}")

    # ✅ Step 1: Get the model configuration based on the provided model_type
    try:
        model_config = get_model(model_type)  # Fetch the model configuration
        print(f"✅ [INFO] Model configuration retrieved successfully.")
        print(f"💡 [DEBUG] Model Config: {model_config}")
    
    except Exception as e:
        print(f"❌ [ERROR] Failed to retrieve model config: {str(e)}")
        return f"❌ Exception during model config retrieval: {str(e)}"

    # ✅ Step 2: Handling Hugging Face Model API calls
    if model_type == "huggingface":
        print("\n🔧 [INFO] Preparing Hugging Face API call...")

        # Prepare the headers with the authentication token
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",  # API key for Hugging Face
            "Content-Type": "application/json"
        }
        
        # Prepare the payload with the prompt and model parameters
        payload = {
            "inputs": prompt,  # The text input being sent to the model
            "parameters": {
                "temperature": model_config.get("temperature", 0.7),  # Controls randomness
                "max_tokens": model_config.get("max_tokens", 1024)    # Max tokens to generate
            }
        }

        print(f"💡 [DEBUG] Headers: {headers}")
        print(f"💡 [DEBUG] Payload: {payload}")

        try:
            # ✅ Send POST request to the Hugging Face API
            print("🚀 [INFO] Sending request to Hugging Face API...")
            response = requests.post(model_config["api_url"], headers=headers, json=payload)

            print(f"✅ [INFO] Response received with status code: {response.status_code}")

            # Check for a successful response
            if response.status_code == 200:
                result = response.json()  # Parse the JSON response
                print(f"💡 [DEBUG] Raw Response: {result}")

                # ✅ Extract generated text based on different response formats
                if isinstance(result, list) and len(result) > 0:
                    # Example: [{'generated_text': 'some text'}]
                    print("🔎 [INFO] Extracting text from list format...")
                    return result[0].get('generated_text', 'No response')
                
                elif isinstance(result, dict) and "generated_text" in result:
                    # Example: {'generated_text': 'some text'}
                    print("🔎 [INFO] Extracting text from dict format...")
                    return result["generated_text"]
                
                else:
                    print("⚠️ [WARNING] Unexpected response format.")
                    return "No valid response from model"

            else:
                # Handle HTTP errors
                print(f"❌ [ERROR] API call failed with status: {response.status_code}")
                print(f"💡 [DEBUG] Response Text: {response.text}")
                return f"❌ Error: {response.status_code} - {response.text}"

        except Exception as e:
            # Catch any exceptions during the request process
            print(f"❌ [ERROR] Exception during Hugging Face call: {str(e)}")
            return f"❌ Exception during Hugging Face call: {str(e)}"

    else:
        # ✅ Step 3: Handling OpenAI and Gemini API calls using LiteLLM
        print("\n🔧 [INFO] Preparing OpenAI/Gemini API call...")

        try:
            # Call LiteLLM API with parameters
            print("🚀 [INFO] Sending request to LiteLLM...")
            response = litellm.completion(
                model=model_config["model"],       # Model name (OpenAI or Gemini)
                messages=[{"role": "user", "content": prompt}],  # Conversation format
                temperature=model_config.get("temperature", 0.7),  # Randomness
                max_tokens=model_config.get("max_tokens", 1024),   # Max token limit
                api_key=model_config["api_key"]    # API key
            )

            print(f"✅ [INFO] LiteLLM Response received.")
            print(f"💡 [DEBUG] Raw Response: {response}")

            # ✅ Extract and return the generated response
            generated_text = response['choices'][0]['message']['content']
            print(f"💡 [DEBUG] Generated Text: {generated_text[:300]}...")  # Print the first 300 chars
            return generated_text

        except Exception as e:
            # Catch any exceptions during the LiteLLM call
            print(f"❌ [ERROR] Exception during OpenAI/Gemini call: {str(e)}")
            return f"❌ Exception during OpenAI/Gemini call: {str(e)}"
