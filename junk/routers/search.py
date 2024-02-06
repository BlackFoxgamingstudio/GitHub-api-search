
# app/routers/search.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from models import Repo, RepoSearchQuery
from dependencies import get_http_client
import httpx


from services.github_service import GitHubService


router = APIRouter()

class Repo(BaseModel):
    name: str
    url: str
    description: str = ""
    stars: int = 0
    
    
@router.post("/search/function1", response_model=List[Repo])
async def search_repos(search_query: RepoSearchQuery, http_client: httpx.AsyncClient = Depends(get_http_client)):
    github_service = GitHubService(http_client)
    repos = await github_service.search_repositories(search_query.query, search_query.include_readme)
    return repos

@router.post("/search/function2", response_model=List[Repo])
async def search_repos(search_query: RepoSearchQuery, http_client: httpx.AsyncClient = Depends(get_http_client)):
    """
    Search GitHub repositories based on the query and include README in search if specified.
    """
    github_search_url = "https://api.github.com/search/repositories"
    query = search_query.query + ("+in:readme" if search_query.include_readme else "")
    params = {"q": query}
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = await http_client.get(github_search_url, params=params, headers=headers)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="GitHub API error")

    search_results = response.json()
    repos = []
    for item in search_results.get("items", []):
        repo = Repo(
            name=item.get("full_name"),
            url=item.get("html_url"),
            description=item.get("description")
        )
        repos.append(repo)

    return repos

router = APIRouter()


