#!/usr/bin/env python3
import pandas as pd
from hourly import get_work_commits, is_clocked_in, is_clocked_out, update_log, commit_log, get_labor
from hourly import get_hours_worked, get_earnings, get_labor_range
from hourly import plot_labor
import plotly.graph_objs as go
import plotly.offline as po
from omegaconf import OmegaConf, dictconfig
import hydra
from os import path
import sys

    
def commit_(repo, commit_message, logfile = None):
    if logfile is not None:
        repo.index.add([logfile])
    commit = repo.index.commit(commit_message)
    return commit

def process_commit(cfg, work, repo):
    """commits clock-in/out message

    If only a message is supplied, commits without clocking in/out
    """


    header_depth = '#'*cfg.work_log.header_depth

    commit_message = cfg.commit.message or ''
    log_message = ''

    if len(commit_message) > 0:
        log_message = '{} {}\n'.format(cfg.work_log.bullet, commit_message)

    if cfg.commit.clock is not None:
        tminus = cfg.commit.tminus or ''
        if len(tminus) != 0:
            commit_message = "T-{} {}".format(tminus.strip('T-'), commit_message)

        if cfg.commit.clock.lower() == 'in':
            last_in = is_clocked_in(work)
            if last_in is not None:
                print("You are still clocked in!")
                print("last clock in: {}, T-{}".format(last_in, 
                    pd.datetime.now(last_in.tzinfo) - last_in))
                sys.exit()
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
                print("You already clocked out!")
                print("last clock out: {}, T-{}".format(last_out,
                    pd.datetime.now(last_out.tzinfo) - last_out))
                sys.exit()
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

def dictConfig_to_dict(om):
    if type(om) == dictconfig.DictConfig:
        new_dict = {}
        for k,v in om.items():
            new_dict[k] = dictConfig_to_dict(v)
        return new_dict
    else:
        return om

def config_override(cfg):
    """Overrides with user-supplied configuration

    hydra_app will override its configuration using
    config.yaml if it is in the current working directory
    or users can set an override config:
        override_path=path/to/myconfig.yaml
    """
    override_path = hydra.utils.to_absolute_path(cfg.config_override)
    if path.exists(override_path):
        override_conf = OmegaConf.load(override_path)
        cfg = OmegaConf.merge(cfg, override_conf)
    return cfg


def run(cfg):
    if cfg.repo.ignore is not None:
        ignore =  cfg.repo.ignore.encode('ascii','ignore')

    gitdir = hydra.utils.to_absolute_path(cfg.repo.gitdir)

    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')
    if cfg.repo.start_date is None:
        start_date = work.index[0]
    else:
        start_date = pd.to_datetime(cfg.repo.start_date)

    if cfg.repo.end_date is None:
        end_date = work.index[-1]
    else:
        end_date = pd.to_datetime(cfg.repo.end_date)

    if cfg.report.pandas is not None:
        pd_opts = flatten_dict(dictConfig_to_dict(cfg.report.pandas)) 
        for k,v in pd_opts.items():
            pd.set_option(k,v)

    if cfg.report.work:
        print(work.loc[start_date:end_date])


    if cfg.commit is not None:
        commit = process_commit(cfg, work, repo)

    
    if cfg.report.timesheet:
        labor = get_labor(work,
            start_date = start_date, 
            end_date = end_date, 
            errant_clocks = cfg.repo.errant_clocks, 
            ignore = cfg.repo.ignore, 
            match_logs = cfg.repo.match_logs)

        if len(labor) > 0:
            print(labor)

            hours_worked = get_hours_worked(labor)
            dt = labor.TimeDelta.sum()
            print("{0}, {1:.2f} hours worked".format(dt, round(hours_worked,2)))


            if cfg.report.wage is not None:
                earnings = get_earnings(hours_worked, cfg.report.wage, cfg.report.currency)

            if cfg.report.outfile is not None:
                start, end = get_labor_range(labor)
                output_file = "{}-{}_to_{}.csv".format(
                    cfg.report.outfile,
                    start.strftime('%Y%m%d-%H%M%S'),
                    end.strftime('%Y%m%d-%H%M%S'))
                print('writing to file {}'.format(output_file))
                labor.to_csv(output_file)
        else:
            print('No data for {} to {}'.format(start_date, end_date))

    if cfg.vis is not None:
        hours_worked = get_hours_worked(labor)
        plot_title = "hours commited: {0:.2f}".format(hours_worked)
        fig = go.Figure(plot_labor(labor, cfg.vis.frequency))
        fig.update_layout(
            title = plot_title, 
            yaxis = dict(title_text = 'hours per {}'.format(cfg.vis.frequency)))

        # override figure with plotly figure kwargs
        fig.update_layout(**dictConfig_to_dict(cfg.vis.plotly.figure)) 

        # include plotly plot kwargs
        div = po.plot(fig,
            **dictConfig_to_dict(cfg.vis.plotly.plot))
        if cfg.vis.plotly.plot.output_type.lower() == 'div':
            with open(cfg.vis.plotly.plot.filename, 'w') as div_output:
                div_output.write(div)
                div_output.write('\n')

@hydra.main(config_path="hourly-config.yaml")
def main(cfg):
    cfg = config_override(cfg)
    run(cfg)

def entry():
    main()

@hydra.main(config_path="hourly-config.yaml")
def cli_in(cfg):
    cfg = config_override(cfg)
    cfg.commit.clock = 'in'
    cfg.vis = None
    cfg.report.work = False
    cfg.report.timesheet = False
    run(cfg)


def hourly_in():
    cli_in()


@hydra.main(config_path="hourly-config.yaml")
def cli_out(cfg):
    cfg = config_override(cfg)
    cfg.commit.clock = 'out'
    cfg.vis = None
    cfg.report.work = False
    cfg.report.timesheet = False
    run(cfg)

def hourly_out():
    cli_out()


if __name__ == "__main__":
    main()
