Follow this guide when setting up your development environment.

# Setup
## Create a virtual environment with python 3.6 or newer 
```
python3.6 -m venv venv
```

## Activate virtual environment
```
(win+cmd) venv\Scripts\activate.bat
(win+sh) source venv/Scripts/activate
(linux) source venv/bin/activate
```

## Install packages with pip
Run this when the requirements change
```
# if you just want to run the project without tests
pip install -r requirements/common.txt
# if you want to run the tests locally
pip install -r requirements/test.txt
# Note: the root requirements.txt file is for heroku and links
# to requirements/deploy.txt
```

## Create and Migrate database
```
# You will need to download postgresql based on your development platform
votingsite$ psql -c 'create database votingapp' -U postgres
votingsite$ python manage.py migrate  # do this anytime there are changes
```

## Download geckodriver and firefox
Only required if you are running the Integration Tests
```
https://github.com/mozilla/geckodriver/releases
(win) Place the exe inside the venv/Scripts folder
(linux) Place in venv/bin folder
```

# Testing
Run Django's test runner
```
votingsite$ python manage.py test
votingsite$ python manage.py test functional_tests # only functionl tests
votingsite$ python manage.py test polls # skip functional tests
```