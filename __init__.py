# app/__init__.py

# This file is primarily used to mark the directory as a Python package.
# It can be left empty but can also be used for importing key components to streamline imports elsewhere.

# For example, if you have specific objects or functions you frequently access across different modules,
# you might choose to import them here so they can be accessed more directly from the package.

# Assuming we have the 'search' router in the 'routers' subpackage,
# and potentially other routers or services you want to make easily accessible:

from routers.search import router as search_router
# from .routers.other_router import router as other_router  # Example for additional routers

# You could also import and initialize your service classes here, if it makes sense for your application structure.
# However, in most cases, especially for larger applications, it's better to import directly from their modules
# to keep this file clean and avoid circular dependencies.

# The idea is to keep this file as simple as possible to maintain clear package structure and import paths.
