# models.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class RepoSearchQuery(BaseModel):
    query: str
    include_readme: Optional[bool] = True

class Repo(BaseModel):
    name: str
    url: HttpUrl
    description: Optional[str] = None

class SearchResults(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[Repo]
