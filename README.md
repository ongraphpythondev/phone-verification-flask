# phone-verification-flask

User can login using registerd phone numbered and an otp is sended to that number which is used for verification.


## Prerequisites:

You will need the following programmes properly installed on your computer.

* [Python](https://www.python.org/) 3.5+
* Virtual Environment

To install virtual environment on your system use:

```bash
pip install virtualenv

or

pip3 install virtualenv #if using linux(for python 3 and above)
```
## Installation             :

```bash
git clone https://github.com/ongraphpythondev/phone-verification-flask.git

virtualenv venv 
      or 
virtualenv venv -p python3 #if using linux(for python 3 and above)

venv\Scripts\activate # for windows
      or
source venv/bin/activate # for linux

# install required packages for the project to run

pip install -r requirements.txt


Create an Authy Application and grab your API Key
https://www.twilio.com/console/authy/applications

```
mv config.py.sample config.py
```

Edit `config.py` and update the API key with your application key. Create a secret key for managing sessions.

## Running

```python verify.py```

navigate to `localhost:5000/phone_verification` to try it out!
