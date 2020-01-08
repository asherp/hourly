## Frequently Asked Questions

### Why do I need hourly to clock-in/out instead of `git commit -m 'clock-in'?`

That's actually how I began work on hourly - I started adding `clock-in/out` to my git
messages and figured I would eventually generate a timesheet based on that. But doing
it manually is error prone! When you use `hourly-in`, hourly first checks that you are not already 
clocked in (by checking the current git users's commit history). If you are already clocked in, hourly
will tell you when you last clocked in and exit before a problematic commit is generated. This works similarly when you clock out.


### What happens if I forgot to clock-in/out for the day?

Everyone makes mistakes. If you forgot to clock out 12 hours and 30 minutes ago, then just clock out now: `hourly-out commit.tminus=12h30m`. This will generate the following commit message:

`clock-out: T-12h30m`

Later on, when hourly generates a timesheet, it will automatically adjust the clock-out time to be 12.5 hours into the past. 

### Why can't I clock-in/out sometime in the future?

While it's easy to forget to do something, it's hard to predict when something will happen. I couldn't think of a reason to support such a feature, so I haven't.

