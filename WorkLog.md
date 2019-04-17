
# 2019-04-16 23:06:17.688503: clock-in: researching payments

# 2019-04-16 01:21:50.338638: clock-out


* Looking into lightning payments https://github.com/ElementsProject/lightning-charge

# 2019-04-16 00:01:09.069912: clock-in

# 2019-04-13 02:43:19.905950: clock-out

* Looking into payment automation
* fixed an errant clock-in/out with hard reset:

	git reset --hard 590804df784c45051c548eb84e930c1157d6acc1

Where I used the last clock-out commit hash from 2019-04-12 18:04:27.744011

# 2019-04-13 02:24:44.339725: clock-in: T-45m

# 2019-04-12 18:04:27.744011: clock-out

# 2019-04-12 17:53:58.904877: clock-in: payment options

# 2019-04-12 15:45:54.653421: clock-out
* determine why report sometimes shows negative time deltas

# 2019-04-12 15:41:12.003763: clock-in

# 2019-04-11 02:48:43.722703: clock-out
# Apr 11, 2019

* Finished in/out flags

# Apr 8, 2019

* working on in/out flags

# Apr 7, 2019

* Adding "hourly in/out" flags
* Pushing python 3 version
* Looking into payment options

# Mar 15, 2019

* Fixed issue with ignore default

# Mar 14, 2019

* bug fixing

# Mar 12, 2019

* scrapping readthedocs in favor of github.io
* starting command-line interface

# Mar 11, 2019

* Trying to fix build error


# Mar 10, 2019

* Added documentation site
* Started integration with readthedocs


# Feb 25, 2019

* Added clock adjustments
* Made match_logs option to raise an error when in/out clocks don't match


# Oct 20, 2018

* Switched to pd.Timestamp to allow for easier slicing
* Added timezones
* Notebook Tutorial runs without errors


# Oct 28, 2018

* Removed line breaks from report
