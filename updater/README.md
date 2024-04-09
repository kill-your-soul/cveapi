# CVEAPI_INIT
Script for first init of CVEAPI database

### Prerequisites
1. Python 3

Copy and fill out `.env.example` to `.env`

### Run via pip

1. Create virtual environment
    ```bash
    python -m venv .venv
    ```
2. Install dependencies
    ```bash
    source ./.venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run script
    ```bash
    python main.py
    ```

### Run via poetry
1. Install dependencies
    ```bash
    poetry install
    ```

2. Run script
    ```bash
    poetry run python main.py
    ```

