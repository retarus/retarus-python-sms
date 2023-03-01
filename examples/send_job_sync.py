from typing import List
import pandas as pd
import os
from dotenv import load_dotenv 

from retarus.sms.client import SmsClient
from retarus.sms.model import SmsJob, Messages, Recipient
from retarus.commons.config import Configuration


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

def main():
    jobs = initialize()
    sdk = SmsClient()
    for job in jobs:
        res = sdk.client.send_sms(job)
        print(res)



if __name__ == '__main__':
    main()