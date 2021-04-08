# Hourly
Hourly is a command-line time tracking tool for git projects. Hourly parses your commit messages for `clock-in` and `clock-out` keywords to precisely estimate work hours. Designed for developers and project managers, hourly makes it easy to see how and where you spend your time. When configured with Stripe or BTCPay, hourly can generate invoices for your specified wage.

## Usage

### Work sessions

To clock in:
```console
hourly-in
```
The above command updates the header of your work log (`WorkLog.md` by default) and commits it with the message "clock-in". 

Stage any changes to your code base. When you are ready to commit:

```console
hourly commit.message="my commit message"
```

Hourly updates the work log with your commit message. Feel free to use the work log to provide additional context.
When you are finished committing other work for this session, you may clock out:

```console
hourly-out
```

Again, hourly updates the work log and commits it with the message "clock-out" along with any other staged files. Read [more
about configuring your work log](WorkLog.md).

### Timesheets

When you are ready to generate a timesheet for your repo, run hourly from your git directory:

```console
hourly-report
```
Hourly parses all the commit messages for clock in/out keywords and uses git's timestamps to determine how long each session lasted.

For example, here's what happens when you run hourly *on the hourly repo itself*:

```console
hourly-report repo.start_date="2018-10-21" repo.end_date="2019-3-10" repo.ignore="pro bono"

pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
                     TimeIn           LogIn                   TimeOut          LogOut TimeDelta     Hours
0 2018-10-28 13:44:48-04:00        clock in 2018-10-28 13:56:35-04:00       clock out  00:11:47  0.196389
1 2019-02-25 10:19:10-05:00  clock in T-1hr 2019-02-25 12:49:51-05:00  clock out T-5m  02:30:41  2.511389
0 days 02:42:28, 2.71 hours worked
```

To save the timesheet as a csv file, include an ouput prefix:

```console
hourly-report repo.start_date="2018-10-21" repo.end_date="2019-3-10" repo.ignore="pro bono" report.filename=Pembroke
pay period: 2018-10-28 13:44:48-04:00 -> 2019-02-25 12:49:51-05:00
ignoring pro bono
                     TimeIn           LogIn                   TimeOut          LogOut TimeDelta     Hours
0 2018-10-28 13:44:48-04:00        clock in 2018-10-28 13:56:35-04:00       clock out  00:11:47  0.196389
1 2019-02-25 10:19:10-05:00  clock in T-1hr 2019-02-25 12:49:51-05:00  clock out T-5m  02:30:41  2.511389
0 days 02:42:28, 2.71 hours worked
writing to file Pembroke-20181028-134448_to_20190225-124951.csv
```

Visit the [Tutorial](README.ipynb) for a detailed walk-through of how hourly generates timesheets.

### Invoicing

To generate an invoice using stripe:

```console
hourly-report invoice=stripe repo.start_date="Jan 1, 2020" stripe.customer.email=myclient@momandpop.com
```

The above command generates a time sheet for this repo, calculates earnings, prepares a stripe invoice,
and asks you to confirm details. After confirmation, an email will be sent from your Stripe account
to myclient@momandpop.com.

The btcpay invoicing is similar:

```console
hourly-report invoice=btcpay repo.start_date="Jan 1, 2020"
```
After confirmation, hourly tells your btcpay server to generate an invoice and displays the corresponding payment url.
Note that BTCPay can be configured for lightning, so streaming payments are possible!

Visit the [Payments](Payments.md) section for more info.

## Getting Started

Hourly is hosted on github under the Apache 2.0 license

[https://github.com/asherp/hourly](https://github.com/asherp/hourly)

### Install

`pip install hourly --upgrade`


### Requirements

* pandas
* gitpython
* [plotly](https://plot.ly/python/)
* [hydra](https://hydra.cc/docs/intro)
* [stripe](https://github.com/stripe/stripe-python) (optional)
* [btcpay-python](https://btcpayserver.org/) (optional)

You can get these dependencies like this:

```console
pip install pandas gitpython plotly
pip install hydra-core --upgrade
```

For invoicing:

```console
pip install btcpay-python
pip install stripe
```

For hourly's docs:

```console
pip install mkdocs mkdocs-material markdown-include mknotebooks
```

### Tests

For integration tests, hourly may be tested against the hourly repo.

Unit tests are based on pytest suite with pytest-cov

```console
pip install pytest pytest-cov
```
To run the tests, navigate to the base of this repo, then

```console
py.test tests.py --cov=hourly
```

## Configuration

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
  identity:
  - name
  - email
  message: ''
  tminus: null
compensation: []
config_override: hourly.yaml
invoice: null
payment: null
repo:
  case_sensitive: false
  end_date: null
  errant_clocks: []
  gitdir: .
  ignore: null
  match_logs: false
  start_date: null
report:
  currency: ''
  filename: null
  pandas:
    display:
      max_columns: 10
      max_colwidth: 45
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

<details>
<summary>
Hourly's default configuration including comments can be seen here.
</summary>

```yaml
{! hourly/cli/conf/hourly.yaml !}
```
</details>

Each of these can be overridden at runtime. For example,

`hourly commit.clock=in vis=null report.timesheet=False`

This will update the WorkLog.md file and commit a clock-in message without visualizing or printing the timesheet.

!!! note
    `hourly-in` is just syntactic sugar for `hourly commit.clock=in vis=null report.timesheet=False`.

But if we want to override hourly's defaults without typing them in each time,
we can specify an hourly.yaml file in our git repo. Hourly will look
for this file (via the `config_override` option) and override its default configuration.

!!! note
    Settings in your project's `config_override` can still be overriden by command line arguments.

An example of a custom override file is found in the top-level of the hourly repo:

```yaml
{! hourly.yaml !}
```

A common use case would be permanently overriding the filename of the work_log you are committing against, to avoid
merge conflicts if multiple developers are working on the same project.

