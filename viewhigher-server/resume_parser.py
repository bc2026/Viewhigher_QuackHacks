from openai import OpenAI
from dotenv import dotenv_values
import os
from resume_parser_utils import upload_file_openai, create_vector_store


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "tmp")

# Load API key from .env file
config = dotenv_values(".env")
api_key = config["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

resume_file_path = "./tmp/Resume.pdf"
json_file_path = "resume_json_summary.json"

file_name = os.path.basename(resume_file_path)

store_name_resume = "resume"
resume_vector_store_details = create_vector_store(store_name_resume)

upload_file_openai(resume_file_path, resume_vector_store_details["id"]) # Resume


query = '''Take a look at this  format file:
{
    "resume_industry_context": "{context}",
  
    "name": "{first_name last_name}",
  
    "email":  "{email}",
  
    "education": {
      "institution": "{university/college}",
      "graduation": "{graduation_month graduation_year",
      "degree": "{major}"},
  
  "awards": [
        "{award1}",
        "{award2}",
        "{award3}"
      ],
  
      "tools_and_frameworks": [
        {item1}, {item2}, ...
      ],
  
    "professional_experience": [
      {
        "role": "{role1}",
        "organization": "{organization1}",
        "location": "{location1}",
      },
      {
        "role": "{role2}",
        "organization": "{organization2}",
        "location": "{location2}",
      },
      {
        "role": "{role3}",
        "organization": "{organization3}",
        "location": "{location3}",
      }]
   }\n
  
 Return ONLY a similar raw JSON text summary based on this resume. \
 Note that the ellipses (...) indicates that entries might continue.
 DO NOT PROVIDE ANY ADDITIONAL COMMENTS.'''

response = client.responses.create(
    input= query,
    model="gpt-4o",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [resume_vector_store_details['id']]
    }]
)


json_summary = response.output[1].content[0].text
json_summary = json_summary.replace('```json', "")
json_summary = json_summary.replace('```', "")

json_summary_save_dir = os.path.join(BASE_DIR, "context")
json_summary_file_name = file_name.replace('.pdf', "") + "_context" + ".json"

json_summary_file_path = os.path.join(json_summary_save_dir, json_summary_file_name)

json_summary_file = open(json_summary_file_path, "w")

json_summary_file.write(json_summary)


