# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import sys, os
import json

# %%
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go

init_notebook_mode(connected=True)

import pandas as pd
import scipy

import numpy as np
import pandas as pd

from collections import defaultdict

from collections.abc import Iterable
import numpy as np
import math

import sys

# %%
from jupyter_dash import JupyterDash
import dash
from dash import dcc
from dash import html

from psidash import load_app # for production
from psidash.psidash import get_callbacks, load_conf, load_dash, load_components, assign_callbacks
import flask

from dash.exceptions import PreventUpdate

from hourly import get_work_commits, is_clocked_in, is_clocked_out

import logging
# -

from omegaconf import OmegaConf

# +
conf = load_conf('hourly-dashboard.yaml')

# app = dash.Dash(__name__, server=server) # call flask server

server = flask.Flask(__name__) # define flask app.server

conf['app']['server'] = server

app = load_dash(__name__, conf['app'], conf.get('import'))

app.layout = load_components(conf['layout'], conf.get('import'))


if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])

def dt_format(dt):
    hours, remainder = divmod(dt.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    # Formatted only for hours and minutes as requested
    return '{}h {}m {}s'.format(int(hours), math.floor(minutes), round(seconds))

# @callbacks.clock_switch
def clock_switch(url):
    work, repo = get_work_commits('.')
    
    last_in = is_clocked_in(work)
    if last_in is not None:
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        return 'Clocked in at {} ({})'.format(last_in, dt_format(time_since_in)), False

    last_out = is_clocked_out(work)
    if last_out is not None:
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        return 'Clocked out at {} ({})'.format(last_out, dt_format(time_since_out)), False

def get_triggered():
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id

# @callbacks.clock_button
def clock_button(url, clock_in_clicks, clock_out_clicks):
    button_id = get_triggered()
    work, repo = get_work_commits('.')
    last_in = is_clocked_in(work)
    last_out = is_clocked_out(work)
    clock_status = ''

    if last_in is not None:
        clock_in_label = 'Clocked in'
        clock_out_label = 'Clock Out'
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        clock_status += 'Clocked in at {} ({})'.format(last_in, dt_format(time_since_in))

    if last_out is not None:
        clock_in_label = 'Clock Out'
        clock_out_label = 'Clocked Out'
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        clock_status += 'Clocked out at {} ({})'.format(last_out, dt_format(time_since_out))
    
    if button_id == 'clock-in':
        if last_in is not None:
            clock_status += ': no need to clock in'
        else:
            clock_status += ': need to clock in'
    if button_id == 'clock-out':
        if last_out is not None:
            clock_status += ': no need to clock out'
        else:
            clock_status += ': need to clock out'
    
    return clock_status, clock_in_label, clock_out_label

# @callbacks.clock_status
def clock_status(url, n_intervals):
    work, repo = get_work_commits('.')
    last_in = is_clocked_in(work)
    if last_in is not None:
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        return 'Clocked in at {} ({})'.format(last_in, dt_format(time_since_in))
    last_out = is_clocked_out(work)
    if last_out is not None:
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        return 'Clocked out at {} ({})'.format(last_out, dt_format(time_since_out))
    
# @callbacks.update_table
def update_table(url):
    work, repo = get_work_commits('.')
    work_ = work.reset_index().iloc[::-1]
    columns = [{"name": i, "id": i} for i in work_.columns]
    data = work_.to_dict('records')
    return columns, data

import git
from hourly.cli.main import get_base_dir, get_work_commits, get_current_user, identify_user, get_clocks, get_user_work, process_commit

@callbacks.hourly_conf
def update_hourly_conf(url, clock_in_clicks, clock_out_clicks, message, git_user_name, git_user_email):
    cfg = OmegaConf.load('hourly.yaml')

    gitdir = os.path.abspath(cfg.repo.gitdir)
    gitdir = get_base_dir(gitdir)
    os.chdir(gitdir)

    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')

    current_user = git.Actor(git_user_name, git_user_email)
    print('current_user:{}'.format(current_user))
    current_user_id = identify_user(current_user, cfg)
    print(current_user_id)
    
    if 'start_date' in cfg.repo:
        start_date = pd.to_datetime(cfg.repo.start_date)
    else:
        start_date = work.index[0]

    if 'end_date' in cfg.repo:
        end_date = pd.to_datetime(cfg.repo.end_date)
    else:
        end_date = work.index[-1]  

    identifier = list(cfg.commit.identity)

    # parse work logs for clock in/out messages
    clocks = get_clocks(work, 
            start_date = start_date,
            end_date = end_date,
            errant_clocks = cfg.repo.errant_clocks,
            case_sensitive = cfg.repo.case_sensitive)
    
#     print(clocks.head())

    button_id = get_triggered()

    if button_id == 'clock-in':
        cfg.commit.clock = 'in'
    if button_id == 'clock-out':
        cfg.commit.clock = 'out'

    cfg.commit.message = message
    if ('clock' in cfg.commit) | (len(cfg.commit.get('message', '')) > 0):
        user_work = get_user_work(clocks, current_user_id, identifier)
        print(user_work.head())
        try:
            process_commit(cfg, user_work, repo)
            pass
        except IOError as error_msg:
            print("Could not process commit for {}:\n{}".format(current_user_id, error_msg))
            raise PreventUpdate
        except:
            print(get_current_user(repo))
            print(current_user_id)
            print(user_work)
            print(clocks)
            print(identifier)
            raise PreventUpdate

    last_in = is_clocked_in(work)
    last_out = is_clocked_out(work)
    clock_status = ''

    if last_in is not None:
        clock_in_label = 'Clocked in'
        clock_out_label = 'Clock Out'
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        clock_status += 'Clocked in at {} ({})'.format(last_in, dt_format(time_since_in))

    if last_out is not None:
        clock_in_label = 'Clock Out'
        clock_out_label = 'Clocked Out'
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        clock_status += 'Clocked out at {} ({})'.format(last_out, dt_format(time_since_out))
    
            
    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')
    work_ = work.reset_index().iloc[::-1]
    columns = [{"name": i, "id": i} for i in work_.columns]
    data = work_.to_dict('records')
    
    return clock_status, clock_in_label, clock_out_label, columns, data

#     return '```yaml\n{}```'.format(cfg.commit.pretty())

    

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, mode='external', debug=True)

# +
# dcc.Input?
# -

conf = OmegaConf.load('hourly-dashboard.yaml')

hourly_conf.commit.get('message', '')


