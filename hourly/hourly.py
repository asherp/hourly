import git

import pandas as pd

import click
import warnings

warnings.simplefilter("ignore")
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 800)


def adjust_time(work, dt_str = 'T-'):
    work = work.reset_index()
    adjustments = work[work.message.str.contains(dt_str)].message.str.split(dt_str, expand = True)
    if len(adjustments) > 0:
        adjustments.columns = ['message','timedelta']
        adjustments.timedelta = adjustments.timedelta.apply(pd.Timedelta)
        if dt_str == 'T-':
            work.time.update(work.loc[adjustments.index].time - adjustments.timedelta)
        else:
            raise NotImplementedError("{} not yet handled".format(dt_str))
    return work.set_index('time')

def get_work_commits(repo_addr, ascending = True, tz = 'US/Eastern', correct_times = True):
    """Retrives work commits from repo"""
    repo = git.Repo(repo_addr)

    commits = list(repo.iter_commits())

    logs = [(c.authored_datetime, c.message.strip('\n'), str(c)) for c in repo.iter_commits()]

    work = pd.DataFrame.from_records(logs, columns = ['time', 'message', 'hash'])

    work.time = pd.DatetimeIndex([pd.Timestamp(i).tz_convert(tz) for i in work.time])
    work.set_index('time', inplace = True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        work = work.sort_index(ascending = ascending)
    if correct_times:
        work = adjust_time(work)
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



def get_labor(work, 
            start_date = None, 
            end_date = None, 
            errant_clocks = [], 
            ignore = None, 
            case_sensitive = False, 
            verbose = True, 
            tz = None,
            return_hashes = False,
            match_logs = True):
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
    clock_in.rename(dict(time = 'TimeIn', message = 'LogIn'), 
                    axis = 'columns', 
                    inplace = True)
    
    clock_out = commit_filter(clocked, ['clock-out', 'clock out'], case_sensitive = case_sensitive).reset_index()
    clock_out.rename(dict(time = 'TimeOut', message = 'LogOut'),
                     axis = 'columns',
                     inplace = True)
    
    if match_logs:
        try:
            assert len(clock_in) == len(clock_out)
        except:
            raise ValueError("In/Out logs do not match: clock ins:{}, clock outs:{}".format(len(clock_in), len(clock_out)))
    else:
        if len(clock_in) == len(clock_out) + 1:
            clock_in.drop(clock_in.tail(1).index,inplace=True) # drop last rows

    
    labor = pd.concat([clock_in, clock_out], axis = 1)
    labor.dropna(inplace=True)
    labor = labor.assign(TimeDelta = labor.TimeOut - labor.TimeIn)
    
    if ignore is not None:
        if verbose:
            print('ignoring {}'.format(ignore))
        try:
            labor = commit_filter(labor, ignore, column = "LogIn", case_sensitive = case_sensitive, exclude = True)
            labor = commit_filter(labor, ignore, column = "LogOut", case_sensitive = case_sensitive, exclude = True)
        except:
            print(labor[['TimeIn', 'TimeOut']])
            raise

    if return_hashes:
        return labor
    else:
        return labor.drop('hash', axis = 1)

def get_earnings(labor, wage = 80, currency = 'usd'):
    dt = labor.TimeDelta.sum()
    hours = dt.total_seconds()/3600.
    print("{0}, {1:.2f} hours worked".format(dt, round(hours,2)))
    print("{0:.2f} {1}".format(round(hours*wage,2), currency))
    return round(hours*wage,2) #usd

def get_report(gitdir, start_date, end_date, errant_clocks, ignore, match_logs, wage, currency):
    work = get_work_commits(gitdir)
    labor = get_labor(work,
        start_date = start_date, 
        end_date = end_date, 
        errant_clocks = errant_clocks, 
        ignore = ignore, 
        match_logs = match_logs)
    earnings = get_earnings(labor, wage, currency)
    return labor, earnings

def get_labor_range(labor):
    start = labor.iloc[0].TimeIn
    end = labor.iloc[-1].TimeOut
    return start, end
   

@click.command()
@click.argument('gitdir', default = '.', type=click.Path(exists=True))
@click.option('-s', '--start-date', default = None, type = str, help = 'Date (time) to begin invoice')
@click.option('-e', '--end-date', default = None, type = str, help = 'Date (time) to end invoice')
@click.option('-o', '--outfile', default = None)
@click.option('-err', '--errant-clocks', default = None, type = str, multiple = True, help = 'hash of the commit to skip')
@click.option('-i', '--ignore', default = None, type = str, help = 'Ignore sessions by keyword such as "pro bono"')
@click.option('-work', '--print-work', is_flag=True, help = 'print the work log and exit')
@click.option('-m', '--match-logs', is_flag=True, default = False, help = 'raise an error if in/out logs do not match')
@click.option('-w', '--wage', default = 80, type = float, help = 'wage to charge (in chosen currency)')
@click.option('-c', '--curency', default = 'usd', type = str, help = 'Currency to print earnings')
def cli(gitdir, start_date, end_date, outfile, errant_clocks, ignore, print_work, match_logs, wage, currency):
    if print_work:
        work = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern', correct_times = True)
        print(work)
        exit()

    if ignore is not None:
        ignore =  ignore.encode('ascii','ignore')
    labor, earnings = get_report(gitdir, start_date, end_date, errant_clocks, ignore, match_logs, wage, currency)
    start, end = get_labor_range(labor)

    if outfile is not None:
        output_file = "{}-{}_to_{}.csv".format(outfile, start.strftime('%Y%m%d-%H%M%S'), end.strftime('%Y%m%d-%H%M%S'))
        print('writing to file {}'.format(output_file))
        labor.to_csv(output_file)
    else:
        print(labor)
