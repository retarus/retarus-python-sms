from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, validator
from retarus.commons.utils import to_camel_case


class Options(BaseModel):
    src: Optional[str]
    encoding: Optional[str]
    billcode: Optional[str]
    status_requested: Optional[bool]
    flash: Optional[bool]
    customer_ref: Optional[str]
    validity_min: Optional[int]
    max_parts: Optional[int]
    invalid_characters: Optional[str]
    qos: Optional[str]
    job_period: Optional[str]
    duplicate_detection: Optional[bool]
    blackout_periods: Optional[List[str]]

    class Config:
        alias_generator = to_camel_case


class Recipient(BaseModel):
    dst: str
    customer_ref: Optional[str]
    blackout_periods: Optional[List[str]]

    class Config:
        alias_generator = to_camel_case


class Messages(BaseModel):
    text: str
    recipients: List[Recipient]


class SmsJob(BaseModel):
    """
    Create an instance of a SmsJob, set all your needed properties and dispatch it to the Retarus server to send it.

    options: Set special properties how the sms should be processed.
    messages*: set your message that you want to send.
    """
    options: Optional[Options]
    messages: List[Messages]

    class Config:
        alias_generator = to_camel_case

    def exclude_optional_dict(model: BaseModel):
        return {**model.dict(exclude_unset=True), **model.dict(exclude_none=True)}

    def minimal(number: str, message: str) -> SmsJob:
        return SmsJob(messages=[Messages(text=message, recipients=[Recipient(dst=number)])])


class JobReport(BaseModel):
    job_id: str
    src: str
    encoding: str
    billcode: str
    status_requested: bool
    flash: bool
    validity_min: int
    customer_ref: str
    qos: str
    receipt_ts: str
    finished_ts: str
    recipient_ids: List[str]

    class Config:
        alias_generator = to_camel_case


class Client(object):
    def send_sms(self, sms: SmsJob):
        pass

    def get_sms_job(self, job_id: str) -> dict:
        pass

    def filter_sms_jobs(self, *args, **kwargs):
        pass

    def server_version(self):
        pass
