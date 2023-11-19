# Quant Coin

## Index

### 1. How to install

0. Install Python which version is over 3.10.9.
1. Clone repository somewhere into your computer.
    ```bash
    $ git clone https://github.com/myeonghan-nim/quant-coin.git
    ```
2. Go into cloned folder.
3. Make virtual environment.
    ```bash
    $ python -m venv venv
    ```
4. Activate environment.
    ```bash
    $ source venv/bin/activate # in macOS/Linux
    $ venv/Scripts/activate.bat # in Windows
    ```
5. Install dependencies using pip.
    ```bash
    $ pip install -r requirements.txt --no-cache-dir
    ```
6. Run code.

### 2. How to use

```bash
$ python main.py -h
usage: main.py [-h] [--include-ETH] [--calculate-profit]

Process command line arguments.

options:
  -h, --help            show this help message and exit
  --include-ETH         Include ETH in the result.
  --calculate-profit    Include calculated profit in the result.
```
