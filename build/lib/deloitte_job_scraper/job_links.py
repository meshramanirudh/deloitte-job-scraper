# Module responsible for generating an exhaustive list of all the jobs listed on usijobs.deloitte.com

import requests
from bs4 import BeautifulSoup
import math
import sys


def getJobLinks() -> list[str]:
    links = []
    link = "https://usijobs.deloitte.com/en_US/careersUSI/SearchJobs/?jobRecordsPerPage=10&jobOffset="
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    noOfJobs = int(soup.find("span", class_="jobListTotalRecords").text)

    print(f"Found {noOfJobs} jobs.")

    # Find all job links

    for i in range(0, (math.floor(noOfJobs / 10) * 10) + 1, 10):
        response = requests.get(link + str(i))
        soup = BeautifulSoup(response.text, "lxml")
        jobsOnPage = soup.find_all("a", class_="link")
        for jobLink in jobsOnPage:
            if str(jobLink.get("href")).startswith(
                "https://usijobs.deloitte.com/en_US/careersUSI/JobDetail/"
            ):
                links.append(str(jobLink.get("href")))

        break
        # Progress
        sys.stdout.write(f"\r Gathering Links : {len(links)}/{noOfJobs}")
        sys.stdout.flush()

    print()
    return links
