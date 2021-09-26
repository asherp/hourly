#!/usr/bin/env python3
import git
import pandas as pd
from hourly import get_work_commits, is_clocked_in, is_clocked_out, update_log, commit_log, get_labor
from hourly import get_hours_worked, get_earnings, get_labor_range
from hourly import plot_labor, get_current_user, get_clocks
from hourly import invoice
import plotly.graph_objs as go
import plotly.offline as po
from omegaconf import OmegaConf, DictConfig, ListConfig
import hydra
from os import path
import os
import sys
import logging
import copy
import numpy as np
import datetime

def handle_errors(cfg, error_msg = None):
    if error_msg is not None:
        print(error_msg)
    if cfg.handle_errors == 'exit':
        sys.exit()
    else:
        raise
    
def commit_(repo, commit_message, logfile = None):
    if logfile is not None:
        repo.index.add([logfile])
    commit = repo.index.commit(commit_message)
    return commit

def identify_user(user, cfg):
    user_id = []
    for id_type in cfg.commit.identity:
        if id_type in ['name', 'email']:
            user_id.append(getattr(user, id_type))
    if len(user_id) > 1:
        return tuple(user_id)
    else:
        return user_id[0]


def process_commit(cfg, work, repo):
    """commits clock-in/out message

    If only a message is supplied, commits without clocking in/out
    """

    header_depth = '#'*cfg.work_log.header_depth

    commit_message = cfg.commit.message or ''
    log_message = ''

    if len(commit_message) > 0:
        log_message = '{} {}\n'.format(cfg.work_log.bullet, commit_message)

    if 'clock' in cfg.commit:
        if cfg.commit.clock is not None:
            tminus = cfg.commit.tminus or ''
            if len(tminus) != 0:
                commit_message = "T-{} {}".format(tminus.strip('T-'), commit_message)

            if cfg.commit.clock.lower() == 'in':
                last_in = is_clocked_in(work)
                if last_in is not None:
                    time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
                    raise IOError(
                        "You are still clocked in!\n" + \
                        "\tlast clock in: {}  ({:.2f} hours ago)".format(
                            last_in,
                            time_since_in.total_seconds()/3600.))
                else:
                    if len(commit_message) == 0:
                        commit_message = "clock-in"
                    else:
                        commit_message = "clock-in: {}".format(commit_message)
                    log_message = "\n{} {}: {}\n\n".format(
                        header_depth, 
                        pd.datetime.now(), 
                        commit_message)
                    print("clocking in with message: {} ".format(commit_message))

            elif cfg.commit.clock.lower() == 'out': # prevent clock in and out at the same time
                last_out = is_clocked_out(work)
                if last_out is not None:
                    time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
                    raise IOError(
                        "You already clocked out!\n" + \
                        "\tlast clock out: {} ({:.2f} hours ago)".format(
                            last_out,
                            time_since_out.total_seconds()/3600.))
                else:
                    if len(commit_message) == 0:
                        commit_message = "clock-out"
                    else:
                        commit_message = "clock-out: {}".format(commit_message)
                    log_message = "{} {}: {}\n\n".format(
                        header_depth,
                        pd.datetime.now(),
                        commit_message)
                    print("clocking out with message: {} ".format(commit_message))
            else:
                raise IOError("unrecocgnized clock value: {}".format(cfg.commit.clock))


    # logfile = hydra.utils.to_absolute_path(cfg.work_log.filename)
    logfile = os.path.abspath(cfg.work_log.filename)

    if len(log_message) > 0:
        update_log(logfile, log_message)
        return commit_(repo, commit_message, logfile)

def flatten_dict(d, sep = '.'):
    '''flattens a dictionary into list of 
    
    courtesy of MYGz https://stackoverflow.com/a/41801708
    returns [{k.sub_key:v},...]
    '''
    
    return pd.io.json.json_normalize(d, sep=sep).to_dict(orient='records')[0]


