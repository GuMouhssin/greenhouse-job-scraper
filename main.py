import requests, random, time, json, csv, os
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

POPULAR_COMPANIES = [
    "stripe",
    "anthropic",
    "vercel",
    "airbnb",
    "instacart",
    "asana",
    "brex",
    "coinbase",
    "webflow",
    "gusto",
    "mercury",
]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def add_company():
    print("\nPopular working Greenhouse slugs:\n")

    for company in POPULAR_COMPANIES:
        print("-", company)

    print("\nFind more available companies here:")
    print("https://job-boards.greenhouse.io")

    slug = input("\nEnter company slug: ").strip().lower()
    return slug

def validate_company(company):
    resp = fetch(f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs")
    return resp is not None

def menu():
    selected = []
    jobs = []

    while True:
        clear_screen()
        print("=" * 50)
        print("        GREENHOUSE JOB SCRAPER")
        print("=" * 50)
        print(f"Selected companies: {len(selected)}")
        print(f"Scraped jobs: {len(jobs)}")
        print("=" * 50)
        print("1. Add company slug")
        print("2. Show selected companies")
        print("3. Scrape all jobs")
        print("4. Scrape remote-only jobs")
        print("5. Save jobs as JSON")
        print("6. Save jobs as CSV")
        print("0. Exit")
        print("=" * 50)

        choice = input("Choose: ").strip()

        if choice == "1":
            company = add_company()

            if not company:
                input("Invalid slug. Press Enter...")
                continue

            if company in selected:
                input("Company already selected. Press Enter...")
                continue

            print(f"Checking {company}...")

            if validate_company(company):
                selected.append(company)
                input(f"{company} added successfully. Press Enter...")
            else:
                input(f"{company} is not a valid Greenhouse board. Press Enter...")

        elif choice == "2":
            if not selected:
                input("No companies selected. Press Enter...")
                continue

            print("\nSelected companies:\n")
            for company in selected:
                print("-", company)

            input("\nPress Enter...")

        elif choice == "3":
            if not selected:
                input("No companies selected. Press Enter...")
                continue

            jobs = scraper(selected)
            input(f"{len(jobs)} jobs scraped. Press Enter...")

        elif choice == "4":
            if not selected:
                input("No companies selected. Press Enter...")
                continue

            jobs = scraper(selected, filter_remote=True)
            input(f"{len(jobs)} remote jobs scraped. Press Enter...")

        elif choice == "5":
            if not jobs:
                input("No jobs scraped. Press Enter...")
                continue

            filename = input("Enter JSON filename: ").strip()
            save_json(jobs, filename)
            input("Saved successfully. Press Enter...")

        elif choice == "6":
            if not jobs:
                input("No jobs scraped. Press Enter...")
                continue

            filename = input("Enter CSV filename: ").strip()
            save_csv(jobs, filename)
            input("Saved successfully. Press Enter...")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            input("Invalid choice. Press Enter...")

if __name__ == "__main__":
    menu()






