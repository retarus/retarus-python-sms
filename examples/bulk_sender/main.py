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


async def send_sms_jobs(jobs: List[SmsJob]):    
    res_futures = []
    for job in jobs:
        res = asyncio.ensure_future(async_sdk.client.send_sms(job))
        res_futures.append(res)
    return await asyncio.gather(*res_futures)


async def get_sms_reports(ids: list[str]):
    res_futures = []
    for x in ids:
        res = asyncio.ensure_future(async_sdk.client.get_sms_job(x["jobId"]))
        res_futures.append(res)
    return await asyncio.gather(*res_futures)


def write_reports(reports: list):
    # save the reports on the local machine
    time = datetime.utcnow()
    path = f"in/{time}-report.json"
    with open(path, "w+") as file:
        json.dump(reports, file)


async def main():

    prepared_jobs: List[SmsJob] = []
    df = pd.read_csv("assets/sms_data.csv", converters={'number': str})
    for data in df.values:
        recipient = Recipient(dst=data[2])
        firstname = data[1]
        message = Messages(
            text=f"Hello {firstname}, Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem",
            recipients=[recipient],
        )
        job = SmsJob(messages=[message])
        prepared_jobs.append(job)
    job_ids = asyncio.ensure_future(send_sms_jobs(prepared_jobs))
    await job_ids
    
    reports = []
    
    # delay for the server to process the jobs and create the reports
    await asyncio.sleep(2)
    reports = asyncio.ensure_future(get_sms_reports(job_ids.result()))
    await reports

    write_reports(reports.result())


if __name__ == "__main__":
    asyncio.run(main())
