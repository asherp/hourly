# WorkLog.md

When you clock in or out of a repo, `hourly` updates update a work log, determined by the `work_log.filename` parameter. By default, hourly searches for `WorkLog.md` in the top level of your repo. Hourly inserts a clock in/out header with the current time stamp at the top of the file. In addition, `hourly commit.message=my message` will update the work log with your message and commit it along with any other files added with the `git add <my changes>`. The work log can (and should!) be edited to include any supporting documentation for the work session. Thus, the `WorkLog.md` file serves a dual purpose:

1. It provides a human-readable account of work session details
2. It ensures there is always a file to commit against

Note that work sessions should be documented even if there are no committed code changes, such as meetings or any other work related to the repo.

### Collaborative Development

While simple and convenient for solo projects, there may be merge conflicts if multiple people are updating the same WorkLog. 
There are at least two ways to work around this:

1. Use the `work_log.filename` option to specify an alternate log file (e.g. `MyWorkLog.md`) in which to store your session details.
2. Delete your `WorkLog.md` before merging. Hourly can still generate a timesheet even if the `WorkLog.md` is missing.

!!! note
    Git keeps the history of your branch's WorkLog after deletion. Recover with `git log --all --full-history -- "**/WorkLog.*"`


### MkDocs 

Currently, the WorkLog is assumed to be in the top level directory of the git project. In order to include work commits in your site's documentation, create a `docs/WorkLog.md` file containing the following line:


\{! WorkLog.md !\} 

Then update `mkdocs.yaml`:

```yaml
nav:
  - WorkLog.md: WorkLog.md

markdown_extensions:
  - markdown_include.include
```

For example, we can use this method to insert this site's work session details below.

## Hourly's WorkLog

{! docs/hourly-work.html !}

Individual work sessions for the hourly project are documented below. 
 
!!! note
    We have used `work_log.header_depth=3` option for clocking in/out so that H3 headers are generated

{! WorkLog.md !} 

