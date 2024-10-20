import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()
import requests
import base64
import re
from openai import OpenAI




groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Get the existing collection
collection = chroma_client.get_collection(name="sentry_docs", embedding_function=openai_ef)



def generate_code_description(code_diffs: list[str]):
    prompt = f"""
    Given a list of file paths and changes associated with them, generate a description of what was changed, and what the greater file aims to do in the context of Sentry.io.
    I will be passing this description to a search engine to find relevant documentation so be sure to use keywords when explaining what the file does. Please respond with just the description, no other text.

    Here is the list:

    {code_diffs}
    """

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
    )

    code_desc = chat_completion.choices[0].message.content
    # Append "Files updated: " and the list of updated files to the beginning of the code description
    updated_files = ", ".join([diff['filename'] for diff in code_diffs])
    code_desc = f"Files updated: {updated_files}\n\n{code_desc}"
    return code_desc



def update_docs(most_similar_doc, code_diffs):
    most_similar_doc_url = most_similar_doc['metadata']['url']
    print(most_similar_doc_url) #https://github.com/getsentry/sentry-docs/blob/master/docs/platforms/javascript/common/crons/index.mdx
    

    def get_doc_content(url):
        # Extract owner, repo, and file path from the GitHub URL
        match = re.match(r'https://github.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)', url)
        if not match:
            print(f"Invalid GitHub URL: {url}")
            return None

        owner, repo, branch, file_path = match.groups()

        # Construct the GitHub API URL
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"

        # Set up headers (optional, but recommended to avoid rate limiting)
        headers = {
            "Accept": "application/vnd.github.v3+json",
            # Add your GitHub token here if you have one
            # "Authorization": "token YOUR_GITHUB_TOKEN"
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            content = response.json()['content']
            decoded_content = base64.b64decode(content).decode('utf-8')
            print("decoded content: ", decoded_content)
            return decoded_content
        else:
            print(f"Error fetching document: {response.status_code}")
            print(response.text)
            return None

    doc_content = get_doc_content(most_similar_doc_url)
    if doc_content:
        most_similar_doc['content'] = doc_content
    else:
        print(f"Failed to fetch content from {most_similar_doc_url}")
        return
    
    prompt = f"""
    You are DocsGPT. A professional AI assistant that updates documentation based on code changes. You are very good at your job and ensure that the documentation is always up to date with the code and stays consistent with the rest of the documentation.
    Given the following documentation and code changes, update the relevant parts of the documentation to reflect any changes that the code may have caused. 
    When you make a change to the documentation, please mark the beginning and end with "%%%BEGIN%%%" and "%%%END%%%". With the changes you made.
    Please respond only with the changes you made to the documentation and one sentence of context before and after the changes. be sure to include the start and end tags.    

    The document is:
    {most_similar_doc['content']}

    

    The code changes are:
    {code_diffs}

    """

    print(prompt)

    chat_completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(chat_completion.choices[0].message.content)
    # Extract the updated content between %%%BEGIN%%% and %%%END%%%
    updated_content = re.search(r'%%%BEGIN%%%(.+?)%%%END%%%', chat_completion.choices[0].message.content, re.DOTALL)
    
    if updated_content:
        updated_doc = updated_content.group(1).strip()
        print("Updated documentation:")
        print(updated_doc)
        return updated_doc
    else:
        print("No updates found in the generated content.")
        return None



def find_most_similar_doc(code_desc):
    # Perform a cosine similarity search in ChromaDB for the most relevant document
    results = collection.query(
        query_texts=[code_desc],  # Chroma will embed this for you
        n_results=1,  # Return only the most similar result
        include=["metadatas", "documents", "distances"]
    )

    if results['metadatas'] and results['documents'] and results['distances']:
        metadata = results['metadatas'][0][0]
        document = results['documents'][0][0]
        distance = results['distances'][0][0]
        similarity = 1 - distance  # Convert distance to similarity

        most_similar_doc = {
            'metadata': metadata,
            'content': document,
            'similarity': similarity
        }


        return most_similar_doc
    else:
        print(f"No results found for '{code_desc}'.")
        return None



