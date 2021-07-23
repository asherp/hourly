import git
import pandas as pd
import warnings
import plotly.graph_objs as go
import plotly.offline as po

warnings.simplefilter("ignore")
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_colwidth', 37)
pd.set_option('display.width', 600)


def adjust_time(work, dt_str = 'T-'):
    work = work.reset_index()
    adjustments = work[work.message.str.contains(dt_str)].message.str.split(dt_str, expand = True)
    if len(adjustments) > 0:
        adjustments.columns = ['message','timedelta']
        # split again to remove any extra message bets
        df = adjustments.timedelta.str.split(expand=True)
        adjustments.timedelta = df[df.columns[0]]
        adjustments.timedelta = adjustments.timedelta.apply(pd.Timedelta)
        if dt_str == 'T-':    
            # work.time.update(up_) # broken
            up_ = work.loc[adjustments.index].time - adjustments.timedelta
            work.loc[up_.index, 'time'] = up_
        else:
            raise NotImplementedError("{} not yet handled".format(dt_str))
    return work.set_index('time')

def get_work_commits(repo_addr, ascending = True, tz = 'US/Eastern', branch = None):
    """Retrives work commits from repo"""
    repo = git.Repo(repo_addr)

    logs = [(c.authored_datetime, c.message.strip('\n'), str(c), c.author.name, c.author.email) for c in repo.iter_commits(branch)]

    work = pd.DataFrame.from_records(logs, columns = ['time', 'message', 'hash', 'name', 'email'])

    work.time = pd.DatetimeIndex([pd.Timestamp(i).tz_convert(tz) for i in work.time])
    work.set_index('time', inplace = True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        work = work.sort_index(ascending = ascending)
    return work, repo

def get_current_user(repo):
    reader = repo.config_reader()
    current_user = git.Actor(
        reader.get_value('user','name'),
        reader.get_value('user','email'))
    return current_user

def commit_filter(commits, filters, column = 'message', case_sensitive = False, exclude = False):
    if exclude:
        if type(filters) == str:
            return commits[~commits[column].str.contains(filters, case = case_sensitive)]
        else:
            return commits[~commits[column].str.contains('|'.join(str(f) for f in filters), case = case_sensitive)]
    else:
        if type(filters) == str:
            return commits[commits[column].str.contains(filters, case = case_sensitive)]
        else:
            return commits[commits[column].str.contains('|'.join(filters), case = case_sensitive)]


def get_clocks(work, 
            start_date = None,
            end_date = None,
            errant_clocks = None,
            case_sensitive = False,
            adjust_clocks = True):
    """Filter work by messages conataining the word 'clock' """

    if errant_clocks is not None:
        work = work[~work.hash.isin(errant_clocks)]

    clocks = commit_filter(work, 'clock', case_sensitive = case_sensitive)

    # handle case where start and dates have different utc offsets
    clocks = clocks.loc[start_date:]
    clocks = clocks.loc[:end_date]

    if adjust_clocks:
        clocks = adjust_time(clocks)
    return clocks


def get_labor(clocked, 
            ignore = None, 
            verbose = True, 
            tz = None,
            return_hashes = False,
            match_logs = True,
            case_sensitive = False):

    if verbose:
        if len(clocked) >= 1:
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
            clock_in.drop(clock_in.tail(1).index, inplace=True) # drop last rows

    
    labor = pd.concat([clock_in[['TimeIn','LogIn']], clock_out], axis = 1)
    labor.dropna(inplace=True)
    labor = labor.assign(TimeDelta = labor.TimeOut - labor.TimeIn)
    labor = labor.assign(Hours = labor['TimeDelta'].apply(lambda x: x.total_seconds()/3600.))
    
    if ignore is not None:
        ignore = ignore.encode('ascii','ignore')
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

def get_labor_description(labor):
    hours_worked = get_hours_worked(labor)
    start, end = get_labor_range(labor)
    labor_description = "{:.2f} hours worked from {} to {}".format(
        round(hours_worked,2), # YYYY-MM-DDTHH:mm:ssZ
        start.isoformat(),
        end.isoformat())
    return labor_description

def get_hours_worked(labor):
    return labor.Hours.sum()


def get_earnings(hours, wage):
    return {currency: float(hours*wage[currency]) for currency in wage}



def get_labor_range(labor):
    start = labor.iloc[0].TimeIn
    end = labor.iloc[-1].TimeOut
    return start, end



def is_clocked_in(clocks):
    if clocks is None:
        return None

    clocked_in = clocks.message.str.contains('|'.join(['clock-in', 'clock in']), case = False).to_frame()
    if len(clocked_in) > 0:
        last_in = clocked_in.iloc[-1]
        if last_in.message == False:
            #  not currently clocked in
            return None
        else:
            # return time of last clock in
            return last_in.name
    else:
        # No previous clock ins
        return None

def is_clocked_out(clocks):
    if clocks is None:
        return None

    clocked_out = clocks.message.str.contains('|'.join(['clock-out', 'clock out']), case = False).to_frame()
    if len(clocked_out) > 0:
        last_out = clocked_out.iloc[-1]
        if last_out.message == False:
            # not currently clocked out
            return None
        else:
            #  return time of last clock out
            return last_out.name
    else:
        # No previous clock outs
        return None

def update_log(logfile, message):
    try:
        with open(logfile,'r') as contents:
            save = contents.read()

        with open(logfile,'w') as contents:
            contents.write(message)
            contents.write(save)
    except:
        with open(logfile,'w') as contents:
            contents.write(message)

def commit_log(repo, logfile, commit_message):
    repo.index.add([logfile])
    commit = repo.index.commit(commit_message)
    return commit

def plot_labor(labor, freq, name = None, norm = 1):
    tdelta = labor.set_index('TimeIn').TimeDelta.groupby(pd.Grouper(freq = freq)).sum()

    tdelta_trace = go.Scatter(
        x = pd.Series(tdelta.index),
        y = [norm*td.total_seconds()/3600. for td in tdelta],
        mode='lines',
        stackgroup = 'one',
        text = [str(td) for td in tdelta],
        name = name)
    return tdelta_trace

