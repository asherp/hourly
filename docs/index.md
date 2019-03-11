# Hourly
A simple hour tracker for git projects. ```hourly``` parses your commit messages for "clock in/out" keywords and uses their unix timestamps to precisely calculate work hours.


## Getting Started

## Install

    pip install hourly


### Requirements

	pandas
    gitpython

### Usage

Hourly will look for key words for clocking in/out.

To clock in:
```console
    git commit -m "clock in - starting work on new feature"
```
do stuff as usual, then clock out
```console
    git commit -m "clock out - finished feature"
```

Visit the [Tutorial](README.ipynb) for a detailed walk-through of the main functions.