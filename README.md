# Hourly
A simple hour tracker for git projects. ```hourly``` parses your commit messages for "clock in/out" keywords and uses their unix timestamps to precisely calculate work hours.

## Usage

To clock in:
```console
  hourly -in
```
The above command updates the WorkLog.md file, and commits it with the message "clock-in". Feel free to edit this log file to provide supporting documentation for this work session.

When you are finished committing other work for this session, you may clock out:

```console
    hourly -out
```

When you are ready to generate a timesheet for your repo, simply run hourly from your git directory:

```console
  hourly
```
Hourly parses all the commit messages for clock in/out keywords and uses git's timestamps to determine how long each session lasted.

For example, here's what happens when you run hourly *on the hourly repo itself*:

```console
hourly -s 2018-10-21 -e 2019-3-10 --ignore "pro bono"
pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
0 days 02:42:28, 2.71 hours worked
216.62 usd
                     TimeIn           LogIn                   TimeOut          LogOut TimeDelta
0 2018-10-28 13:44:48-04:00        clock in 2018-10-28 13:56:35-04:00       clock out  00:11:47
1 2019-02-25 10:19:10-05:00  clock in T-1hr 2019-02-25 12:49:51-05:00  clock out T-5m  02:30:41
```

To store the logs in a csv file, include an ouput prefix:
```console
hourly -s 2018-10-21 -e 2019-3-10 --ignore "pro bono" -o Pembroke
pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
0 days 02:42:28, 2.71 hours worked
216.62 usd
writing to file Pembroke-20181028-134448_to_20190225-124951.csv
```

Visit the [Tutorial](README.ipynb) for a detailed walk-through of the main functions.

## Getting Started

## Install

    pip install hourly


### Requirements

* pandas
* gitpython
* click


### Tests

I use the pytest suite with pytest-cov

```console
pip install pytest pytest-cov
```
To run the tests, navigate to the base of this repo, then

```console
py.test tests.py --cov=hourly
```

## Full Options

```console
Usage: hourly [OPTIONS] [GITDIR]

Options:
  --version                   Show the version and exit.
  -s, --start-date TEXT       Date (time) to begin invoice
  -e, --end-date TEXT         Date (time) to end invoice
  -o, --outfile TEXT
  -err, --errant-clocks TEXT  hash of the commit to skip
  -i, --ignore TEXT           Ignore sessions by keyword such as "pro bono"
  -work, --print-work         print the work log and exit
  --match-logs                raise an error if in/out logs do not match
  -w, --wage FLOAT            wage to charge (in chosen currency)
  -c, --currency TEXT         Currency to print earnings
  -in, --clock-in             clock in to current repo
  -out, --clock-out           clock out of current repo
  -m, --message TEXT          clock in/out message
  -log, --logfile PATH        File in which to log work messages
  --help                      Show this message and exit.
```

