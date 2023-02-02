from typing import List

from .model import Client

from retarus.commons.region import RegionUri, Region
from ._async import AsyncSmsClient
from .sync import SyncSmsClient


class SmsClient(object):
    __sms_uris: List[RegionUri] = [
        RegionUri(
            region=Region.Europe,
            ha_uri="https://sms4a.eu.retarus.com",
            urls=["https://sms4a.de1.retarus.com", "https://sms4a.de2.retarus.com"],
        )
    ]

    def __init__(self, is_async: bool = False):
        self.is_async: bool = is_async
        if is_async:
            self.client: Client = AsyncSmsClient(self.__sms_uris)
        else:
            self.client: Client = SyncSmsClient(self.__sms_uris)