def config_override(cfg):
    """Overrides with user-supplied configuration

    hourly will override its configuration using
    hourly.yaml if it is in the base git directory
    or users can set an override config:
        config_override=path/to/myconfig.yaml
    """
    # change to the git directory of the original working dir
    original_path = hydra.utils.get_original_cwd()
    change_git_dir(original_path, verbosity = cfg.verbosity)

    # get the full path of the override file if available
    override_path = os.path.abspath(cfg.config_override)

    if path.exists(override_path):
        if cfg.verbosity > 0:
            print("overriding config with {}".format(override_path))
        override_conf = OmegaConf.load(override_path)
        # merge overrides first input with second
        cfg = OmegaConf.merge(cfg, override_conf)
    else:
        if cfg.verbosity > 0:
            print("override path does not exist: {}".format(override_path))

    # merge in command line arguments
    cli_conf = OmegaConf.from_cli()
    cfg = OmegaConf.merge(cfg, cli_conf)

    return cfg

def get_user_work(work, current_user, identifier):
    for user_id, user_work in work.groupby(identifier):
        if user_id == current_user:
            return user_work

def resolve(cfg):
    """Expands a configuration, interpolating variables"""
    cfg_dict = cfg.to_container(resolve = True)
    return OmegaConf.create(cfg_dict)


def localize(t):
    if t is None:
        return t
    if t.tzinfo is None:
        LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo
        return t.tz_localize(LOCAL_TIMEZONE)
    else:
        return t

def get_avg_time(cfg, labor, total_hours):

    tdelta = labor.set_index('TimeIn').TimeDelta.groupby(pd.Grouper(freq = cfg.vis.frequency)).sum()
    
    tmin = tdelta.index.min()
    tmax = tdelta.index.max()

    time_range_sec = (tmax - tmin).total_seconds()
    if cfg.verbosity:
        print('freq: {}'.format(cfg.vis.frequency))
        print('time range [sec]: {}'.format(time_range_sec))
    bin_size_val, bin_size_unit = cfg.vis.frequency.split(' ')
    bin_size = pd.Timedelta(float(bin_size_val), unit = bin_size_unit)
    bin_size_sec = bin_size.total_seconds()
    if cfg.verbosity:
        print('bin size : {} [sec]: {}'.format(bin_size, bin_size_sec))
    time_bins = (time_range_sec/bin_size_sec) + 1
    avg_time = total_hours/time_bins
    if cfg.verbosity:
        print('hours: {} bins: {} average time: {}'.format(total_hours, time_bins, avg_time))
    return avg_time, tmin, tmax


def divide_labor(cfg, labor):
    """divides labor among multiple repo names"""
    rows = []
    for _, row in labor.iterrows():
        if isinstance(row.repo, tuple):
            if cfg.verbosity > 1:
                print("!!!!!!!Found multiple names {} !!!!!!".format(row.repo))
            #  divide evenly among the tags
            tag_count = len(row.repo)
            row_tag = row
            row_tag.TimeDelta = row.TimeDelta/tag_count
            row_tag.Hours = row.Hours/tag_count
            for repo_name in row.repo:
                row_tag.repo = repo_name
                rows.append(pd.DataFrame(row_tag).T)
                if cfg.verbosity > 1:
                    print('  appending {}'.format(repo_name))
        else:
            if cfg.verbosity > 1:
                print('appending {}'.format(row.repo))
            rows.append(pd.DataFrame(row).T)
    return pd.concat(rows)

