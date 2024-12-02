# Noovox App Front End

This is the code for our front-end

## Development requirements
This should be done in the root directory (one level up from the directory this file is in)
First setup python environment:
- install Python 3.13, Pip, and Pyenv
- setup and activate a virtual environment:
    - `pyenv virtualenv 3.13 noovox`
    - `pyenv activate noovox`
(Optional in VSCode) Select the new environment as your VSCode interpreter
- Ctrl-Shift-P, and `Python: Select Interpreter`
- Select the newly created virtual environment
Then change directory to this directory and run:
    - `pip install -r requirements.txt`
    - `pip install -e .`

## Testing
To run tests simply run:
```
pytest
```