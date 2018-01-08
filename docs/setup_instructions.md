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
```
# if you just want to run the project without tests
pip install -r requirements/common.txt
# if you want to run the tests locally
pip install -r requirements/test.txt
# Note: the root requirements.txt file is for heroku and links
# to requirements/deploy.txt
```

## Migrate database
```
votingsite$ python manage.py migrate
```

## Download geckodriver and firefox
Only required if you are running the Integration Tests
```
https://github.com/mozilla/geckodriver/releases
(win) Place the exe inside the venv/Scripts folder
(linux) Place in venv/bin folder
```

## Create local config
Copy the example file from the docs folder to the votingsite folder.

Edit the file for your own personal settings.
