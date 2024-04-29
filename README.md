
# Stock Forecast Model Pipeline 

Model Pipeline for Stock Forecast

This is a mock project designed to automate a model training pipeline by configuring a file (/pipeline/config.json) that specifies all the steps, from fetching data to the training process, and saving it for later deployment.

It also utilizes MLflow to track some experiments but is not configured by a config file; instead, it is configured only by code.

The models created are intended to 'forecast' stock prices, even though there is a significant conceptual error as these series are not stationary. However, for the purpose of this project, it didn't matter.

The Pipeline code (etl, train) is located in the /pipeline/components folder

## Installation

Python version==3.11.5

Start virtual enviroment. [venv] (https://docs.python.org/3/library/venv.html#venv-def)
```bash
python -m venv .venv
source .venv/bin/activate
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

### Output

In the 'pipeline/history' folder, you should find a JSON output containing all the details of the run. It includes input and output of each step and the directory to the model output located in the '/pipeline/models' folder.

## Project Structure
```bash
tree -d -I __pycache__
```
```
.
├── components
│   ├── etl.py
│   └── train.py
│   └── pipeline.py
├── data
│   ├── processed
│   └── raw
├── history
├── models
├── notebooks
│   └── utils
├── prediction
└── src
    ├── services
    └── utils
```
