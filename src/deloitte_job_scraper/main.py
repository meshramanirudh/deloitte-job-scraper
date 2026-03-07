import datetime
from itertools import batched
from deloitte_job_scraper.job_links import getJobLinks
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv("deloitte_jobs.csv") if os.path.isfile("deloitte_jobs.csv") else None


def _get_job_detail(link: str) -> tuple[str, dict] | None:
    global df
    if df is not None and not df.empty:
        if df.jobApplyLink[df.jobApplyLink == link].any():
            return
    try:
        _job_details = dict()
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "lxml")

        jobDescriptionIdentifier = "container--boxed"
        jobDescription = soup.find("div", class_=jobDescriptionIdentifier)
        jobDescription = jobDescription.text if jobDescription is not None else ""

        jobTitleIdentifier = "article__header__text__title--4"
        jobTitle = soup.find("h2", class_=jobTitleIdentifier)
        jobTitle = jobTitle.text if jobTitle is not None else ""

        jobLocationsIdentifier = "article__header--locations"
        jobLocations = soup.find("div", class_=jobLocationsIdentifier)
        jobLocations = jobLocations.text if jobLocations is not None else ""
        jobLocations = jobLocations.strip("\n").split("\n")

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
            "addedOn": datetime.datetime.now(),
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
    MAX_THREADS = (os.cpu_count() or 10) * 2

    for _links in batched(links, MAX_THREADS):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as exec:
            futures = [exec.submit(_get_job_detail, link) for link in _links]
            results = [f.result() for f in futures]
            for job in results:
                if job:
                    jobs[job[0]] = job[1]
    export_csv(jobs)


def export_csv(jobs: dict) -> None:
    output_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    filename = "deloitte_jobs.csv"
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
        df = pd.concat(
            [df, pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"})]
        )
        df.to_csv(f"{output_directory}/{filename}", index=False)
    else:
        pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"}).to_csv(
            f"{output_directory}/{filename}", index=False
        )

    print(f"\nSaved {filename} in {output_directory}")


def main():
    print(
        f"Output directory : {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))}"
    )

    links = getJobLinks()
    getDetails(links)


if __name__ == "__main__":
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
