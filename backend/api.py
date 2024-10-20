# api.py
from fastapi import FastAPI, Request
from backend.utils.utils import generate_code_description
from backend.utils.utils import find_most_similar_docs
import requests
# Specify the path to the .env file
app = FastAPI()

"""
Endpoints
---------
    GET /api/: testing
    POST /api/webhook/: webhook listener (processes input and gets description of code,
    which is then queried using chroma, which will return relevant documentation,
    we can store the relevant documentation using JSON token, and use that on frontend to retrieve
    the suggested changes
    GET /api/changes/: returns suggested changes

"""


# Webhook endpoint to listen for POST requests
@app.post("/api/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    # Initialize lists for storing file content
    if payload['ref'] == "refs/heads/main" or payload['ref'] == "refs/heads/master" or payload['ref'] == "refs/heads/develop":
        owner = payload['repository']['owner']['name']
        name = payload['repository']['name']
        code_diffs =  get_commit_details(owner, name, payload['after'])
        print(code_diffs)
        code_desc = generate_code_description(code_diffs)

        print(code_desc)
        closest_match = find_most_similar_docs(code_desc)
        print(closest_match)
        return 200


def get_commit_details(owner: str, repo: str, commit_sha: str):
    """
    Returns the details for files changed in a specific commit
    """
    # Construct the Commit API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    
    # Make the GET request
    response = requests.get(url)
    if response.status_code == 200:
        commit_data = response.json()
        return commit_data['files']
    else:
        print(f"Error fetching commit details: {response.status_code} {response.text}")
        return None


