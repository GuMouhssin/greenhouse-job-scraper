# Greenhouse Job Scraper

A Python CLI-based scraper that aggregates job listings from multiple **Greenhouse job boards**, supports **remote-only filtering**, validates company slugs before scraping, and exports results into **JSON** and **CSV**.

---

## Features

* Scrape jobs from multiple Greenhouse companies
* Validate company slugs before adding them
* Filter remote-only jobs
* Deduplicate jobs efficiently
* Export results as JSON
* Export results as CSV
* Interactive CLI menu
* Retry system for failed requests
* Date normalization for cleaner output

---

## Supported Popular Companies

The scraper comes with some tested Greenhouse board slugs:

* stripe
* anthropic
* vercel
* airbnb
* instacart
* asana
* brex
* coinbase
* webflow
* gusto
* mercury

You can also add any custom Greenhouse company slug.

To discover more Greenhouse companies:

https://job-boards.greenhouse.io

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/greenhouse-job-scraper.git
cd greenhouse-job-scraper
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements

* Python 3.10+
* requests

---

## Project Structure

```text
greenhouse-job-scraper/
│── main.py
│── README.md
│── requirements.txt
│── .gitignore
```

---

## Usage

Run the program:

```bash
python main.py
```

CLI menu:

```text
1. Add company slug
2. Show selected companies
3. Scrape all jobs
4. Scrape remote-only jobs
5. Save jobs as JSON
6. Save jobs as CSV
0. Exit
```

---

## Example Output

JSON:

```json
{
  "id": 123456,
  "title": "Software Engineer",
  "location": "Remote",
  "published_at": "2026-06-20 15:30",
  "updated_at": "2026-06-21 12:00",
  "absolute_url": "https://boards.greenhouse.io/company/jobs/123456",
  "company": "Stripe",
  "deadline": "2026-07-15 23:59"
}
```

CSV:

```csv
id,title,location,published_at,updated_at,absolute_url,company,deadline
123456,Software Engineer,Remote,...
```

---

## Technical Notes

### Validation

Each company slug is checked before being added:

```python
https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
```

Invalid slugs are rejected immediately.

---

### Deduplication Strategy

Local deduplication is used inside each company fetch to prevent unnecessary parsing.

This reduces computational overhead and improves performance.

Complexity:

* Fetching: O(n)
* Deduplication: O(1) average lookup using Python sets
* Aggregation: O(n)

---

## Limitations

* Only works with public Greenhouse boards
* Depends on Greenhouse API availability
* Job IDs are assumed unique per board

---

## Future Improvements

* Salary filtering
* Keyword search
* Country filtering
* SQLite storage
* Async scraping
* Better analytics dashboard

---

## License

MIT License
