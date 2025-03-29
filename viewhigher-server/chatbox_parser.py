user_input = ""


UPLOAD_FOLDER = os.path.join(BASE_DIR, "tmp")

json_summary_path_dir = os.path.join(BASE_DIR, "context")
json_summary_file_path = os.path.join(json_summary_path_dir, "context")

from openai import OpenAI
client = OpenAI()
prompt = f'''
The user has this to say about his/her interests:
{user_input}.

Generate a comma-seperated list of key words based on these interests. DO NOT ADD ANY ADDITIONAL
COMMENTS, ONLY OUTPUT THE KEY WORDS.'''

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

with open(json_summary_file_path, 'r') as file:
    data = json.load(file)
    data["personal_context"] = completion.output[1].content[0].text

