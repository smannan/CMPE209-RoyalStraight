# Server installation

## Requirements

- Python3.7 (3.5+ probably works)
- Requirements.txt packages

## Instructions

### Install requirements.

From a virtualenv (recommended):

`pip install -r requirements.txt`

If not virtualenv, probably this:

`pip3 install --user -r requirements.txt`

### Run server.

`python pokerapp.py`

### Browse server

* http://localhost:5000/api/users/
* http://localhost:5000/api/user/warnold22
* http://localhost:5000/api/docs
