#!/usr/bin/env python3
import pandas as pd
from hourly import get_work_commits, is_clocked_in, is_clocked_out, update_log, commit_log, get_labor
from hourly import get_hours_worked, get_earnings, get_labor_range
from hourly import plot_labor, get_current_user, get_clocks
from hourly import invoice
import plotly.graph_objs as go
import plotly.offline as po
from omegaconf import OmegaConf, DictConfig
import hydra
from os import path
import sys
import logging
import copy

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


    logfile = hydra.utils.to_absolute_path(cfg.work_log.filename)

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
    hourly.yaml if it is in the current working directory
    or users can set an override config:
        config_override=path/to/myconfig.yaml
    """
    override_path = hydra.utils.to_absolute_path(cfg.config_override)
    if path.exists(override_path):
        override_conf = OmegaConf.load(override_path)
        # merge overrides first input with second
        cfg = OmegaConf.merge(cfg, override_conf)
    return cfg

def get_user_work(work, current_user, identifier):
    for user_id, user_work in work.groupby(identifier):
        if user_id == current_user:
            return user_work


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

    gitdir = hydra.utils.to_absolute_path(cfg.repo.gitdir)

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

            labor = get_labor(
                user_work.drop(['name','email'], axis = 1),
                ignore = cfg.repo.ignore.encode('ascii','ignore'), 
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

            plot_filename = hydra.utils.to_absolute_path(
                cfg.vis.plotly.plot.filename)
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
    cfg = config_override(cfg)
    cfg.report.timesheet = True
    run(cfg)

def hourly_report():
    cli_report()

if __name__ == "__main__":
    main()
