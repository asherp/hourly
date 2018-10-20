

```python
%load_ext autoreload

%autoreload 2
```

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
from hourly.hourly import get_work_commits, get_labor, get_pay_usd
```

```get_work_commits``` gathers all commits into a pandas array


```python
work = get_work_commits('.')
work
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
  </tbody>
</table>
</div>



```get_labor``` calculates hours worked by differencing commit timestamps. 
*Note: ```get_labor``` raises an error if clock in and clock out are of different lengths *

### Getting time card


```python
get_labor(work)
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 02:03:56-04:00
    


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    ~\Documents\Projects\hourly\hourly\hourly.py in get_labor(work, start_date, end_date, ignore, case_sensitive, verbose)
         47     try:
    ---> 48         assert len(clock_in) == len(clock_out)
         49     except:
    

    AssertionError: 

    
    During handling of the above exception, another exception occurred:
    

    ValueError                                Traceback (most recent call last)

    <ipython-input-4-798babb3f913> in <module>
    ----> 1 get_labor(work)
    

    ~\Documents\Projects\hourly\hourly\hourly.py in get_labor(work, start_date, end_date, ignore, case_sensitive, verbose)
         48         assert len(clock_in) == len(clock_out)
         49     except:
    ---> 50         raise ValueError("In/Out logs do not match")
         51 
         52     labor = pd.concat([clock_in, clock_out], axis = 1)
    

    ValueError: In/Out logs do not match


### Filtering work session keywords

Use the "ignore" key word to skip any work you don't want to include in your invoices.


```python
get_labor(work, ignore = 'pro bono')
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 02:03:56-04:00
    


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-26-7e529657d9fe> in <module>()
    ----> 1 get_labor(work, ignore = 'pro bono')
    

    C:\Users\Asher\Documents\Projects\hourly\hourly\hourly.py in get_labor(work, start_date, end_date, ignore, case_sensitive, verbose)
         48         assert len(clock_in) == len(clock_out)
         49     except:
    ---> 50         raise ValueError("In/Out logs do not match")
         51 
         52     labor = pd.concat([clock_in, clock_out], axis = 1)
    

    ValueError: In/Out logs do not match



```python

```
