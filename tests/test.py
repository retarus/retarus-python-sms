import pytest
import os

from retarus.sms.client import SmsClient
from retarus.sms.model import SmsJob
from retarus.commons.config import Configuration
from retarus.commons.exceptions import ConfigurationError


sdk = SmsClient(is_async=True)

jobIds = []
def init():
    Configuration.set_auth(os.environ["retarus_userid"], os.environ["retarus_sms_password"])


@pytest.mark.asyncio
async def test_authentication_validation():
    Configuration.auth = {}
    error = {}
    try:
        res = await sdk.client.filter_sms_jobs(job_ids_only=True, limit=2)
    except Exception as e:
        error = e

    if error == {}:
        assert False


@pytest.mark.asyncio
async def test_server_version():
    init()

    res = await sdk.client.server_version()
    print(res)
    assert isinstance(res, dict)


@pytest.mark.asyncio
async def test_Send_sms():
    global jobIds
    init()
    sms = SmsJob.minimal("+4917600000000", "Hallo Welt")
    res = await sdk.client.send_sms(sms)
    print(res)

    sms = SmsJob.minimal("+4917600000000", "Hallo Welt")
    res = await sdk.client.send_sms(sms)

@pytest.mark.asyncio
async def test_filter_sms_jobs():
    init()
    
    res = await sdk.client.filter_sms_jobs(job_ids_only=True, limit=1)
    print(res)
    if len(res) != 1:
        assert False



sync_sdk = SmsClient()

def test_sync_client():
    init()
    res = sync_sdk.client.filter_sms_jobs(limit=1, job_ids_only=True)
    print(res)
    if len(res) != 1:
        assert False
