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

