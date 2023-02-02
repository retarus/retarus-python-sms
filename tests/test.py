import pytest
import os

from retarus.sms.client import SmsClient
from retarus.commons.config import Configuration
from retarus.commons.exceptions import ConfigurationError


sdk = SmsClient(is_async=True)


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


sync_sdk = SmsClient()


@pytest.mark.asyncio
async def test_server_version():
    init()

    res = await sdk.client.server_version()
    print(res)
    assert isinstance(res, dict)


@pytest.mark.asyncio
async def test_filter_sms_jobs():
    init()

    res = await sdk.client.filter_sms_jobs(job_ids_only=True, limit=2)
    print(res)
    if len(res) != 2:
        assert False


def test_sync_client():
    init()
    res = sync_sdk.client.filter_sms_jobs(limit=2, job_ids_only=True)
    print(res)
    if len(res) != 2:
        assert False
