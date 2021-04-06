* added division of labor for multiple repo names

### 2021-04-05 22:00:06.101441: clock-in

### 2020-08-07 11:57:14.484755: clock-out

* added normalization without second axis

### 2020-08-07 11:32:29.729332: clock-in

### 2020-07-29 20:42:30.976371: clock-out

* added average time

### 2020-07-29 19:09:05.013725: clock-in: T-30m 

### 2020-07-29 17:32:59.062285: clock-out


### 2020-07-29 17:03:52.631490: clock-in

* fixed tz localize error
* fixed timedelta update again
* fixing time adjustment
### 2020-04-05 23:12:17.506294: clock-out

* got groupings to work by name or repo

### 2020-04-05 23:10:16.904078: clock-in: T-30m 

### 2020-04-05 22:33:49.515939: clock-out: T-5h 


### 2020-04-05 17:27:29.678827: clock-in

### 2020-04-05 13:51:53.130898: clock-out

* bug fixes

### 2020-04-05 13:36:21.847920: clock-in

### 2020-04-05 13:18:53.515173: clock-out

* fixing bugs not allowing group by name

### 2020-04-05 12:06:16.000383: clock-in

### 2020-04-05 11:05:49.617937: clock-out

* grouping by name

### 2020-04-05 11:00:51.458868: clock-in

* updating multi repo docs
### 2020-04-05 00:22:24.450956: clock-out: T-10m 

* adding multi repo docs

### 2020-04-04 23:20:09.144648: clock-in

### 2020-04-04 15:12:34.630127: clock-out

* added 'report.grouping' to specify name, email, repo, branch
* got multiple branches to work
* moved cli arg override into config_override
* fixed bug preventing command line args from overriding those specified in config_override

### 2020-04-04 12:38:56.777222: clock-in

### 2020-04-01 16:50:06.390562: clock-out

* set default repo name to empty str (pandas groupby ignores `None` values)

### 2020-04-01 16:32:39.430697: clock-in

### 2020-03-29 17:00:11.285076: clock-out

* got multiple repos to render
Instead of repo.gitdir, the gitdir could be determined by the location of the hourly.yaml file.
That would allow compositions through a custom resolver:

```python
OmegaConf.register_resolver("repo", lambda cfg_file: OmegaConf.load(cfg_file).repo)
```

```yaml
repo: <conf>
report:
	repos:
		- ${repo:hourly.yaml}
		- ${repo:path/to/other/hourly.yaml}
```
Here, the resolver has to take into account user directories and relative paths

You may need to use the hydra decorator to pick up default args:
```python
hydra.main(config_path="conf/config.yaml", strict = True)
```


### 2020-03-29 14:18:59.040093: clock-in

### 2020-03-23 00:02:16.968108: clock-out

* using variable interpolation

### 2020-03-22 23:30:41.959084: clock-in

### 2020-03-21 23:01:56.800234: clock-out

* added repos option to report
* keeping repo option to specify the repo for clocking in/out

### 2020-03-21 22:16:11.776279: clock-in

### 2020-03-21 18:32:05.992784: clock-out

* we only want to clock in to the current repo and generate reports for all listed repos
* Listing multiple branches
* Using chdir for each listed repo

### 2020-03-21 17:05:31.416456: clock-in

### 2020-03-21 16:02:52.504923: clock-out


### 2020-03-21 15:48:39.355359: clock-in

### 2020-03-21 15:02:28.495820: clock-out

* The goal is to list multiple repos or branches in hourly's config.
* Hourly should be able to generate a timesheet that takes into account all listed branches/repos
* This feature will avoid cluttering a project's commit history with Hourly's metadata

### 2020-03-21 14:46:21.623353: clock-in

