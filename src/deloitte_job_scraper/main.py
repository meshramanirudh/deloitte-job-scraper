from deloitte_job_scraper.job_links import getJobLinks
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os


def getDetails(links: list[str]) -> dict:
    jobs = dict()
    try:
        for link in links:
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

            jobs[jobCode] = {
                "jobTitle": jobTitle.strip(),
                "jobDescription": jobDescription.strip(),
                "jobLocations": jobLocations.strip(),
                "jobApplyLink": f"{link}",
            }

            # Progress
            sys.stdout.write(
                f"\r Details for Job ID {jobCode} added : {len(jobs.keys())}/{len(links)}"
            )
            sys.stdout.flush()
        return jobs
    except:
        print("An error has occured, Exporting with existing data...")
        create_df(jobs)


def export_csv(jobs: dict) -> None:
    file_path = f"{os.path.abspath('.')}/deloitte_jobs.csv"

    df_exists = False
    if os.path.exists(file_path):
        df_exists = True

    print()

    filename = "deloitte_jobs"

    if df_exists:
        pd.concat(
            [
                pd.read_csv(file_path),
                pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"}),
            ]
        ).to_csv(f"{os.path.abspath('.')}/{filename}.csv", index=False)
    else:
        pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"}).to_csv(
            f"{os.path.abspath('.')}/{filename}.csv", index=False
        )
    print(f"Saved {filename}.csv in {os.path.abspath('.')}")


def main():
    print(f"Output directory : {os.path.abspath('.')}")

    links = getJobLinks()
    jobs = getDetails(links)
    export_csv(jobs)


if __name__ == "__main__":
    main()