def run_report(cfg):
    if cfg.verbosity > 1:
        print(cfg.pretty())

    repos = resolve(cfg.report.repos)

    if 'start_date' in cfg.repo:
        start_date = pd.to_datetime(cfg.repo.start_date)
        start_date = localize(start_date)
    else:
        start_date = None
        

    if 'end_date' in cfg.repo:
        end_date = pd.to_datetime(cfg.repo.end_date)
        end_date = localize(end_date)
    else:
        end_date = None

    if 'pandas' in cfg.report:
        pd_opts = flatten_dict(
            OmegaConf.to_container(cfg.report.pandas)) 
        for k,v in pd_opts.items():
            pd.set_option(k,v)

    clocks = pd.DataFrame()

    if type(cfg.commit.identity) is str:
        identifier = [cfg.commit.identity]
    else:
        identifier = cfg.commit.identity.to_container()

    labor = pd.DataFrame()

    for repo_conf in repos:
        gitdir = get_base_dir(repo_conf.gitdir)

        # get list of branches
        if repo_conf.branch is not None:
            if type(repo_conf.branch) is str:
                branches = [repo_conf.branch]
            else:
                branches = repo_conf.branch.to_container()
        else:
            branches = [None]
    
        work = []
        for branch in branches:
            if cfg.verbosity > 0:
                print("getting commits for repo:branch {}:{}".format(gitdir, branch))

            branch_work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern', branch = branch)
            if branch is None:
                branch_name = ''
            else:
                branch_name = branch
            print('assigning branch name {}'.format(branch_name))
            branch_work = branch_work.assign(branch = branch_name)
            if cfg.verbosity > 0:
                print("{} work commits found".format(len(branch_work)))
            print(branch_work.head())
            work.append(branch_work.sort_index())

        work = pd.concat(work)
        print('available work columns:', work.columns)

        if cfg.verbosity > 1:
            print('removing duplicates by hash')

        work.drop_duplicates('hash', inplace=True)

        print('unique branches:', work['branch'].unique())
    
        try:
            clocks = get_clocks(work,
                    start_date = start_date,
                    end_date = end_date,
                    errant_clocks = repo_conf.errant_clocks,
                    case_sensitive = repo_conf.case_sensitive)  
        except:
            print('issue with repo: {}'.format(gitdir))
            print('start_date: {}'.format(start_date))
            print('end_date: {}'.format(end_date))
            raise



        # clocks = clocks.assign(repo = repo_conf.name)
        # allow repo name to be a list
        if isinstance(repo_conf.name, ListConfig):
            clocks = clocks.assign(repo = [tuple(repo_conf.name)]*len(clocks))
        else:
            clocks = clocks.assign(repo=repo_conf.name)
        clocks.sort_index(inplace=True)
        clocks = clocks.loc[start_date:].loc[:end_date]

        print('clock columns:{}'.format(clocks.columns))  

        # id_dict = dict(repo = repo_conf.name, branch = branch)


        for user_id, user_work in clocks.groupby(identifier):
            # if type(user_id) is tuple:
            #     for i, identifier_ in enumerate(identifier):
            #         id_dict[identifier_] = user_id[i]
            # else:
            #     id_dict[identifier[0]] = user_id

    

            print(user_work.head())

            if cfg.report.work:
                print("\nWork for {}".format(user_id))
                print(user_work.drop(['name', 'email'], axis = 1))

            user_labor = get_labor(
                user_work,
                ignore = repo_conf.ignore, 
                match_logs = repo_conf.match_logs,
                case_sensitive = repo_conf.case_sensitive)


            labor = pd.concat((labor, user_labor))

    if 'filename' in cfg.report:
        # ToDo: replace 'total' prefix with user ids
        save_report(cfg, labor, 'total')

    if type(cfg.report.grouping) is str:
        report_grouping = [cfg.report.grouping]
    else:
        report_grouping = cfg.report.grouping.to_container()

    hours = []
    plot_traces = []

    print('labor columns!', labor.columns)
    print(report_grouping)
    print(labor.head())

    print('unique branches', labor.branch.unique())

    labor = divide_labor(cfg, labor)

    for labor_id, labor_ in labor.groupby(report_grouping):
        hours_worked = get_hours_worked(labor_)
        dt = labor_.TimeDelta.sum()
        print("{0}: {1} sessions, {2}, {3:.2f} hours worked".format(labor_id, len(labor_), dt, round(hours_worked,2)))

        hours.append(hours_worked)

        # # move this down
        # if 'vis' in cfg:
        #     if type(labor_id) == tuple:
        #         plot_label = "<br>".join(labor_id)
        #     else:
        #         plot_label = labor_id

        #     labor_trace = plot_labor(
        #         labor_,
        #         cfg.vis.frequency,
        #         name = plot_label)
        #     plot_traces.append(labor_trace)



    if 'vis' in cfg:
        total_hours = sum(hours)
        avg_time, tmin, tmax = get_avg_time(cfg, labor, total_hours)

        if cfg.vis.normalize:
            norm = cfg.vis.normalize/avg_time # norm > 1 if avg_time < normalization
            if cfg.verbosity:
                print('normalization factor: {}'.format(norm))
        else:
            norm = 1    

        for labor_id, labor_ in labor.groupby(report_grouping):
            if type(labor_id) == tuple:
                try:
                    plot_label = "<br>".join(labor_id)
                except:
                    raise NameError('something wrong with {}'.format(labor_id))
            else:
                plot_label = labor_id

            labor_trace = plot_labor(
                labor_,
                cfg.vis.frequency,
                name = plot_label,
                norm = norm)
            plot_traces.append(labor_trace)


        plot_title = "total hours commited: {0:.2f}".format(total_hours*norm)
        plot_traces = [plot_traces[i] for i in np.argsort(hours)[::-1]]
        fig = go.Figure(plot_traces)

        
        avg_x = pd.date_range(start = tmin, end = tmax, freq = cfg.vis.frequency)


        avg_trace = go.Scatter(
            x = avg_x,
            y = len(avg_x)*[avg_time*norm],
            mode = 'lines',
            name="average",
            text= 2*['{0:.2f}'.format(avg_time)],
            # yaxis="y2",
            )

        fig.add_trace(avg_trace)


        fig.update_layout(
            title = plot_title, 
            yaxis = dict(title_text = 'hours per {}'.format(cfg.vis.frequency)))

        # override figure with plotly figure kwargs
        fig.update_layout(**OmegaConf.to_container(cfg.vis.plotly.figure)) 

        # plot_filename = hydra.utils.to_absolute_path(
        #     cfg.vis.plotly.plot.filename)
        plot_filename = os.path.abspath(cfg.vis.plotly.plot.filename)
        plot_options = OmegaConf.to_container(cfg.vis.plotly.plot)
        plot_options['filename'] = plot_filename
        # include plotly plot kwargs
        div = po.plot(fig, **plot_options)
        if cfg.vis.plotly.plot.output_type.lower() == 'div':
            with open(plot_filename, 'w') as div_output:
                div_output.write(div)
                div_output.write('\n')



