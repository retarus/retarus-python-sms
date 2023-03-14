from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, validator
from retarus.commons.utils import to_camel_case


class Options(BaseModel):
    """
    This object can be used to set more details about how the SmsJob should be processed. Short explaination for each key:

    src: Set your source number
    encoding: which encoding should be used, default: STANDARD options: [ STANDARD, UTF-16 ]
    billcode: Max. 70 characters.
    status_requested: Delivery notification requested.
    flash: specify if the sms should be express or not
    customer_ref: Recommended max. 64 characters.
    validity_min: Validity of the SMS in minutes. When 0 the provider’s default value is used. Otherwise, values must be between 5 and 2880 minutes.
    max_parts: Maximum allowed parts in a multi-part message. Values must be between 1 and 20. Longer messages are truncated.
    invalid_characters: Define how to handle invalid characters in SMS. options: [ REFUSE, REPLACE, TO_UTF16, TRANSLITERATE ]
    qos: Quality of Service. options: [ EXPRESS, NORMAL ]
    job_period: Timestamp to schedule when to start processing the SMS Job (iso-8601).
    duplicate_detection: bool
    blackout_periods: Time periods in which no SMS is delivered (iso-8601). SMS will be scheduled to be sent at the end of the blackout period.
    """
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
    """
    Specify a message and a list of recipient which should receive this message.
    """
    text: str
    recipients: List[Recipient]


class SmsJob(BaseModel):
    """
    Create an instance of a SmsJob, set all your needed properties and dispatch it to the Retarus server to send it.

    options: Set special properties how the sms should be processed.
    messages*: set your messages that you want to send. Via this SmsJob Object you are able to send multiple messages at a time.
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
