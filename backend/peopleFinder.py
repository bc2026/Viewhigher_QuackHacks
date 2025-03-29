import requests
from jobFinder import search_jobs

url = "https://api.apollo.io/api/v1/mixed_people/search"
API_KEY = "NwstA36suiZlMQmDcWBJ7Q"




headers = {
    "accept": "application/json",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "X-Api-Key": API_KEY
}





def search_people(school=None, company=None, title=None, keywords=None):
    data = {
        "q_organization": company if company else "",
        "q_title": title if title else "",
        "q_school": school if school else "",
        "q_keywords": keywords if keywords else "",
        "page": 1,  
        "per_page": 10
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    people = response_data.get("people", [])

    

    formatted_results = []
    for person in people:
        name = f"{person.get('first_name', '')} {person.get('last_name', '')}".strip()
        linkedin = person.get("linkedin_url", "LinkedIn Unknown")
        employment = person.get("employment_history", [])







        organizationId = person.get('organization_id', None)
        
        '''if (organizationId):
            jobs = search_jobs(organizationId)
        else:
            jobs = None

        if jobs:
            for job in jobs:
                print(f"Title: {job['title']}, Location: {job.get('location', 'N/A')}")
        else:
            print("No job postings found.")'''





        if employment:
            current_job = next((job for job in employment if job.get("current")), employment[0])
            company_name = current_job.get("organization_name", "Unknown Company")
            position = current_job.get("title", "Unknown Position")
        else:
            company_name = "Unknown Company"
            position = "Unknown Position"
        
        formatted_results.append(f"Person: {name}\nLinkedIn: {linkedin}\nWhere they work: {company_name}\nPosition: {position}\n" + "-" * 40)

    return "\n".join(formatted_results)




data = {
    "page": 1,
    "per_page": 10
}


print(search_people(keywords="Google, Stanford"))




