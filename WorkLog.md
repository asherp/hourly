### 2019-11-30 16:19:45.897554: clock-out
* embedding work graph as iframe
* changing `--plot` option to specify path/to/work-graph.html

### 2019-11-30 15:25:51.433329: clock-in

### 2019-11-30 15:07:32.727339: clock-out
* Testing header depth option

### 2019-11-30 15:05:34.680440: clock-in

### 2019-11-30 14:58:11.651795: clock-out
* updating docs
* added worklog header depth option 

### 2019-11-30 13:53:43.831968: clock-in

### 2019-10-23 22:55:48.632734: clock-out

### 2019-10-23 21:10:25.808038: clock-in

### 2019-09-19 21:47:37.949509: clock-out

* Moved time adjustment so it only applies at labor calculation, in clock commits

### 2019-09-19 21:13:46.261481: clock-in

### 2019-09-19 20:43:24.455285: clock-out
* pysat contains commits with ROCSAT-1, which breaks time adjustment

### 2019-09-19 20:33:26.659734: clock-in

### 2019-09-19 20:25:52.236443: clock-out
* testing on pysat repo

### 2019-09-19 20:18:01.673816: clock-in

### 2019-08-21 01:17:15.009128: clock-out: added plot options
* add plot output

### 2019-08-20 23:21:41.235199: clock-in

### 2019-08-14 00:30:48.962283: clock-out
* failed to fix utc error when giving only start time

### 2019-08-14 00:12:41.780463: clock-in: T-7m

### 2019-08-14 00:05:12.536012: clock-out
* Testing new output for double clock in warning

### 2019-08-14 00:04:16.778490: clock-in

### 2019-08-14 00:04:04.274688: clock-out

### 2019-08-14 00:03:57.681741: clock-in: T-1h22m

### 2019-08-13 22:40:45.276268: clock-out
* bug: negative dt when listing work for one day
* UTC bug occurs when no end date is specified
* removed default from wage option
* Got table into gui

### 2019-08-13 22:39:42.742055: clock-in

### 2019-08-07 23:51:23.947759: clock-out: T-15m
* upgrading to python 3.7
* cleaned up output for when no labor is available
* prototyping gui
* bug when date range covers different UTC offsets, which can occur during travel:

```console
2018-10-28 13:44:48-04:00                              clock in  c4e95f59dc0c8ce296a40300760ab6880...
2018-10-28 13:56:35-04:00                             clock out  f5200e718c062e828d436506286fd05e5...
2019-02-25 10:19:10-05:00                        clock in T-1hr  d7add63b4d2e3e1ca1423296aaed25d9c...
2019-02-25 12:49:51-05:00                        clock out T-5m  acfb8596317786e38177345aa25310980...
2019-03-10 22:57:58-04:00                              clock in  217ad6169fbd10efbb1e497a6cc6e4553...
2019-03-11 00:05:42-04:00  clock out - integrating with read...  297a561d5d7c57ecb641fa841d86dc5a6...
```

### 2019-08-07 22:01:03.125488: clock-in

### 2019-06-19 19:03:19.375329: clock-out

### 2019-06-19 18:11:54.185775: clock-in

### 2019-06-19 14:56:37.451578: clock-out: T-5m
* Weasyprint looks like the easiest path to generating pdfs
* Look at their [invoice](https://github.com/Kozea/WeasyPrint/tree/gh-pages/samples/invoice) example

### 2019-06-19 14:32:23.261121: clock-in

### 2019-06-13 18:36:23.538048: clock-out
* Looking at generating invoices in pdf

### 2019-06-13 18:19:19.036767: clock-in

### 2019-04-17 00:21:48.211640: clock-out

* got c-lightning server running in container on windows 10
* had to skip the -u `id -u` parameter, which means it runs as root
* have to use docker-machine ip to get the appropriate ip for the windows container
* got a few of the rest api commands to work, then ran into this:

	Starting bitcoind... waiting for cookie... waiting for RPC... Error: Error: Disk space is low!

* may need to delete ./data and start again?

### 2019-04-16 23:06:17.688503: clock-in: researching payments

### 2019-04-16 01:21:50.338638: clock-out

* Looking into lightning payments https://github.com/ElementsProject/lightning-charge

### 2019-04-16 00:01:09.069912: clock-in

### 2019-04-13 02:43:19.905950: clock-out

* Looking into payment automation
* fixed an errant clock-in/out with hard reset:

	git reset --hard 590804df784c45051c548eb84e930c1157d6acc1

Where I used the last clock-out commit hash from 2019-04-12 18:04:27.744011

### 2019-04-13 02:24:44.339725: clock-in: T-45m

### 2019-04-12 18:04:27.744011: clock-out

### 2019-04-12 17:53:58.904877: clock-in: payment options

### 2019-04-12 15:45:54.653421: clock-out
* determine why report sometimes shows negative time deltas

### 2019-04-12 15:41:12.003763: clock-in

### 2019-04-11 02:48:43.722703: clock-out
### Apr 11, 2019

* Finished in/out flags

### Apr 8, 2019

* working on in/out flags

### Apr 7, 2019

* Adding "hourly in/out" flags
* Pushing python 3 version
* Looking into payment options

### Mar 15, 2019

* Fixed issue with ignore default

### Mar 14, 2019

* bug fixing

### Mar 12, 2019

* scrapping readthedocs in favor of github.io
* starting command-line interface

### Mar 11, 2019

* Trying to fix build error


### Mar 10, 2019

* Added documentation site
* Started integration with readthedocs


### Feb 25, 2019

* Added clock adjustments
* Made match_logs option to raise an error when in/out clocks don't match


### Oct 20, 2018

* Switched to pd.Timestamp to allow for easier slicing
* Added timezones
* Notebook Tutorial runs without errors


### Oct 28, 2018

* Removed line breaks from report
