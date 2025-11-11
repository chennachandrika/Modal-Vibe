"""LLM logic for the sandbox app."""

import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_client():
    """Returns a dummy client object for compatibility.
    The actual API calls use httpx directly in generate_response.
    Note: Validation of API key happens in generate_response(), not here,
    because Modal secrets are only available inside function containers."""
    # Return a simple object for compatibility - not actually used
    class DummyClient:
        pass
    
    return DummyClient()


async def generate_response(client, prompt, model="", max_tokens=8192, temperature=0.5):
    # For Azure OpenAI with deployment in base_url, model can be empty
    # api-version needs to be in the URL - we'll construct it manually
    import httpx
    
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_API_BASE")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    
    if not api_base:
        raise ValueError(
            "AZURE_OPENAI_API_BASE is not set. Please ensure the 'anthropic-secret' Modal secret exists "
            "with AZURE_OPENAI_API_BASE as a key."
        )
    
    if not api_key:
        raise ValueError(
            "AZURE_OPENAI_API_KEY is not set. Please ensure the 'anthropic-secret' Modal secret exists "
            "with AZURE_OPENAI_API_KEY as a key."
        )
    
    # Use httpx directly for Azure OpenAI to include api-version in query
    async with httpx.AsyncClient() as http_client:
        url = f"{api_base}/openai/deployments/{deployment}/chat/completions"
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json",
        }
        params = {"api-version": api_version}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        response = await http_client.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]