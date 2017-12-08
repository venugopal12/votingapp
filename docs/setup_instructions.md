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
pip install -r requirements.txt
```

## Migrate database
```
votingsite$ mkdir ../database
votingsite$ python manage.py makemigrations
votingsite$ python manage.py migrate
```

## Download geckodriver
* not yet required *
Only required if you are running the Integration Tests
```
https://github.com/mozilla/geckodriver/releases
(win) Place the exe inside the venv/Scripts folder
(linux) Place in venv/bin folder
```
