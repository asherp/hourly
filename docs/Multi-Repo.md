

When generating reports, `hourly` may be configured to work with multiple repositories and branches.


### Multiple branches

List trackable branches using the `repo.branch` parameter.

```yaml
repo:
	branch:
	- master
	- develop
```
 
!!! note
    `hourly-in` and `hourly-out` apply to the currently checkout out branch and are not affected by the `repo.branch` settings.


### Mutltiple repos

To configure hourly with multiple repos, add the following to your `hourly.yaml` file

```yaml
report:
  repos:
    - ${repo} # current repo's settings
    - name: "My Other Repo" # name of repo or ''
      branch: null # name(s) of branch or null for currently checked out
      gitdir: path/to/other/repo
```

Use `report.repos` to list other repos and their configurations.

### Report groupings

`report.grouping` will determine how labor will be grouped for time sheets and plotting. 
Which grouping you choose depends on your time tracking needs.

#### Labor distributed accross repos, branches, and developer

To generate reports based on committer's emails:

```yaml
report:
  grouping:
    - repo
    - branch
    - email
```

Alternatively, you may divide work based on the commiter's name:

```yaml
report:
  grouping:
    - repo
    - branch
    - email
```

!!! note
    You can also do `name` and `email` if need be.

#### Total labor across multiple repos, independent of branches and developers

Here you need only specify that work should be grouped by `repo.name`

```yaml
report:
  grouping:
    - repo
```

#### Total labor per developer, independent of repos and branches

```yaml
report:
  grouping:
    - email
    - name
```


#### Example from `hourly` repo

The hourly repo has a top-level `hourly.yaml` that demonstrates using multiple branches.

<details>
	<summary> hourly.yaml </summary>

```yaml
{! hourly.yaml !}
```
</details>




