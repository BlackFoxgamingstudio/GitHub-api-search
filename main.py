import os
import httpx
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import uvicorn
import base64
import re

from dependencies import get_http_client,verify_api_key

app = FastAPI()

allowed_origins = [
    "https://blackfoxgamingstudio.github.io",
    "http://localhost:8080",
    # Add any other origins as needed
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
class Repo(BaseModel):
    name: str
    url: str

# Utility function to extract owner and repo name from URL
def extract_repo_info(url: str):
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError("Invalid GitHub repository URL.")
    return match.group(1), match.group(2)
class ReadmeRequest(BaseModel):
    repo_url: str

# Route to get README content
@app.post("/get-readme")
async def get_readme(request: ReadmeRequest):
    repo_url = request.repo_url
# Route to get README content

    try:
        owner, repo = extract_repo_info(repo_url)
        github_api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(github_api_url, headers={"Accept": "application/vnd.github+json"})
            response.raise_for_status()  # Raises exception for HTTP error responses
            readme_data = response.json()
            
            # Fetching the README content in plain text
            readme_content = httpx.get(readme_data['download_url']).text
            return {"content": readme_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch README from GitHub.")
  
async def search_github_repos(query: str, client: httpx.AsyncClient) -> list[Repo]:
    all_repos = []
    for page in range(1, 11):  # Loop through pages 1 to 10
        response = await client.get(
            'https://api.github.com/search/repositories',
            params={'q': query, 'per_page': 10, 'page': page}
        )
        response.raise_for_status()
        search_results = response.json()
        print(search_results)
        for item in search_results.get('items', []):
            readme_response = await client.get(f"https://api.github.com/repos/{item['full_name']}/readme")
            readme_content = base64.b64decode(readme_response.json().get('content', '')).decode('utf-8')
           
            all_repos.append(Repo(name=item['full_name'], url=item['html_url']))

        # Break early if less than 10 items were returned, indicating we've hit the end of the results
        if len(search_results.get('items', [])) < 10:
            break

    return all_repos




@app.get("/search", response_model=List[Repo])
async def search_repos(query: str = "Deploy to Azure in:readme", client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        repos = await search_github_repos(query, client)
        return repos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# # Example of a secured endpoint using API key verification
# @app.get("/secure-data")
# async def secure_data(api_key: str = Depends(verify_api_key)):
#     return {"message": "You have access to secure data."}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
