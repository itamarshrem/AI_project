# Connect Four Cube

[![Build Status](https://travis-ci.com/keykey7/connect4cube.svg?branch=master)](https://travis-ci.com/keykey7/connect4cube)
[![License](https://img.shields.io/badge/licence-GPLv3-blue)](LICENCE)

A 3D connect four game ("4 gewinnt").

### Development Environment
* `python3.7`
* `pipenv` as package manager (`pip install --user pipenv`)
* PyCharm: [Configure pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html) 
* Shell:
    ```bash
    pipenv install --dev --three
    pipenv shell
    python3 -m connect4cube
    ```

For an opinionated Raspberry PI setup see [RASPI.md](RASPI.md).

### Testing
```bash
pytest
flake8
```
Running the VPython 3D mockup:
```bash
PYTHONPATH=$(pwd) python3 -m connect4cube --vpython
```
