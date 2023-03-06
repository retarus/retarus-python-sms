## Examples


This folder contains a small set of applications which should visualize how the sms sdk can be used to dispatch messages and fulfill your business needs.

### Credentials
All the example applications still require credentials to authorize your request on the retarus server. So for that the sdk uses environment variables. In this case you can simply export you credentials in your current terminal like this:
```bash
export retarus_userid="your_retarus_userid"
```

Or you could use an ".env" file which contains your credentials and other information with the same variables names as they are called in the examples.
If you are using the .env file you need to add following line to the example and install following package:


```bash
pip install python-dotenv
```


```python
from dotenv import load_dotenv


load_dotenv()
```


To find out which variables are needed you can search for the following statements in the examples:
```python
import os


os.environ["retarus_userid"]
```



