
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
      <th>hash</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-10-19 23:40:41-04:00</th>
      <td>Initial commit</td>
      <td>ef5690543bfb354b9325d1fbd1f9abbafbb4d9a4</td>
    </tr>
    <tr>
      <th>2018-10-19 23:57:48-04:00</th>
      <td>clock in\n</td>
      <td>5c8f05b57b739ec525291c248ea9200651b49997</td>
    </tr>
    <tr>
      <th>2018-10-20 00:21:40-04:00</th>
      <td>preparing setup.py\n</td>
      <td>254ecdacb52fc70bc358f8d55be58df3b70c7609</td>
    </tr>
    <tr>
      <th>2018-10-20 00:39:11-04:00</th>
      <td>clock out - work done for the day\n</td>
      <td>0e33fa3d74f663f954b05dd9f30e0128ca7af162</td>
    </tr>
    <tr>
      <th>2018-10-20 01:06:08-04:00</th>
      <td>clock in - start adding requirements and examp...</td>
      <td>dc065b17337b14c2f8e0458de61e6880a338d6ae</td>
    </tr>
    <tr>
      <th>2018-10-20 01:47:01-04:00</th>
      <td>clock out\n</td>
      <td>644ad6ebf4c9015fd512ed47b858602d784d6204</td>
    </tr>
    <tr>
      <th>2018-10-20 01:47:45-04:00</th>
      <td>clock in - pro bono\n</td>
      <td>e6b5f78daa68e3731f82effccb66fd4bd14996bf</td>
    </tr>
    <tr>
      <th>2018-10-20 01:51:36-04:00</th>
      <td>clock out - pro bono\n</td>
      <td>1aff88af5e9688645966ccd15da8e1530205cfea</td>
    </tr>
    <tr>
      <th>2018-10-20 02:03:56-04:00</th>
      <td>clock in - finishing tutorial\n</td>
      <td>53bd7316e579d8582c46af09277b40fbba3a390e</td>
    </tr>
    <tr>
      <th>2018-10-20 02:11:54-04:00</th>
      <td>clock out - converted notebook for README\n</td>
      <td>d55b5718a3178ab6161f7e3a148c6561a305cd79</td>
    </tr>
    <tr>
      <th>2018-10-20 02:14:21-04:00</th>
      <td>had to clock out so notebook examples don't br...</td>
      <td>d9ec537b36475b565df6b28d0cab6edc3a89f2da</td>
    </tr>
    <tr>
      <th>2018-10-20 02:18:27-04:00</th>
      <td>fixed for rendering\n</td>
      <td>e2f8a2ca212fa9e7568618934da18a0ec7164fa3</td>
    </tr>
    <tr>
      <th>2018-10-20 02:22:56-04:00</th>
      <td>fixing requiremens that raised a security alert\n</td>
      <td>e0e71a05c6c5af1fc5515040ec75f33b71bd3b15</td>
    </tr>
    <tr>
      <th>2018-10-20 02:51:13-04:00</th>
      <td>fixed requirements, tutorial updates\n</td>
      <td>d8d87767005022c9a8e83015d40f6fb736f2b73b</td>
    </tr>
    <tr>
      <th>2018-10-20 02:57:22-04:00</th>
      <td>merging\n</td>
      <td>f5585c89612a5fac2d948ee61536fffe276f8949</td>
    </tr>
    <tr>
      <th>2018-10-20 11:53:00-04:00</th>
      <td>clock in - handling errant messages\n</td>
      <td>fa615994ba6b771594d711dea6087cc7ba0348b5</td>
    </tr>
    <tr>
      <th>2018-10-20 13:16:13-04:00</th>
      <td>clock out - converting to pd.Timestamp\n</td>
      <td>ed7aab29e43e7120428816481216198a255de8f4</td>
    </tr>
    <tr>
      <th>2018-10-20 13:47:56-04:00</th>
      <td>clock in - adding work log\n</td>
      <td>5b398037bf24cd503a7fc88c3b078913fa184f7e</td>
    </tr>
  </tbody>
</table>
</div>



```get_labor``` calculates hours worked by differencing commit timestamps and raises an error if clock in and clock out are of different lengths.

### Getting time card

