from typing import List
import pandas as pd
import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from retarus.sms.client import SmsClient
from retarus.sms.model import SmsJob, Messages, Recipient
from retarus.commons.config import Configuration


'''
How to use this example
1. Setup the SDK like described in the README file on top level of the repository. If 
   you need additonal help, please have a look at our OpenAPI here: 
   https://developers.retarus.com/docs/sms/api/sms-sending-api/
2. Create an .env file somewhere in your project. It must at least contain key / value
   pairs of "retarus_userid" and "retarus_sms_password". You need the values to
   authenticate as can be seen below. An entry looks like this:
   retarus_userid=user123
   We recommend to create the .env file on the same level as this script.
3. This example will overtake the contacts from the sms_data.csv in the assets folder 
   in the sms examples. Please replace the recipient numbers by your own one(s) to see a
   result when you send the SMS.
4. When you are satisfied with your settings, execute this script. As a confirmation,
   this example prints the job IDs that you can use to check it's status. Please see
   our example 'get_status_async.py' for details on getting a status. Feel free to adjust
   the status handling in the way you like it. For example, you could report it in a
   logger and then save it to a log file.
'''


def initialize():
    Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_sms_password"])
    jobs: List[SmsJob] = []
    df = pd.read_csv("assets/sms_data.csv", converters={'number': str})
    for data in df.values:
        recipient = Recipient(dst=data[2])
        firstname = data[1]
        message = Messages(
            text=f"Hello {firstname}, Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem",
            recipients=[recipient],
        )
        job = SmsJob(messages=[message])
        jobs.append(job)

    return jobs


def write_reports(reports):
    # save the reports on the local machine
    time = datetime.utcnow()
    path = f"{time}-report.json".replace(":", "_")
    with open(path, "w") as file:
        json.dump(reports, file, indent=4)


async def send_sms_jobs(jobs: List[SmsJob]):

    # gets the list of jobs and sends it via the sdk and receives a response with the job_id
    job_ids = []
    for job in jobs:
        id = await async_sdk.client.send_sms(job)
        job_ids.append(id)

    return job_ids


async def main(jobs):
    job_ids = await send_sms_jobs(jobs)

    reports = []
    for job_id in job_ids:
        report = await async_sdk.client.get_sms_job(job_id["jobId"])
        reports.append(report)
    
    write_reports(reports)


if __name__ == "__main__":
    # With load_dotenv, you load the env file needed in the initialize function.
    load_dotenv()
    async_sdk = SmsClient(True)
    jobs = initialize()
    asyncio.run(main(jobs))