def run(cfg):
    if cfg.verbosity > 1:
        print(cfg.pretty())
    if cfg.init:
        if 'invoice' in cfg:
            if 'btcpay' in cfg.invoice:
                from hourly.invoice.btcpay import initialize_btcpay
                initialize_btcpay(cfg)
                sys.exit()
            # elif cfg.invoice.stripe is not None:
            #     from hourly.invoice.stripe import initalize_stripe
            #     initalize_stripe(cfg)
            #     sys.exit()
            else:
                print('No method to initialize this invoice type')
                print(cfg.invoice.pretty())
                sys.exit()
        else:
            print('no invoice set to initialize')
            print('options are:\n\tinvoice=stripe\n\tinvoice=btcpay')
            sys.exit()

    
    gitdir = os.path.abspath(cfg.repo.gitdir)
    gitdir = get_base_dir(gitdir)
    os.chdir(gitdir)

    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')

    current_user = get_current_user(repo)
    current_user_id = identify_user(current_user, cfg)

    if 'start_date' in cfg.repo:
        start_date = pd.to_datetime(cfg.repo.start_date)
    else:
        start_date = work.index[0]
        

    if 'end_date' in cfg.repo:
        end_date = pd.to_datetime(cfg.repo.end_date)
    else:
        end_date = work.index[-1]  

    if 'pandas' in cfg.report:
        pd_opts = flatten_dict(
            OmegaConf.to_container(cfg.report.pandas)) 
        for k,v in pd_opts.items():
            pd.set_option(k,v)

    identifier = list(cfg.commit.identity)
    if cfg.report.work:
        try:
            for user_id, user_work in work.groupby(identifier):
                print("\nWork for {}".format(user_id))

                # handle case where start and end dates have different utc offsets
                print(user_work.drop(['name', 'email'], axis = 1).loc[start_date:].loc[:end_date])
        except KeyError as m:
            print(m)
            print(work.columns)
            sys.exit()
            raise

    # parse work logs for clock in/out messages
    clocks = get_clocks(work, 
            start_date = start_date,
            end_date = end_date,
            errant_clocks = cfg.repo.errant_clocks,
            case_sensitive = cfg.repo.case_sensitive)

    if 'commit' in cfg:
        if ('clock' in cfg.commit) | (len(cfg.commit.message) > 0):
            
            user_work = get_user_work(clocks, current_user_id, identifier)
            try:
                process_commit(cfg, user_work, repo)
            except IOError as error_msg:
                print("Could not process commit for {}:\n{}".format(current_user_id, error_msg))
                sys.exit()
            except:
                print(get_current_user(repo))
                print(current_user_id)
                print(user_work)
                print(clocks)
                print(identifier)
                raise


    if cfg.report.timesheet:
        total_hours = 0
        plot_traces = []
        for user_id, user_work in clocks.groupby(identifier):
            print("\nProcessing timesheet for {}".format(user_id))
            if cfg.repo.ignore is not None:
                ignore = cfg.repo.ignore.encode('ascii','ignore')
            labor = get_labor(
                user_work.drop(['name','email'], axis = 1),
                ignore = cfg.repo.ignore, 
                match_logs = cfg.repo.match_logs,
                case_sensitive = cfg.repo.case_sensitive)

            if len(labor) > 0:
                print(labor)

                hours_worked = get_hours_worked(labor)
                dt = labor.TimeDelta.sum()
                print("{0}, {1:.2f} hours worked".format(dt, round(hours_worked,2)))

                total_hours += hours_worked

                compensation = get_compensation(cfg, identifier, user_id)

                if compensation is not None:
                    # should return {'currency': earnings} dictionary
                    # this way, preferred currency is communicated by relative price!
                    earnings = get_earnings(hours_worked, compensation.wage) 
                    print(pd.Series(earnings).to_string())

                if 'filename' in cfg.report:
                    save_report(cfg, labor, user_id)

                if user_id == current_user_id:
                    print('current user:{}'.format(user_id))
                    if 'invoice' in cfg:
                        if cfg.verbosity > 0:
                            print('processing your invoice')
                        try:
                            if 'stripe' in cfg.invoice:
                                if cfg.verbosity > 0:
                                    print('creating stripe invoice')
                                from hourly.invoice.stripe import get_stripe_invoice
                                invoice = get_stripe_invoice(
                                    copy.deepcopy(cfg), # don't leak customer info!
                                    labor,
                                    current_user,
                                    earnings)
                            elif 'btcpay' in cfg.invoice:
                                if cfg.verbosity > 0:
                                    print('creating btcpay invoice')
                                from hourly.invoice.btcpay import get_btcpay_invoice
                                invoice = get_btcpay_invoice(
                                    copy.deepcopy(cfg), # don't leak customer info! 
                                    labor, 
                                    current_user, 
                                    earnings)
                            else:
                                print('hourly cannot process this invoice type yet:')
                                print(cfg.invoice.pretty())
                        except IOError as m:
                            print("Could not generate invoice: {}".format(m))
                            sys.exit()
                else:
                    print("{} is not the current user".format(user_id))
                        
                if 'vis' in cfg:
                    if type(user_id) == tuple:
                        plot_label = "<br>".join(user_id)
                    else:
                        plot_label = user_id

                    user_trace = plot_labor(
                        labor,
                        cfg.vis.frequency,
                        name = plot_label)
                    plot_traces.append(user_trace)
            else:
                print('No data for {} to {}'.format(start_date, end_date))

        if 'vis' in cfg:
            plot_title = "total hours commited: {0:.2f}".format(total_hours)
            fig = go.Figure(plot_traces)
            fig.update_layout(
                title = plot_title, 
                yaxis = dict(title_text = 'hours per {}'.format(cfg.vis.frequency)))

            # override figure with plotly figure kwargs
            fig.update_layout(**OmegaConf.to_container(cfg.vis.plotly.figure)) 

            # plot_filename = hydra.utils.to_absolute_path(
            #     cfg.vis.plotly.plot.filename)
            plot_filename = os.path.abspath(cfg.vis.plotly.plot.filename)
            plot_options = OmegaConf.to_container(cfg.vis.plotly.plot)
            plot_options['filename'] = plot_filename
            # include plotly plot kwargs
            div = po.plot(fig, **plot_options)
            if cfg.vis.plotly.plot.output_type.lower() == 'div':
                with open(plot_filename, 'w') as div_output:
                    div_output.write(div)
                    div_output.write('\n')



