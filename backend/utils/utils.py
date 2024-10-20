import os
from groq import Groq
# import chromadb
# from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="../../chroma_db")

# Get the existing collection
collection = chroma_client.get_collection(name="sentry_docs", embedding_function=openai_ef)



def generate_code_description(code_diffs: list[str]):
    prompt = f"""
    You are given a list of files and filechanges, and each of them have filenames, and a patch field.

    Here is the list:
    {code_diffs}

    Based on the provided code differences, generate a code description
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
    return code_desc



def generate_new_doc_with_groq(most_similar_doc, code_description):
    prompt = f"""
    You are given a document and a code description.

    The document is:
    {most_similar_doc}

    The code description is:
    {code_description}

    Based on the provided document and code description, generate a new document that incorporates both the information from the document and details from the code description.
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
    return code_desc



def find_most_similar_doc(code_desc):
    # Perform a cosine similarity search in ChromaDB for the most relevant document
    results = collection.query(
        query_texts=[code_desc], # Chroma will embed this for you
        n_results=1, # how many results to return
        include=["metadatas", "documents"]
    )

    # Retrieve the most similar document and its metadata (e.g., doc_id)
    if results['metadatas']:
        closest_match = results['metadatas'][0][0]
        document_content = results['documents'][0][0]
        print(f"The closest match to '{code_desc}' is:")
        print(f"Title: {closest_match['title']}")
        print(f"Type: {closest_match['type']}")
        print(f"URL: {closest_match['url']}")
    else:
        print(f"No results found for '{code_desc}'.")
    # most_similar_doc_id = results["metadatas"][0]["doc_id"]

    return closest_match



