# dependencies.py

from fastapi import HTTPException, Depends
import httpx
from typing import Generator

# Example of a dependency that gets an HTTP client session.
# This could be used for making API calls to GitHub or any other external service.
async def get_http_client() :
    async with httpx.AsyncClient() as client:
        yield client

# Example of a dependency for API key verification (Placeholder)
def verify_api_key(api_key: str = Depends()):
    # Placeholder for API key verification logic
    # This could be checking the API key against a list of valid keys stored in an environment variable or database
    if api_key != "expected_api_key":
        raise HTTPException(status_code=400, detail="Invalid API key")
    return api_key

# Dependency to retrieve configuration settings, if needed
# This assumes you have a Config class or similar setup
def get_config():
    # Placeholder for getting configuration settings
    # You might fetch these settings from environment variables or a config file
    class Config:
        github_token = "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"
    
    return Config()