def get_compensation(cfg, identifier, user_id):
    compensation = pd.DataFrame(OmegaConf.to_container(cfg.compensation))
    if cfg.verbosity > 0:
        print("Compensation for {}".format(user_id))
        print(compensation)
    if len(compensation) > 0:
        try:
            for user_, comp in compensation.groupby(identifier):
                if user_ == user_id:
                    return OmegaConf.create(comp.iloc[0].to_dict())
        except KeyError:
            error_msg = "Problem getting compensation:"
            error_msg += "identifiers: {}\n".format(identifier)
            error_msg += "compensation: {}".format(compensation)
            handle_errors(cfg, error_msg)


def save_report(cfg, labor, user_id):
    start, end = get_labor_range(labor)
    if type(user_id) == tuple:
        user_filename = '.'.join(user_id)
    else:
        user_filename = user_id
    output_file = "{}-{}-{}_to_{}.csv".format(
        cfg.report.filename,
        user_filename,
        start.strftime('%Y%m%d-%H%M%S'),
        end.strftime('%Y%m%d-%H%M%S'))
    print('writing to file {}'.format(output_file))
    labor.to_csv(output_file)

def get_base_dir(directory = '.'):
    """obtain the base directory of the git repo"""
    user_dir = os.path.expanduser(directory)
    repo = git.Repo(user_dir, search_parent_directories=True)
    base_dir = repo.working_tree_dir
    return base_dir

