# Backend Server

This is the backend server for the project. 

## Requirements
### uv

This project uses the Python package manager [uv](https://github.com/astral-sh/uv), 
because of its simplicity and significant performance advantages compared to other package managers.

A guide to installing uv can be found [here](https://github.com/astral-sh/uv)

Once uv has been installed, make sure you're in this directory ([/finance-management-system/](/finance-management-system))

Then, use `uv sync` to update your local virtual environment to the project's requirements. This command will install the required Python version, along with Django and all the required dependencies.
```
uv sync
```
Note that all commands involving Python (for example running a file with `python main.py`) will need to use `uv run` (`uv run main.py`).

If a change to the code requires a new Python dependency to be installed, add it to the project requirements with:
```
uv add [package name]
```

### Django

This project uses the Python web framework [Django](https://www.djangoproject.com/). If you haven't used Django before, it may be helpful to review the [Documentation](https://docs.djangoproject.com/).

## Running the server

The server can be ran using the file `manage.py`, with the following command:
```
uv run manage.py runserver
```
When the server is started with this command, it supports automatic reloading, meaning you don't need to restart the server when you make changes to the code. However, some actions like adding files don't trigger a restart, so you may need to restart the server in these cases.