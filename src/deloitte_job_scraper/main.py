def main():
    from deloitte_job_scraper.job_links import getJobLinks
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import sys
    import os

    links = getJobLinks()
    jobs = dict()

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
            "jobApplyLink": f"https://usijobs.deloitte.com/en_US/careersUSI/Login?jobId={jobCode}",
        }

        # Progress
        sys.stdout.write(
            f"\r Details for Job ID {jobCode} added : {len(jobs.keys())}/{len(links)}"
        )
        sys.stdout.flush()

    print()

    filename = "deloitte_jobs"
    pd.DataFrame(jobs).T.reset_index().rename(columns={"index": "jobId"}).to_csv(
        f"../../{filename}.csv", index=False
    )

    print(f"Saved {filename}.csv in {os.path.abspath('.')}")


if __name__ == "__main__":
    main()
