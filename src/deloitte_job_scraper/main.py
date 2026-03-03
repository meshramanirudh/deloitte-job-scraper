from itertools import batched
from deloitte_job_scraper.job_links import getJobLinks
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from concurrent.futures import ThreadPoolExecutor


def _get_job_detail(link) -> tuple[str, dict] | None:
    try:
        _job_details = dict()
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "lxml")

        jobDescriptionIdentifier = "container--boxed"
        jobDescription = soup.find("div", class_=jobDescriptionIdentifier).text

        jobTitleIdentifier = "article__header__text__title--4"
        jobTitle = soup.find("h2", class_=jobTitleIdentifier).text

        jobLocationsIdentifier = "article__header--locations"
        jobLocations = (
            str(soup.find("div", class_=jobLocationsIdentifier).text)
            .strip("\n")
            .split("\n")
        )

        if len(jobLocations) != 1:
            jobLocations = ";".join(jobLocations)
        else:
            jobLocations = jobLocations[0]

        # Job Requisition Code
        jobCode = str(link[link.rfind("/") + 1 :])

        _job_details = {
            "jobTitle": jobTitle.strip(),
            "jobDescription": jobDescription.strip(),
            "jobLocations": jobLocations.strip(),
            "jobApplyLink": f"{link}",
        }

        # Progress
        sys.stdout.write(f"\r Details for Job ID {jobCode} added")
        sys.stdout.flush()
        return (jobCode, _job_details)
    except:
        return


def getDetails(links: list[str]):
    """Loop through all the links and scrape the relevant information"""
    jobs = dict()
    MAX_THREADS = 10

    for _links in batched(links, MAX_THREADS):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as exec:
            futures = [exec.submit(_get_job_detail, link) for link in _links]
            results = [f.result() for f in futures]
            for job in results:
                if job:
                    jobs[job[0]] = job[1]
    export_csv(jobs)


def export_csv(jobs: dict) -> None:
    filename = "deloitte_jobs.csv"
    pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"}).to_csv(
        filename, index=False
    )

    print(f"\nSaved {filename} in {os.path.abspath('.')}")


def main():
    print(f"Output directory : {os.path.abspath('.')}")

    links = getJobLinks()
    getDetails(links)


if __name__ == "__main__":
    main()
