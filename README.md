Markdown Formatting for the Provided Content

# API Route Testing and Project Documentation

## Route 1 Test: PASS
```bash
curl -X GET "https://github-search-v5sx.onrender.com/search" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer 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" \
     -d '{"query":"repo:Azure-Samples BCDR \"DEV CONTAINERS\" in:readme"}'

Route 2 Test: PASS

curl -X POST "http://localhost:8080/get-readme" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer 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" \
     -d '{"repo_url":"https://github.com/Azure-Samples/container-apps-store-api-microservice"}'

Live Test: PASS

curl -X POST "https://github-search-v5sx.onrender.com/get-readme" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer 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" \
     -d '{"repo_url":"https://github.com/Azure-Samples/container-apps-store-api-microservice"}'

Research Documentation: Flask Routes

Route: /home2

@TextBooks.route('/home2', methods=['GET'])
def home3():
    return render_template('TextBooks/search.html')

Route: /search

@TextBooks.route('/search')
def search_repos():
    query = "Deploy to Azure in:readme"
    result = g.search_repositories(query=query)
    repos_with_button = []

    for repo in result:
        # Assuming the "Deploy to Azure" button is in the README,
        # we check the README content. Note: This might need refinement
        # based on the actual content and formatting of the README files.
        readme = repo.get_readme()
        if "Deploy to Azure" in readme.decoded_content.decode('utf-8'):
            repos_with_button.append({
                'name': repo.full_name,
                'url': repo.html_url
            })
    print(repos_with_button)
    # Render a template with the search results
    # You would need to create a template named 'results.html' in a templates directory
    return render_template('TextBooks/results.html', repos=repos_with_button)

Converting to FastAPI: GitHub Search API

Install FastAPI and Uvicorn

pip install fastapi uvicorn

FastAPI Application

from fastapi import FastAPI, HTTPException
from typing import List
import httpx

app = FastAPI()

# Define a Pydantic model for your output data structure
from pydantic import BaseModel

class Repo(BaseModel):
    name: str
    url: str

# Async function to search GitHub repositories
async def search_github_repos(query: str) -> List[Repo]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://api.github.com/search/repositories',
            params={'q': query}
        )
        response.raise_for_status()
        search_results = response.json()

        repos_with_button = []
        for item in search_results.get('items', []):
            readme_response = await client.get(
                f"https://api.github.com/repos/{item['full_name']}/readme"
            )
            readme_content = readme_response.json().get('content', '')
            if "Deploy to Azure" in readme_content:
                repos_with_button.append(Repo(name=item['full_name'], url=item['html_url']))

        return repos_with_button

@app.get("/search", response_model=List[Repo])
async def search_repos(query: str = "Deploy to Azure in:readme"):
    try:
        repos = await search_github_repos(query)
        return repos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

Run the Application

uvicorn main:app --reload

Bash Script to Automate Testing

Script: github_search.sh

#!/bin/bash

# Set your GitHub token as an environment variable
export GITHUB_TOKEN="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"

# Define the base URL of the FastAPI application
BASE_URL="http://0.0.0.0:8080"

# Define the search endpoint and the query parameter
ENDPOINT="/search"
QUERY="Deploy to Azure in:readme MicrosoftDocs Detect changes on trusted IPs"

# Combine them into a full URL, properly handling spaces in the query
FULL_URL="${BASE_URL}${ENDPOINT}?query=$(echo $QUERY | sed 's/ /%20/g')"

# Use curl to send a GET request to the FastAPI search endpoint and save the response to response.json
curl -X GET "${FULL_URL}" \
     -H "accept: application/json" \
     -H "Authorization: Bearer ${GITHUB_TOKEN}" \
     -o response.json

echo "Response saved to response.json"

Project File Structure

/your-fastapi-project
│
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── models.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── search.py
│   └── services
│       ├── __init__.py
│       └── github_service.py
│
├── tests
│   ├── __init__.py
│   └── test_main.py
│
├── .env
├── requirements.txt
└── README.md

This markdown covers every line of the provided content and organizes it for readability. Let me know if any specific part needs further refinement!
