# WorkLog.md

The `hourly` command line utility will update the top-level `WorkLog.md` file when you clock in/out of a project, inserting a clock in/out header with the current time stamp at the top of the file. This file may be edited to add details about the current work sessions. The `WorkLog.md` file serves a dual purpose:

1. It provides a human-readable account of work session details
2. It ensures there is always a file to commit against

This way work sessions can be documented even if there are no committed code changes.

### Collaborative Development

While simple and convenient for solo projects, there may be merge conflicts if multiple people are updating the same WorkLog. There are two ways to work around this:

1. Use the `-log` option to specify an alternate log file (e.g. `MyWorkLog.md`) in which to store your session details.
2. Delete your `WorkLog.md` before merging. 

!!! note
    Git keeps the history of your branch's WorkLog after deletion. Recover with `git log --all --full-history -- "**/WorkLog.*"`

Because `hourly`  relies on commit timestamps, it can still generate a timesheet even if the `WorkLog.md` is missing.

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

The work sessions for the hourly project are documented below. 
 
!!! note
    We have used -d 3 option for clocking in/out so that H3 headers are generated

{! WorkLog.md !} 

