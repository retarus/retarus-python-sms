from typing import List
import pandas as pd
import asyncio
from retarus.sms.client import SmsClient
from retarus.sms.model import SmsJob, Messages, Recipient
from retarus.commons.config import Configuration
import os
import json
from pathlib import Path
from datetime import datetime

Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_sms_password"])

async_sdk = SmsClient(True)


async def send_fax_job(jobs: List[SmsJob]):
    # gets the list of jobs and sends it via the sdk and receives a response with the job_id
    reports = []
    for job in jobs:
        res = await async_sdk.client.send_sms(job)
        reports.append(res)

    return reports


def write_reports(reports: list):
    # save the reports on the local machine
    time = datetime.utcnow()
    path = f"in/{time}-report.json"
    with open(path, "w+") as file:
        json.dump(reports, file)


async def main():
    prepared_jobs: List[SmsJob] = []
    df = pd.read_csv("assets/sms_data.csv")
    for data in df.values:
        recipient = Recipient(dst=data[2])
        firstname = data[1]
        message = Messages(
            text=f"Hello {firstname}, Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem",
            recipients=[recipient],
        )
        job = SmsJob(messages=[message])
        prepared_jobs.append(job)

    job_ids = await send_fax_job(prepared_jobs)
    reports = []
    for job_id in job_ids:
        report = await async_sdk.client.get_sms_job(job_id["jobId"])
        reports.append(report)

    write_reports(reports)


if __name__ == "__main__":
    asyncio.run(main())
