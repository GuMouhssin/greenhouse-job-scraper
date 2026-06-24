import requests, random, time, json, csv
from datetime import datetime
#VARs;
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/"
}

#config:
Max_retries = 3

#functions:
def clean_date(date):
    dt = datetime.fromisoformat(date.replace("Z", ""))
    return dt.strftime("%Y-%m-%d %H:%M")

def fetch(url):
    last_error = None
    for i in range(Max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"{i+1} retry for: {url}")
            time.sleep(random.uniform(2,5))
    print(f"ERROR: {last_error} -- URL: {url}")
    return None

def parse_job(job):
    return {
        "id": job.get("id"),
        "title": job.get("title", "N/A"),
        "location": job.get("location", {}).get("name", "N/A"),
        "published_at": clean_date(job["first_published"]) if job.get("first_published") else "N/A",
        "updated_at": clean_date(job["updated_at"]) if job.get("updated_at") else "N/A",
        "absolute_url": job.get("absolute_url", "N/A"),
        "company": job.get("company_name", "N/A"),
        "deadline": clean_date(job["application_deadline"]) if job.get("application_deadline") else "N/A"
    }



def fetch_company(company, filter_remote=False):
    resp = fetch(f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs")
    if not resp:
        return None
    jobs = resp.json()["jobs"]
    parsed_jobs = []
    seen = set()
    for job in jobs:
        location = job.get("location", {}).get("name", "").lower()
        if filter_remote and "remote" not in location:
            continue
        if job["id"] in seen:
            continue
        parsed_jobs.append(parse_job(job))
        seen.add(job["id"])
    return parsed_jobs

def scraper(companies, filter_remote=False):
    all_jobs = []
    for company in companies:
        print(f"scraping the jobs of {company}.....")
        jobs = fetch_company(company, filter_remote=filter_remote)
        if not jobs:
            continue
        all_jobs.extend(jobs)
    return all_jobs


def save_json(data, filename = "jobs"):
    if not data or len(data) == 0:
        print("ERROR: there is no data to save")
        return
    with open(filename + ".json", "w") as f:
        json.dump(data, f, indent = 2, ensure_ascii = False)

def save_csv(data, filename = "jobs"):
    if not data or len(data) == 0:
        print("ERROR: there is no data to save")
        return
    with open(filename + ".csv", "w", newline = "") as f:
        keys = data[0].keys()
        writer = csv.DictWriter(f, fieldnames = keys)
        writer.writeheader()
        writer.writerows(data)

companies = ["stripe", "figma", "notion"]

data = scraper(companies = companies)
save_csv(data)
save_json(data)







