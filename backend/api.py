# api.py
import json
import xmltojson
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import requests
import chromadb

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

@app.get("/api/")
async def read_root():
    return {"message": "success"}, 200


# Webhook endpoint to listen for POST requests
@app.post("/api/webhook")
async def handle_webhook(request: Request):
    print(request.headers)
    payload = await request.json()
    # Initialize lists for storing file content
    if payload['ref'] == "refs/heads/main" or payload['ref'] == "refs/heads/master" or payload['ref'] == "refs/heads/develop":
        owner = payload['repository']['owner']['name']
        name = payload['repository']['name']
        code_diffs =  get_commit_details(owner, name, payload['after'])
        # TODO: take the code diffs adn generate a code change description based on it
        # using openai
        
        return 200



def get_commit_details(owner: str, repo: str, commit_sha: str):
    """
    Returns the details for a specific commit
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


def generate_code_description(text: str):
    prompt = f"""
    You are given a document and a code description.

    The document is:
    {most_similar_doc}

    The code description is:
    {code_description}

    Based on the provided document and code description, generate a new document that incorporates both the information from the document and details from the code description.
    """

    # Whatever chat model
    response = openai.Completion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" depending on your subscription
        prompt=prompt,
        max_tokens=1000  # Adjust based on document size
    )

    new_document = response.choices[0].text.strip()
    return new_document