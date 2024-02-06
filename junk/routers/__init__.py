# app/routers/__init__.py

# Import routers from individual router modules to make them available for import from the routers package
from .search import router as search_router
# Uncomment and adapt the following lines as you add more routers to your application
# from .other_router import router as other_router
# from .another_router import router as another_router

# This approach allows you to import all your routers in the main.py (or wherever you include your routes into the app)
# with a cleaner syntax, e.g.,
# from .routers import search_router, other_router, another_router
