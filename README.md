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

    git commit -m "clock in - starting work on new feature"

do stuff as usual, then clock out

    git commit -m "clock out - finished feature"


# Tutorial

We can illustrate how to use hourly on the hourly repo itself.

    git clone https://github.com/asherp/hourly.git
    cd hourly


```python
from hourly.hourly import get_work_commits, get_labor, get_earnings
```

```get_work_commits``` gathers all commits into a pandas array


```python
work = get_work_commits('.')
work
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>message</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-10-19 23:40:41-04:00</th>
      <td>Initial commit</td>
    </tr>
    <tr>
      <th>2018-10-19 23:57:48-04:00</th>
      <td>clock in\n</td>
    </tr>
    <tr>
      <th>2018-10-20 00:21:40-04:00</th>
      <td>preparing setup.py\n</td>
    </tr>
    <tr>
      <th>2018-10-20 00:39:11-04:00</th>
      <td>clock out - work done for the day\n</td>
    </tr>
    <tr>
      <th>2018-10-20 01:06:08-04:00</th>
      <td>clock in - start adding requirements and examp...</td>
    </tr>
    <tr>
      <th>2018-10-20 01:47:01-04:00</th>
      <td>clock out\n</td>
    </tr>
    <tr>
      <th>2018-10-20 01:47:45-04:00</th>
      <td>clock in - pro bono\n</td>
    </tr>
    <tr>
      <th>2018-10-20 01:51:36-04:00</th>
      <td>clock out - pro bono\n</td>
    </tr>
    <tr>
      <th>2018-10-20 02:03:56-04:00</th>
      <td>clock in - finishing tutorial\n</td>
    </tr>
    <tr>
      <th>2018-10-20 02:11:54-04:00</th>
      <td>clock out - converted notebook for README\n</td>
    </tr>
  </tbody>
</table>
</div>



```get_labor``` calculates hours worked by differencing commit timestamps. 
*Note: ```get_labor``` raises an error if clock in and clock out are of different lengths *

### Getting time card


```python
get_labor(work)
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 02:11:54-04:00
    




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TimeIn</th>
      <th>log in</th>
      <th>TimeOut</th>
      <th>log out</th>
      <th>TimeDelta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-10-19 23:57:48-04:00</td>
      <td>clock in\n</td>
      <td>2018-10-20 00:39:11-04:00</td>
      <td>clock out - work done for the day\n</td>
      <td>00:41:23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-10-20 01:06:08-04:00</td>
      <td>clock in - start adding requirements and examp...</td>
      <td>2018-10-20 01:47:01-04:00</td>
      <td>clock out\n</td>
      <td>00:40:53</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-10-20 01:47:45-04:00</td>
      <td>clock in - pro bono\n</td>
      <td>2018-10-20 01:51:36-04:00</td>
      <td>clock out - pro bono\n</td>
      <td>00:03:51</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-10-20 02:03:56-04:00</td>
      <td>clock in - finishing tutorial\n</td>
      <td>2018-10-20 02:11:54-04:00</td>
      <td>clock out - converted notebook for README\n</td>
      <td>00:07:58</td>
    </tr>
  </tbody>
</table>
</div>



### Filtering work session keywords

Use the "ignore" key word to skip any work you don't want to include in your invoices.


```python
labor = get_labor(work, ignore = 'pro bono')
labor
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 02:11:54-04:00
    ignoring pro bono
    

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TimeIn</th>
      <th>log in</th>
      <th>TimeOut</th>
      <th>log out</th>
      <th>TimeDelta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-10-19 23:57:48-04:00</td>
      <td>clock in\n</td>
      <td>2018-10-20 00:39:11-04:00</td>
      <td>clock out - work done for the day\n</td>
      <td>00:41:23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-10-20 01:06:08-04:00</td>
      <td>clock in - start adding requirements and examp...</td>
      <td>2018-10-20 01:47:01-04:00</td>
      <td>clock out\n</td>
      <td>00:40:53</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-10-20 02:03:56-04:00</td>
      <td>clock in - finishing tutorial\n</td>
      <td>2018-10-20 02:11:54-04:00</td>
      <td>clock out - converted notebook for README\n</td>
      <td>00:07:58</td>
    </tr>
  </tbody>
</table>
</div>



## Get total earnings


```python
get_earnings(labor.TimeDelta)
```

    0 days 01:30:14, 1.5038888888888888 hours worked
    120.31 usd
    




    120.31


