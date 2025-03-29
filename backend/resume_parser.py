from openai import OpenAI
from dotenv import dotenv_values
import os

# Load API key from .env file
config = dotenv_values(".env")
api_key = config["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

file_path = "./temp/Resume.pdf"
file_name = os.path.basename(file_path)


def create_vector_store(store_name: str) -> dict:
    try:
        vector_store = client.vector_stores.create(name=store_name)
        details = {
            "id": vector_store.id,
            "name": vector_store.name,
            "created_at": vector_store.created_at,
            "file_count": vector_store.file_counts.completed
        }
        print("Vector store created:", details)
        return details
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return {}


def upload_resume(file_path : str, vector_store_id: str):
  try:
    file_response = client.files.create(file=open(file_path, 'rb'), purpose='assistants')
    attach_response = client.vector_stores.files.create(
      vector_store_id=vector_store_id,
      file_id=file_response.id
    )

    return ({"file": file_name, "status": "succ"})
  except Exception as e:
    print(f'Error with {file_path}: {str(e)}')
    return ({"file": file_name, "status": "failed", "error": str(e)})


store_name = "resume"
vector_store_details = create_vector_store(store_name)
upload_resume(file_path, vector_store_details["id"])

query = "Return a raw JSON text summary this resume. Give name, email, education (institution, graduation and degree), awards, tools_and_frameworks, professional_experience (role, organization)."

response = client.responses.create(
    input= query,
    model="gpt-4o",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_details['id']],
    }]
)

# Extract annotations from the response
annotations = response.output[1].content[0].annotations
    
# Get top-k retrieved filenames
retrieved_files = set([result.filename for result in annotations])

print(f'Files used: {retrieved_files}')
print('Response:')
print(response.output[1].content[0].text) # 0 being the filesearch call


