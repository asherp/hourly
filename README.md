# Hourly
A simple hour tracker for git projects, ```hourly``` parses your commit messages for `clock-in` and `clock-out` keywords and uses their unix timestamps to precisely calculate work hours.

## Usage

To clock in:
```console
  hourly-in
```
The above command updates the `WorkLog.md` file, and commits it with the message "clock-in". Feel free to edit this log file to provide supporting documentation for this work session.

When you are finished committing other work for this session, you may clock out:

```console
  hourly-out
```

When you are ready to generate a timesheet for your repo, run hourly from your git directory:

```console
  hourly
```
Hourly parses all the commit messages for clock in/out keywords and uses git's timestamps to determine how long each session lasted.

For example, here's what happens when you run hourly *on the hourly repo itself*:

```console
  hourly repo.start_date="2018-10-21" repo.end_date="2019-3-10" repo.ignore="pro bono"

pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
                     TimeIn           LogIn                   TimeOut          LogOut TimeDelta     Hours
0 2018-10-28 13:44:48-04:00        clock in 2018-10-28 13:56:35-04:00       clock out  00:11:47  0.196389
1 2019-02-25 10:19:10-05:00  clock in T-1hr 2019-02-25 12:49:51-05:00  clock out T-5m  02:30:41  2.511389
0 days 02:42:28, 2.71 hours worked
```

To store the logs in a csv file, include an ouput prefix:

```console
hourly repo.start_date="2018-10-21" repo.end_date="2019-3-10" repo.ignore="pro bono" report.outfile=Pembroke
pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
                     TimeIn           LogIn                   TimeOut          LogOut TimeDelta     Hours
0 2018-10-28 13:44:48-04:00        clock in 2018-10-28 13:56:35-04:00       clock out  00:11:47  0.196389
1 2019-02-25 10:19:10-05:00  clock in T-1hr 2019-02-25 12:49:51-05:00  clock out T-5m  02:30:41  2.511389
0 days 02:42:28, 2.71 hours worked
writing to file Pembroke-20181028-134448_to_20190225-124951.csv
```

Visit the [Tutorial](README.ipynb) for a detailed walk-through of the main functions.

# Getting Started

## Install

    pip install hourly


## Requirements

* pandas
* gitpython
* plotly
* [hydra](https://hydra.cc/docs/intro)


### Tests

I use the pytest suite with pytest-cov

```console
pip install pytest pytest-cov
```
To run the tests, navigate to the base of this repo, then

```console
py.test tests.py --cov=hourly
```

## Customization

`Hourly` uses [`Hydra`](https://hydra.cc/docs/intro) for customized configuration. The full options are given by hourly's
help command:

<details>
  <summary> hourly --help </summary>

```console
A simple hour tracker for git projects

This application helps users clock in and out of git repos,
as well as generate timesheets for invoicing.

Configure hourly to ignore commits by keyword or hashes

== Configuration groups ==
Compose your configuration from those groups (group=option)

== Config ==
Override anything in the config (foo.bar=value)
commit:
  clock: null
  message: ''
  tminus: null
config_override: hourly-config.yaml
repo:
  end_date: null
  errant_clocks: []
  gitdir: .
  ignore: null
  match_logs: false
  start_date: null
report:
  currency: ''
  outfile: null
  pandas:
    display:
      max_columns: 10
      max_colwidth: 64
      max_rows: null
      width: 600
  timesheet: true
  wage: null
  work: false
vis:
  frequency: 1 d
  plotly:
    figure:
      margin:
        pad: 0
    plot:
      animation_opts: null
      auto_open: true
      auto_play: true
      config: null
      filename: hourly-work.html
      image: null
      image_filename: plot_image
      include_mathjax: cdn
      include_plotlyjs: cdn
      link_text: Export to plot.ly
      output_type: file
      show_link: false
      validate: true
work_log:
  bullet: '*'
  filename: WorkLog.md
  header_depth: 1

Powered by Hydra (https://hydra.cc)
Use --hydra-help to view Hydra specific help
```
<br>
</details>

Each of these can be overridden at runtime. For example,

`hourly commit.clock=in vis=null report.timesheet=False`

This will update the WorkLog.md file and commit a clock-in message without visualizing or printing the timesheet.

!!! note
    `hourly-in` is just syntactic sugar for `hourly commit.clock=in vis=null report.timesheet=False`.

But if we want to override hourly's default without typing it in each time,
we can specify an hourly-config.yaml file in our git repo. Hourly will look
for this file (via the `config_override` option) and override its default configuration,
including any configurations set at command line.

A common use case would be permanently overriding the filename of the work_log you are committing against, to avoid
merge conflicts if multiple developers are working on the same project.


