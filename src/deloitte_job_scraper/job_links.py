"""Module responsible for generating an exhaustive list of all the jobs listed on usijobs.deloitte.com"""

import requests
from bs4 import BeautifulSoup
import math
from itertools import batched
from concurrent.futures import ThreadPoolExecutor
import sys
import os


def _get_job_links(link) -> list[str]:
    links = []
    response = requests.get(
        "https://usijobs.deloitte.com/en_US/careersUSI/SearchJobs/?jobRecordsPerPage=10&jobOffset="
        + str(link)
    )
    soup = BeautifulSoup(response.text, "lxml")
    linksOnPage = soup.find_all("a", class_="link")
    for jobLink in linksOnPage:
        jobLink = str(jobLink.get("href"))
        if jobLink.startswith(
            "https://usijobs.deloitte.com/en_US/careersUSI/JobDetail/"
        ):
            links.append(jobLink)
    return links


def getJobLinks() -> list[str]:
    links = []
    link = "https://usijobs.deloitte.com/en_US/careersUSI/SearchJobs/?jobRecordsPerPage=10&jobOffset="

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    noOfJobs = soup.find("span", class_="jobListTotalRecords")
    noOfJobs = int(noOfJobs.text) if noOfJobs is not None else 0

    print(f"Found {noOfJobs} jobs.")

    # Find all job links

    pages = range(0, (math.floor(noOfJobs / 10) * 10) + 1, 10)
    MAX_THREADS = (os.cpu_count() or 10) * 2

    for _pages in batched(pages, MAX_THREADS):
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as exec:
            futures = [exec.submit(_get_job_links, page) for page in _pages]
            results = [f.result() for f in futures]
            for result in results:
                links.extend(result)
                sys.stdout.write(f"\rLinks added : {len(links)}")
                sys.stdout.flush()

    return links
