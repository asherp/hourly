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
    
@callbacks.clock_status
def clock_status(url, n_intervals):
    last_in = is_clocked_in(work)
    if last_in is not None:
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        return 'Clocked in at {} ({})'.format(last_in, dt_format(time_since_in))
    last_out = is_clocked_out(work)
    if last_out is not None:
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        return 'Clocked out at {} ({})'.format(last_out, dt_format(time_since_out))
    
@callbacks.update_table
def update_table(url):
    work_ = work.reset_index().iloc[::-1]
    columns = [{"name": i, "id": i} for i in work_.columns]
    data = work_.to_dict('records')
    return columns, data

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, mode='external', debug=True)
# -

flo

time_since_in.components.hours

work, repo = get_work_commits('.')
work.head()

work.tail()

dash.__version__

work.columns

# +
# work.to_dict?
# -

work.to_dict('records')


