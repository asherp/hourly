# Hourly
A simple hour tracker for git projects. ```hourly``` parses your commit messages for "clock in/out" keywords and uses their unix timestamps to precisely calculate work hours.


## Getting Started

## Install

    pip install hourly


### Requirements

* pandas
* gitpython
* click

### Usage

Hourly will look for key words for clocking in/out.

To clock in:
```console
    git commit -m "clock in - starting work on new feature"
```
Then, commit other work as usual, then clock out:

```console
    git commit -m "clock out - finished feature"
```

Then run hourly from your git directory. For example, here's what happens when you run hourly within hourly:

```console
hourly -s 2018-10-21 -e 2019-3-10 --ignore "pro bono"
```

this generates the following output:
```console
pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
0 days 02:42:28, 2.71 hours worked
216.62 usd
writing to file labor-20181028-134448_to_20190225-124951.csv
```
The work logs are stored in the local directory.

Visit the [Tutorial](README.ipynb) for a detailed walk-through of the main functions.

### Tests

I use the pytest suite with pytest-cov

```console
pip install pytest pytest-cov
```
To run the tests, navigate to the base of this repo, then

```console
py.test tests.py --cov=hourly
```
