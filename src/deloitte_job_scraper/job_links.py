# Module responsible for generating an exhaustive list of all the jobs listed on usijobs.deloitte.com

import requests
from bs4 import BeautifulSoup
import math
import sys
import pandas as pd
import os


def getJobLinks() -> list[str]:
    links = []
    link = "https://usijobs.deloitte.com/en_US/careersUSI/SearchJobs/?jobRecordsPerPage=10&jobOffset="
    file_path = f"{os.path.abspath('.')}/deloitte_jobs.csv"
    df_exists = False
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print(df)
        df_exists = True

    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    noOfJobs = int(soup.find("span", class_="jobListTotalRecords").text)

    print(f"Found {noOfJobs} jobs.")

    # Find all job links

    for i in range(0, (math.floor(noOfJobs / 10) * 10) + 1, 10):
        response = requests.get(link + str(i))
        soup = BeautifulSoup(response.text, "lxml")
        linksOnPage = soup.find_all("a", class_="link")
        for jobLink in linksOnPage:
            jobLink = str(jobLink.get("href"))
            if jobLink.startswith(
                "https://usijobs.deloitte.com/en_US/careersUSI/JobDetail/"
            ):
                if df_exists:
                    if not (df.jobApplyLink == jobLink).any():
                        links.append(jobLink)

        # Progress
        sys.stdout.write(f"\r Gather Links : {i}")
        sys.stdout.flush()

    print(
        f"\nSkipped {noOfJobs - len(links)} links which were already present in the database"
    )

    return links
