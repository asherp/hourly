import git

import pandas as pd


def get_work_commits(repo_addr, ascending = True, tz = 'US/Eastern'):
    """Retrives work commits from repo"""
    repo = git.Repo(repo_addr)

    commits = list(repo.iter_commits())

    logs = [(c.authored_datetime, c.message, str(c)) for c in repo.iter_commits()]

    work = pd.DataFrame.from_records(logs, columns = ['time', 'message', 'hash'])

    work.time = pd.DatetimeIndex([pd.Timestamp(i).tz_convert(tz) for i in work.time])
    work.set_index('time', inplace = True)
    return work.sort_index(ascending = ascending)




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



def get_labor(work, 
            start_date = None, 
            end_date = None, 
            errant_clocks = [], 
            ignore = None, 
            case_sensitive = False, 
            verbose = True, 
            tz = None,
            return_hashes = False):
    clocked = commit_filter(work[~work.hash.isin(errant_clocks)], 'clock', case_sensitive = case_sensitive)
    if start_date is None:
        start_date = clocked.index[0]
    else:
        start_date = pd.to_datetime(start_date)
    if end_date is None:
        end_date = clocked.index[-1]
    else:
        end_date = pd.to_datetime(end_date)
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
        
    if return_hashes:
        return labor
    else:
        return labor.drop('hash', axis = 1)

def get_earnings(labor, wage = 80, currency = 'usd'):
    dt = labor.TimeDelta.sum()
    hours = dt.total_seconds()/3600.
    print("{}, {} hours worked".format(dt, hours))
    print("{0:.2f} {1}".format(round(hours*wage,2), currency))
    return round(hours*wage,2) #usd

