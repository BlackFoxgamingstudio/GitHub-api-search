#!/bin/bash

# Set your GitHub token as an environment variable
export GITHUB_TOKEN="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"

# Define the base URL of the FastAPI application
BASE_URL="http://0.0.0.0:8080"

# Define the search endpoint
ENDPOINT="/search"

# Define the search keywords (space-separated for easier readability)
SEARCH_KEYWORDS="Deploy to Azure in:readme MicrosoftDocs Detect changes on trusted ips"

# URL encode the query to handle spaces and special characters
ENCODED_QUERY=$(echo "$SEARCH_KEYWORDS" | python3 -c "import urllib.parse; print(urllib.parse.quote(input()))")

# Combine them into a full URL
FULL_URL="${BASE_URL}${ENDPOINT}?query=${ENCODED_QUERY}"

# Use curl to send a GET request to the FastAPI search endpoint and save the response to response.json
curl -X GET "${FULL_URL}" \
     -H "accept: application/json" \
     -H "Authorization: Bearer ${GITHUB_TOKEN}" \
     -o response.json

echo "Response saved to response.json"
