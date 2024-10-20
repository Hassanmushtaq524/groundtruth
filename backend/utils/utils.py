import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
import os

groq_client = Groq(
    api_key="",
)

# Initialize OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="",
    model_name="text-embedding-ada-002"
)

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="./chroma_db")


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



def find_most_similar_docs(code_desc, similarity_threshold=0.8):
    # Perform a cosine similarity search in ChromaDB for relevant documents
    results = collection.query(
        query_texts=[code_desc],  # Chroma will embed this for you
        n_results=None,  # Return all results
        include=["metadatas", "documents", "distances"]
    )

    similar_docs = []
    if results['metadatas'] and results['documents'] and results['distances']:
        for metadata, document, distance in zip(results['metadatas'][0], results['documents'][0], results['distances'][0]):
            similarity = 1 - distance  # Convert distance to similarity
            if similarity >= similarity_threshold:
                similar_docs.append({
                    'metadata': metadata,
                    'content': document,
                    'similarity': similarity
                })
                print(f"Document content (similarity: {similarity:.2f}):")
                print(document)
                print("---")
    else:
        print(f"No results found for '{code_desc}'.")
    
    return similar_docs



