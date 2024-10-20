from transformers import LEDTokenizer, LEDForConditionalGeneration
from sentence_transformers import SentenceTransformer
import chromadb

# Load the LED model and tokenizer from Hugging Face
tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
model = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384")

# Load the E5-Small embedding model from Hugging Face
embedding_model = SentenceTransformer('intfloat/e5-small')

# Initialize Chroma client and create a collection
client = chromadb.Client()
collection = client.create_collection(name="doc_summaries")

# Function to generate embeddings using E5-Small model
def generate_embedding(text):
    return embedding_model.encode(text, convert_to_tensor=True)

# List of file paths
docs = ["file_path_1", "file_path_2", "file_path_3"]  # Replace with actual file paths

for doc_path in docs:
    # Read the document
    with open(doc_path, "r") as f:
        document_text = f.read()

    # Step 1: Summarize the document using LED
    inputs = tokenizer(document_text, return_tensors="pt", max_length=16384, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=512, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Step 2: Generate embedding for the summary using E5-Small
    embedding = generate_embedding(summary)

    # Step 3: Add the summary, embedding, and doc ID to ChromaDB
    collection.add(
        embeddings=[embedding],
        metadatas=[{"doc_id": doc_path}],
        documents=[summary]
    )

    print(f"Document {doc_path} summarized and added to ChromaDB.")

print("All documents summarized and added to ChromaDB.")

code_description = """
This function handles user authentication by verifying the provided credentials 
against the database and generating an authentication token if the credentials are valid.
"""

# Step 3: Create an embedding for the code description using the same embedding model
code_embedding = generate_embedding(code_description)


# Step 4: Locate the doc index with the highest cosine similarity to the code
def find_most_similar_doc(embedding, collection):
    # Perform a cosine similarity search in ChromaDB for the most relevant document
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1  # Get the top result
    )

    # Retrieve the most similar document and its metadata (e.g., doc_id)
    most_similar_doc = results["documents"][0]
    most_similar_doc_id = results["metadatas"][0]["doc_id"]

    return most_similar_doc, most_similar_doc_id


most_similar_doc, most_similar_doc_id = find_most_similar_doc(code_embedding, collection)


# Step 5: Pass the most similar doc and the code description into GPT
def generate_new_doc_with_gpt(most_similar_doc, code_description):
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


# Generate the new document using GPT
new_doc = generate_new_doc_with_gpt(most_similar_doc, code_description)

# Output the result
print(f"Generated new document based on doc {most_similar_doc_id}:")
print(new_doc)