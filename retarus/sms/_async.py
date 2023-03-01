from retarus.commons.transport import Transporter
from .model import Client, SmsJob
from retarus.commons.utils import to_camel_case


class AsyncSmsClient(Client):

    def __init__(self, uris):
        self.transporter = Transporter(uris)

    async def send_sms(self, sms: SmsJob):
        data = sms.exclude_optional_dict()
        url = "/jobs"
        res = await self.transporter.post(url, data)
        return res

    async def get_sms_job(self, job_id: str):
        path = f"jobs/{job_id}"
        res = await self.transporter.get(path)
        return res

    async def filter_sms_jobs(self, *args, **kwargs):
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
        path = "jobs"
        parms = {}
        for key, value in kwargs.items():
            parms[to_camel_case(key)] = str(value) if isinstance(value, bool) else value
        res = await self.transporter.get(path, query_parms=parms)
        return res

    async def server_version(self) -> dict:
        """
        Get current server version and build information.
        """
        path = "version"
        res = await self.transporter.get(path)
        return res
