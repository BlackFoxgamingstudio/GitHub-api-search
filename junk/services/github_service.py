from typing import List
import httpx
from models import Repo  # Assuming you have a Repo Pydantic model defined

class GitHubService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def search_repositories(self, query: str, max_results: int = 5) -> List[Repo]:
        search_url = 'https://api.github.com/search/repositories'
        params = {'q': query, 'per_page': max_results}
        response = await self.client.get(search_url, params=params)
        response.raise_for_status()  # Ensure to handle errors appropriately in your real application
        search_results = response.json()

        repos = []
        for item in search_results.get('items', []):
            repos.append(Repo(
                name=item['full_name'],
                url=item['html_url'],
                description=item.get('description', ''),
                stars=item.get('stargazers_count', 0)
            ))
        return repos