def change_git_dir(directory, verbosity = 0):
    '''changes to base path of git directory'''
    gitdir = get_base_dir(directory)
    if verbosity > 0:
        print("changing to git directory: {}".format(gitdir))
    os.chdir(gitdir)


@hydra.main(config_path="conf/config.yaml", strict = True)
def main(cfg):
    cfg = config_override(cfg)
    run(cfg)

def entry():
    main()

@hydra.main(config_path="conf/config.yaml", strict = True)
def cli_in(cfg):
    cfg = config_override(cfg)
    cfg.commit.clock = 'in'
    cfg.vis = None
    cfg.report.work = False
    cfg.report.timesheet = False
    run(cfg)


def hourly_in():
    cli_in()


@hydra.main(config_path="conf/config.yaml", strict = True)
def cli_out(cfg):
    cfg = config_override(cfg)

    cfg.commit.clock = 'out'
    cfg.vis = None
    cfg.report.work = False
    cfg.report.timesheet = False
    run(cfg)

def hourly_out():
    cli_out()


@hydra.main(config_path="conf/config.yaml", strict = True)
def cli_report(cfg):

    # apply custom override
    cfg = config_override(cfg)

    cfg.report.timesheet = True
    run_report(cfg)

def hourly_report():
    cli_report()

if __name__ == "__main__":
    main()
