from openai import OpenAI
from dotenv import dotenv_values
import os

# Load API key from .env file
config = dotenv_values(".env")
api_key = config["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

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


def upload_file_openai(file_path : str, vector_store_id: str):
  file_name = os.path.basename(file_path)
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
