import git

import pandas as pd

def get_work_log(rep_addr):
    repo = git.Repo(rep_addr)
    log = repo.head.log()
    times = pd.Series([l.time[0] for l in log])
    time = pd.to_datetime(times, unit = 's', origin='unix')
    messages = pd.Series([l.message for l in log])
    work = pd.DataFrame(dict(time = time, message = messages)).set_index('time')
    return work

def commit_filter(commits, filters, column = 'message', case_sensitive = False, exclude = False):
    if exclude:
        if type(filters) == str:
            return commits[~commits[column].str.contains(filters, case = case_sensitive)]
        else:
            return commits[~commits[column].str.contains('|'.join(filters), case = case_sensitive)]
    else:
        if type(filters) == str:
            return commits[commits[column].str.contains(filters, case = case_sensitive)]
        else:
            return commits[commits[column].str.contains('|'.join(filters), case = case_sensitive)]

def get_labor(work, start_date = None, end_date = None, ignore = None, case_sensitive = False, verbose = True):
    clocked = commit_filter(work, 'clock', case_sensitive = case_sensitive)
    if start_date is None:
        start_date = clocked.index[0]
    if end_date is None:
        end_date = clocked.index[-1]
    clocked = clocked.loc[start_date:end_date]
    
    if verbose:
        print('pay period: {} -> {}'.format(*clocked.index[[0,-1]]))
   
    clock_in = commit_filter(clocked, ['clock-in', 'clock in'], case_sensitive = case_sensitive).reset_index()
    clock_in.rename(dict(time = 'TimeIn', message = 'log in'), 
                    axis = 'columns', 
                    inplace = True)
    
    clock_out = commit_filter(clocked, ['clock-out', 'clock out'], case_sensitive = case_sensitive).reset_index()
    clock_out.rename(dict(time = 'TimeOut', message = 'log out'),
                     axis = 'columns',
                     inplace = True)
    
    try:
        assert len(clock_in) == len(clock_out)
    except:
        raise ValueError("In/Out logs do not match")
    
    labor = pd.concat([clock_in, clock_out], axis = 1)
    labor = labor.assign(TimeDelta = labor.TimeOut - labor.TimeIn)
    
    if ignore is not None:
        if verbose:
            print('ignoring {}'.format(ignore))
        labor = commit_filter(labor, ignore, column = "log in", case_sensitive = case_sensitive, exclude = True)
        labor = commit_filter(labor, ignore, column = "log out", case_sensitive = case_sensitive, exclude = True)
        
    
    return labor

def get_pay_usd(labor, wage = 80):
    dt = labor.sum()
    hours = dt.total_seconds()/3600.
    print("{}, {} hours worked".format(dt, hours))
    print("{} usd".format(hours*wage))
    return hours*wage #usd

def get_work_commits(repo_addr, ascending = True):
    repo = git.Repo(repo_addr)

    commits = list(repo.iter_commits())

    logs = [(c.authored_datetime, c.message) for c in repo.iter_commits()]

    work = pd.DataFrame.from_records(logs, columns = ['time', 'message']).set_index('time')
    return work.sort_index(ascending = ascending)

