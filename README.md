## Retarus Python SDK
The official Python SDK provided by Retarus to contact our messaging services.


## Installation
Install from PyPi using pip, a package manager for Python. Minimum python version 3.8.


```bash
pip install retarus-sms
```


Or you can download the [source code for the Retarus python SDK](https://github.com/retarus/retarus-python-sms) and then build it with following command:
```bash
git clone https://github.com/retarus/retarus-python-sms
cd retarus-python
pip install .
```


## Usage
The Python SDK implements different services that are offered by Retarus. Each service provides a small variety of examples to get a better understanding of how to use their functionality. The examples can be found in the examples directory sorted by each service. Furthermore, you can check out our OpenAPI documents on the interfaces here: https://developers.retarus.com


### Configuring the SDK
First, you need to configure the SDK with your details.
```python
from retarus.commons.configuration import Configuration


Configuration.set_auth(your_user_id, your_password)
```
Each service implements a client, so simply call "retarus.your_service" and create a client that provides your functionality.


```python
from retarus.sms.client import SmsClient


sdk = SmsClient(True)
```
Please note that *True* will use the SDK in an asynchronous way while *False* will work in a synchronous setup.


### Send a SMS
To send a sms, first setup the SDK like described above. For your credentials, we recommend setting up an .env file. It should also contain the customer number.
> **Please note:** Using the API will only work with valid credentials.


After that, you can execute the examples 'send_jobs_async.py' (for asynchronous processing) or 'send_jobs_sync.py' (for synchronous processing) with Python. As a result, you should get a message that reports back the ID of the created job.


In the sms examples folder, you will also find examples on how to retrieve the status of a sms job. The examples contain a little documentation on their own.





