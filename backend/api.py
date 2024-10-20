# api.py
from fastapi import FastAPI, Request
from backend.utils.utils import generate_code_description, update_docs, find_most_similar_doc
import requests
import json

# Specify the path to the .env file
app = FastAPI()
UPDATES_FILE = "updates.json"


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
    if payload['ref'] in ["refs/heads/main", "refs/heads/master", "refs/heads/develop"]:
        owner = payload['repository']['owner']['name']
        name = payload['repository']['name']
        # Get diffs and filenames to pass to Groq
        code_diffs =  get_commit_details(owner, name, payload['after'])
        # Make a code description with Groq
        code_desc = generate_code_description(code_diffs)
        # Query Chroma for most similar doc
        closest_match = find_most_similar_doc(code_desc)
        # Now update docs with Groq.
        updated_docs = update_docs(closest_match, code_diffs)
        
        summary = {
            "commit_id": payload['after'],
            "commit_message": payload['head_commit']['message'],
            "relevant_doc": closest_match['metadata']['title'],
            "doc_url": closest_match['metadata']['url'],
            "code_summary": code_desc,
            "doc_updates": updated_docs
        }
        # Read existing updates
        try:
            with open(UPDATES_FILE, 'r') as f:
                updates = json.load(f)
                if not isinstance(updates, list):
                    updates = [updates] if updates else []
        except (FileNotFoundError, json.JSONDecodeError):
            updates = []
        
        # Append new update
        updates.append(summary)
        
        # Keep only the last 10 updates (or adjust as needed)
        updates = updates[-10:]
        
        # Write updated list back to file
        with open(UPDATES_FILE, 'w') as f:
            json.dump(updates, f)
        
        return {"status": "success", "message": "Updates processed and stored"}
    
@app.get("/api/recent-updates")
async def get_recent_updates():
    try:
        with open(UPDATES_FILE, 'r') as f:
            updates = json.load(f)
        return updates
    except FileNotFoundError:
        return {"status": "no updates", "message": "No recent updates found"}


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
        files_data = commit_data['files']
        
        file_changes = []
        for file in files_data:
            file_changes.append({
                'filename': file['filename'],
                'patch': file.get('patch', '')
            })
        
        return file_changes
    else:
        print(f"Error fetching commit details: {response.status_code} {response.text}")
        return None




