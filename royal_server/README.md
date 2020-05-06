# Server installation

## Requirements

- Python3.7 (3.5+ probably works)
- Requirements.txt packages

## Instructions

### Install requirements.

Install nginx

`sudo apt install nginx`

From a virtualenv (recommended):

`pip install -r requirements.txt`

If not virtualenv, probably this:

`pip3 install --user -r requirements.txt`

### Start API, with WSGI

* Adjust proxypass config for nginx
* Run `sudo nginx -t && sudo systemctl restart nginx`
* Add systemd file in files/
* Run `install.sh` for config

### Start API locally if testing

`python poker_api.py`

### Run server interactively

`python game_runner.py`

### Browse server (if local)

* http://localhost:5000/api/users/
* http://localhost:5000/api/user/{username}
* http://localhost:5000/api/docs