```python
get_labor(work, end_date='2018-10-20 02:11:54-04:00')
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 02:11:54-04:00
    

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TimeIn</th>
      <th>log in</th>
      <th>hash</th>
      <th>TimeOut</th>
      <th>log out</th>
      <th>hash</th>
      <th>TimeDelta</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-10-19 23:57:48-04:00</td>
      <td>clock in\n</td>
      <td>5c8f05b57b739ec525291c248ea9200651b49997</td>
      <td>2018-10-20 00:39:11-04:00</td>
      <td>clock out - work done for the day\n</td>
      <td>0e33fa3d74f663f954b05dd9f30e0128ca7af162</td>
      <td>00:41:23</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-10-20 01:06:08-04:00</td>
      <td>clock in - start adding requirements and examp...</td>
      <td>dc065b17337b14c2f8e0458de61e6880a338d6ae</td>
      <td>2018-10-20 01:47:01-04:00</td>
      <td>clock out\n</td>
      <td>644ad6ebf4c9015fd512ed47b858602d784d6204</td>
      <td>00:40:53</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-10-20 01:47:45-04:00</td>
      <td>clock in - pro bono\n</td>
      <td>e6b5f78daa68e3731f82effccb66fd4bd14996bf</td>
      <td>2018-10-20 01:51:36-04:00</td>
      <td>clock out - pro bono\n</td>
      <td>1aff88af5e9688645966ccd15da8e1530205cfea</td>
      <td>00:03:51</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2018-10-20 02:03:56-04:00</td>
      <td>clock in - finishing tutorial\n</td>
      <td>53bd7316e579d8582c46af09277b40fbba3a390e</td>
      <td>2018-10-20 02:11:54-04:00</td>
      <td>clock out - converted notebook for README\n</td>
      <td>d55b5718a3178ab6161f7e3a148c6561a305cd79</td>
      <td>00:07:58</td>
    </tr>
  </tbody>
</table>
</div>



### Handling errant clock in/out messages
If you mistakenly put "clock out" in a message, hourly will interpret the message as a legitimate end time. This will likely raise an error when computing the labor. For example, there is a problematic commit in the this repo's history:


```python
problematic_commit = work[work.hash == 'd9ec537b36475b565df6b28d0cab6edc3a89f2da']
problematic_commit
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>message</th>
      <th>hash</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-10-20 02:14:21-04:00</th>
      <td>had to clock out so notebook examples don't br...</td>
      <td>d9ec537b36475b565df6b28d0cab6edc3a89f2da</td>
    </tr>
  </tbody>
</table>
</div>



When we include this in our labor calculation, we get the following error:


```python
try:
    get_labor(work, end_date = '2018-10-20 13:16:13-04:00')
except ValueError as e:
    print(e)
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 13:16:13-04:00
    In/Out logs do not match
    

We can skip this errant commit by setting ```errant_clocks```


```python
get_labor(work, end_date = '2018-10-20 13:16:13-04:00', 
          errant_clocks = ['d9ec537b36475b565df6b28d0cab6edc3a89f2da'])
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 13:16:13-04:00
    


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
    <tr>
      <th>4</th>
      <td>2018-10-20 11:53:00-04:00</td>
      <td>clock in - handling errant messages\n</td>
      <td>2018-10-20 13:16:13-04:00</td>
      <td>clock out - converting to pd.Timestamp\n</td>
      <td>01:23:13</td>
    </tr>
  </tbody>
</table>
</div>



### Filtering work session keywords

Use the "ignore" key word to skip any work you don't want to include in your invoices.


```python
labor = get_labor(work, 
            ignore = 'pro bono', 
            end_date = '2018-10-20 13:16:13-04:00',
            errant_clocks = ['d9ec537b36475b565df6b28d0cab6edc3a89f2da'])
labor
```

    pay period: 2018-10-19 23:57:48-04:00 -> 2018-10-20 13:16:13-04:00
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
    <tr>
      <th>4</th>
      <td>2018-10-20 11:53:00-04:00</td>
      <td>clock in - handling errant messages\n</td>
      <td>2018-10-20 13:16:13-04:00</td>
      <td>clock out - converting to pd.Timestamp\n</td>
      <td>01:23:13</td>
    </tr>
  </tbody>
</table>
</div>



## Get total earnings

Total earnings can be found using this function. Currency is just a string for printing, but in the future we can add unit conversion.


```python
get_earnings(labor, wage = 30, currency = 'USD')
```

    0 days 02:53:27, 2.890833333333333 hours worked
    86.72 USD
    
    86.72


