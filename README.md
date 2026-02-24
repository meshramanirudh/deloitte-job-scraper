## Introduction

**What is this Project?**

`deloitte-job-scraper` is a Python based CLI tool that scrapes job listings from the [Deloitte USI Careers Page](https://usijobs.deloitte.com/en_US/careersusi) and exports them into a structured CSV file for easy analysis and filtering.

**What problem does this project solve?**

The Deloitte USI Careers Page only allows the user to view 10 job postings at a time whilst having ~500 active job listings. Additionally, important details such as YoE and key skill requirements are only visible after opening each individual job posting. This makes manual browsing time consuming and inefficient.

This projects addresses that limitation by programmatically collecting all available job postings in one run. The scraper navigates the careers page, gathers links to all job listings, visits each posting individually, and extracts relevant details including job requisition code, job title and job description. Once completed, the data is exported into a CSV file that can be viewed and filtered using spreadsheet tools.

## Prerequisites
- Python `3.10+`
- `pip`

## Installation
```bash
# cd desired/installation/path
git clone https://github.com/meshramanirudh/deloitte-job-scraper
cd deloitte-job-scraper
python3 -m venv venv # Create a virtual environment
source bin/activate/activate # for Linux
pip install . # Install project dependencies
# Or for installing and editing:
# pip install -e .
```

## Usage
After following the installation steps simply run

```
deloitte-job-scraper
```

**Here's what it should look like:**
![Screenshot](images/Screenshot.png)

**Typical Output**:
```
Found X jobs.
	
	Gathering Links : ABC
	Details for Job ID 123456 added : ABC/XYZ

Saved deloitte_jobs.csv in path/to/your/project_installation
```
`deloitte_jobs.csv` will be saved in the root directory of your project installation.

| jobCode | jobTitle | jobDescription |
| ------- | -------- | -------------- |
| 123     | title    | description    |

## To-Do
- [ ] Need to use `job_links` as a generator for `main` to reduce the turnaround time.
- [ ] Remove white-spaces and other non-printable characters from the texts before exporting.
- [ ] Update `README.md`
- [x] Extract {City, State} for each job opening.

> [!CAUTION]
> This project is for educational purposes only. It demonstrates web scraping techniques using public web pages. The author does not distribute, or claim ownership of any scraped data. Users are responsible for complying with the terms of service of the websites they access.

## About Me

Hey there 👋 Thank you for reading thus far. I am [Anirudh](https://www.linkedin.com/in/anirudh-meshram/), currently upskilling myself for **Analyst** roles. As of writing this, I am looking for roles which tests my **Excel, Python, Power BI and SQL** skills in real business-case scenarios.

In my last role as a **Data Analyst Associate**, I saved **~200 hours** using a **Python web-automation tool** which automatically generates paginated reports from our SaaS platform - which was earlier done manually! Additionally I solely led the development of **Power BI dashboards** in collaboration with cross-functional teams (Operations, Sales, Finance, Product, Marketing), allowing non-technical stakeholders to access data independently.

If you, or anyone you know, is looking for candidates who match my skill set, Do connect with me on [LinkedIn](https://www.linkedin.com/in/anirudh-meshram/).

## License
MIT License
