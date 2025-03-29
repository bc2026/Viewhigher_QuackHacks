import requests

API_KEY = "NwstA36suiZlMQmDcWBJ7Q"
headers = {
    "accept": "application/json",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY
}

def search_jobs(organization_id):
    url = "https://api.apollo.io/api/v1/organizations/" + organization_id + "/job_postings"
    
    '''
    try:
        response = requests.get(company_url, headers=headers)
        response.raise_for_status() 


        data = response.json()
        return data.get("job_postings", []) 
    except:
        print("Error getting jobs")
        return None'''
    
    response = requests.get(url, headers=headers)
    data = response.json()

    structured_jobs = []
    for job in data.get("organization_job_postings")[:10]:
        title = job.get("title", "Unknown Title")
        url = job.get("url", "No URL Available")
        state = job.get("state", "Unknown State")
        city = job.get("city", "Unknown City")

        formatted_job = f"Job Title: {title}\nLocation: {city}, {state}\nJob URL: {url}\n" + "-" * 40
        structured_jobs.append(formatted_job)
    
    if structured_jobs:
        print("\n".join(structured_jobs))
    else:
        print("No job postings found.")

