import asyncio
from ._async import AsyncSmsClient
from .model import Client, SmsJob


class SyncSmsClient(Client):
    def __init__(self, uris):
        self.client = AsyncSmsClient(uris)
        self.loop = asyncio.new_event_loop()

    def send_sms(self, sms: SmsJob):
        res = self.loop.run_until_complete(self.client.send_sms(sms))
        return res

    def get_sms_job(self, job_id: str) -> dict:
        res = self.loop.run_until_complete(self.client.get_sms_job(job_id))
        return res

    def filter_sms_jobs(self, *args, **kwargs):
        """
        Gets all sms reports that match the given criteria.

        Parameters:
        job_ids_only: bool
        from_ts: str (e.g. 2018-06-13T00:00+02:00) can only be max 30 days before to_ts
        to_ts: str (e.g. 2018-06-20T00:00+02:00)
        open: bool
        offset: int (default: 0)
        limit: int (default: 100)
        """
        res = self.loop.run_until_complete(self.client.filter_sms_jobs(**kwargs))
        return res

    def server_version(self):
        res = self.loop.run_until_complete(self.client.server_version())
        return res
