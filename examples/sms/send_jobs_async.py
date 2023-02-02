from typing import List
import pandas as pd
import asyncio
import os
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
   this example prints the job ID that you can use to check it's status. Please see
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


async def send_sms_jobs(jobs: List[SmsJob]):
    async_sdk = SmsClient(True)

    # gets the list of jobs and sends it via the sdk and receives a response with the job_id
    for job in jobs:
        id = await async_sdk.client.send_sms(job)
        print("Fax job was sent successfully, you can track it with job ID " + id['jobId'])



if __name__ == "__main__":
    # With load_dotenv, you load the env file needed in the initialize function.
    load_dotenv()
    jobs = initialize()
    asyncio.run(send_sms_jobs(jobs))
