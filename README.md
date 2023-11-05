
# Stock Forecast Model Pipeline 

Model Pipeline for Stock Forecast

## Installation

Python version==3.11.5

Start virtual enviroment. [venv] (https://docs.python.org/3/library/venv.html#venv-def)
```bash
python -m venv .venv
```

Use pip-tools package manager to install project dependencies. [pip-tools] (https://pip-tools.readthedocs.io/en/stable/)
```bash
python -m pip install pip-tools
```

To install dependencies from requirements.in run: 
```bash
pip-compile requirements.in
pip install -r requirements.txt

```

## Usage

```bash
python run.py
```

## Project Structure
```bash
tree -d -I __pycache__
```
```
.
├── app
│   ├── static
│   │   ├── assets
│   │   │   └── dist
│   │   └── images
│   └── templates
├── pipeline
│   ├── components
│   ├── data
│   │   ├── processed
│   │   └── raw
│   ├── history
│   ├── models
│   ├── notebooks
│   │   └── utils
│   ├── prediction
│   └── src
│       ├── services
│       └── utils
├── test
└── web_app
    └── templates
```
