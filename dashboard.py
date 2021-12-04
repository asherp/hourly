# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
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

from hourly import get_work_commits, is_clocked_in, is_clocked_out, get_labor, get_base_dir

import logging

# +

import git
from hourly.cli.main import get_base_dir, get_work_commits, get_current_user, identify_user, get_clocks, get_user_work, process_commit


# +
import os, sys
LND_DIR = os.environ.get('LND_DATADIR', '/root/.lnd')

use_test_data = 'true' in os.environ.get('USE_TEST_DATA', 'False').lower()


from collections import namedtuple
# Compiled grpc modules are located in `/grpc`
sys.path.append('/grpc')
import codecs, grpc
# See https://github.com/lightningnetwork/lnd/blob/master/docs/grpc/python.md for instructions.
import lightning_pb2 as lnrpc, lightning_pb2_grpc as lightningstub
# -

import dash_bootstrap_components as dbc
dbc.__version__

# +
macaroon = codecs.encode(open(LND_DIR+'/data/chain/bitcoin/signet/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open(LND_DIR+'/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('playground-lnd:10009', ssl_creds)
stub = lightningstub.LightningStub(channel)
# request = lnrpc.ChannelGraphRequest(include_unannounced=True)
# response = stub.DescribeGraph(request, metadata=[('macaroon', macaroon)])


request = lnrpc.Invoice(
        memo="test payment",
#         r_preimage=<bytes>,
#         r_hash=<bytes>,
        value=500,
#         value_msat=<int64>,
#         settled=<bool>,
#         creation_date=<int64>,
#         settle_date=<int64>,
#         payment_request=<string>,
#         description_hash=<bytes>,
        expiry=3600*24,
#         fallback_addr=<string>,
#         cltv_expiry=<uint64>,
#         route_hints=<array RouteHint>,
#         private=<bool>,
#         add_index=<uint64>,
#         settle_index=<uint64>,
#         amt_paid=<int64>,
#         amt_paid_sat=<int64>,
#         amt_paid_msat=<int64>,
#         state=<InvoiceState>,
#         htlcs=<array InvoiceHTLC>,
#         features=<array FeaturesEntry>,
#         is_keysend=<bool>,
#         payment_addr=<bytes>,
#         is_amp=<bool>,
#         amp_invoice_state=<array AmpInvoiceStateEntry>,
    )
response = stub.AddInvoice(request, metadata=[('macaroon', macaroon)])
response.payment_request
# -

from omegaconf import OmegaConf

import math
import time

# +
import qrcode
from qrcode.image.styledpil import StyledPilImage

import base64
from io import BytesIO
# -

import requests, shutil


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
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), math.floor(minutes), round(seconds))

def get_triggered():
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return button_id


def get_clock_status(work):
    last_in = is_clocked_in(work)
    last_out = is_clocked_out(work)
    clock_status = ''
    clock_in_label = ''
    clock_out_label = ''
    
    if last_in is not None:
        clock_in_label = 'Clocked in'
        clock_out_label = 'Clock Out'
        time_since_in = pd.datetime.now(last_in.tzinfo) - last_in
        clock_status += 'Clocked in at {}'.format(last_in) # dt_format(time_since_out)
    elif last_out is not None:
        clock_in_label = 'Clock in'
        clock_out_label = 'Clocked Out'
        time_since_out = pd.datetime.now(last_out.tzinfo) - last_out
        clock_status += 'Clocked out at {}'.format(last_out) # dt_format(time_since_out)
    else:
        print('not clocked in or out')
        raise PreventUpdate
        
    return clock_status, clock_in_label, clock_out_label

def get_btc_price(currency):
    """return current price, symbol"""
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    price = data['bpi'][currency]['rate_float']
    symbol = data['bpi'][currency]['symbol']
    return price

@callbacks.set_wage
def get_wage(currency, email):
    if None in (currency, email):
        raise PreventUpdate
    else:
        print('get_wage {}, {}'.format(currency, email))
    wage = None
    cfg = OmegaConf.load('hourly.yaml')
    placeholder = 'hourly rate ({}/hr)'.format(currency)
    currency_error = ''
    email_error = ''
    for _ in cfg.compensation:
        print('compensation for {}'.format(_['name']))
        if _['email'] == email:
            if currency in _['wage']:
                print('found currency in wage')
                wage = _['wage'][currency]
                print(wage)
                break
            else:
                available_currencies = ', '.join([c for c in _['wage']])
                currency_error = '{} not found in {}'.format(currency, available_currencies)   
                print('currency_error: ' + currency_error)
        else:
            print('{} != {}'.format(_['email'], email))
            available_users = ', '.join([u['email'] for u in cfg.compensation])
            email_error = '{} not found in {}'.format(email, available_users)
            print('email error: ' + email_error)
    if wage is None:
        return dash.no_update, \
            'could not set wage for {} ({}). {} {}'.format(
                email, currency, currency_error, email_error), \
            placeholder
    return wage, '', placeholder

    
@callbacks.invoice
def generate_invoice(selected_rows, data, rate, currency):
    # amount [sat] = rate [curr/hour] * 100e6 [sat/btc] * price [btc/curr]
    result = 0
    if selected_rows is None:
        raise PreventUpdate
    if (rate is None):
        raise PreventUpdate
    for _ in selected_rows:
        result += float(data[_]['Hours'])
    amt_in_currency = result * float(rate) 
    btc_price = get_btc_price(currency)
    amt_in_sat = math.floor(amt_in_currency * 100e6/float(btc_price))

    request = lnrpc.Invoice(
            memo="test payment",
    #         r_preimage=<bytes>,
    #         r_hash=<bytes>,
            value=amt_in_sat,
    #         value_msat=<int64>,
    #         settled=<bool>,
    #         creation_date=<int64>,
    #         settle_date=<int64>,
    #         payment_request=<string>,
    #         description_hash=<bytes>,
            expiry=3600*24,
    #         fallback_addr=<string>,
    #         cltv_expiry=<uint64>,
    #         route_hints=<array RouteHint>,
    #         private=<bool>,
    #         add_index=<uint64>,
    #         settle_index=<uint64>,
    #         amt_paid=<int64>,
    #         amt_paid_sat=<int64>,
    #         amt_paid_msat=<int64>,
    #         state=<InvoiceState>,
    #         htlcs=<array InvoiceHTLC>,
    #         features=<array FeaturesEntry>,
    #         is_keysend=<bool>,
    #         payment_addr=<bytes>,
    #         is_amp=<bool>,
    #         amp_invoice_state=<array AmpInvoiceStateEntry>,
        )
    response = stub.AddInvoice(request, metadata=[('macaroon', macaroon)])
    payment_request = response.payment_request
    
    return "{:.2f}".format(amt_in_currency), payment_request
    
    
#     return "invoice amount: {} sat payment request: {}".format(result, payment_request)

def load_image(image_url):
    filename = image_url.split('/')[-1]
    if not os.path.exists(filename):
        r = requests.get(image_url, stream = True)
        r.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return filename


@callbacks.render_invoice
def render_invoice(payment_request, size):
    if len(payment_request) == 0:
        raise PreventUpdate

    qr_image_path = None
    if len(conf['qr_logo']) > 0:
        qr_image_path = load_image(conf['qr_logo'])
    
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=size)
    qr.add_data(payment_request)
    qr_img = qr.make_image(image_factory=StyledPilImage, embeded_image_path=qr_image_path)

    buffered = BytesIO()
    qr_img.save(buffered)
    encoded_image = base64.b64encode(buffered.getvalue())
    return 'data:image/png;base64,{}'.format(encoded_image.decode('ascii'))
    

@callbacks.open_qr
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callbacks.qr_size
def modal_size(scale):
    if scale < 5:
        return 'sm'
    elif scale <= 7:
        return 'md'
    else:
        return 'lg'

@callbacks.qr_payment_text
def pass_through(payment_code):
    return payment_code

@callbacks.display_led
def update_display(label, n_interval):
    if 'in' in label:
        time_last = pd.Timestamp(label.split('at')[-1].strip())
        time_since = pd.datetime.now(time_last.tzinfo) - time_last
        return dt_format(time_since), '#40900E' # green
    else:
        return '00:00:00', '#9B9B9B' # gray
    

def get_modified(repo):
    modified = []
    for _ in repo.index.diff(None):
        modified.append(_.a_path)
    return modified

def get_staged(repo):
    staged = []
    for _ in repo.index.diff('HEAD'):
        staged.append(_.a_path)
    return staged

def get_commit_date(repo, fname):
    """last commit time"""
    commit = next(repo.iter_commits(paths=fname, max_count=1))
    return pd.datetime.fromtimestamp(commit.committed_date)

def get_modified_time(fname):
    """last save time"""
    modTimesinceEpoc = os.path.getmtime(fname)
    modified = pd.datetime.fromtimestamp(modTimesinceEpoc)
    return modified

@callbacks.files_table
def render_files(url, gitdir, n_interval):
    repo = git.Repo(gitdir, search_parent_directories=True)

    modified_files = get_modified(repo)
    commit_age = []
    commit_time = []
    modified_age = []
    modified_time = []
    for fname in modified_files:
        now = pd.datetime.now()
        
        com_time = get_commit_date(repo, fname)
        commit_time.append(com_time)
        commit_age.append(dt_format(now - com_time))
        
        mod_time = get_modified_time(fname)
        modified_time.append(mod_time)
        modified_age.append(dt_format(now - mod_time))

    modified = pd.DataFrame({
        "modified": modified_files,
        "last commit": commit_time,
        "commit age": commit_age,
        "modified time": modified_time,
        "modified age": modified_age,
    })
    
    modified_columns = [{"name": i, "id": i} for i in modified.columns]
    modified_records = modified.to_dict('records')
    
    staged_files = get_staged(repo)
    staged = pd.DataFrame(dict(
        staged = staged_files))
    staged_columns = [{"name": i, "id": i} for i in staged.columns]
    staged_records = staged.to_dict('records')

    return modified_columns, modified_records, \
            staged_columns, staged_records

@callbacks.stage_style
def stage_style(selected_rows, data):
    if selected_rows is None:
        return True, 'secondary'

    if len(selected_rows) > 0:
        return False, 'primary'
    else:
        return True, 'secondary'


@callbacks.stage_files
def stage_files(n_clicks, selected_rows, data, gitdir):
    repo = git.Repo(gitdir, search_parent_directories=True)
    button_id = get_triggered()
    if button_id == 'stage-button':
        for _ in selected_rows:
            fname = data[_]['modified']
            repo.index.add([fname])
    return []

@callbacks.unstage_style
def unstage_style(selected_rows, data):
    if selected_rows is None:
        return True, 'secondary'
    if len(selected_rows) > 0:
        return False, 'primary'
    else:
        return True, 'secondary'
    

@callbacks.commit_style
def commit_style(data, message):
    message_required = False
    message_label = 'Commit message'
    commit_disabled = True
    
    if len(data) > 0:
        commit_color = 'primary'
        if len(message) == 0:
            message_required = True     
            message_label = 'Commit message required'
        else:
            commit_disabled = False
    else:
        commit_color = 'secondary'

    
    return commit_color, message_required, message_label, commit_disabled
    
@callbacks.clear_message
def clear_message(data, message):
    if data is None:
        raise PreventUpdate

    if len(data) == 0:
        return ''
    else:
        return message
    
@callbacks.unstage_files
def unstage_files(unstage_clicks, gitdir, selected_rows, data):
    """commit or unstage files
    
    both actions should deselect all files in staged area,
    so they need to be gathered in one callback
    """
    repo = git.Repo(gitdir, search_parent_directories=True)
    button_id = get_triggered()
    
    if button_id == 'unstage-button':
        fnames = []
        for _ in selected_rows:
            fname = data[_]['staged']
            fnames.append(fname)
        repo.index.reset(paths=fnames)
    return []

@callbacks.commit
def commit(url, clock_in_clicks, clock_out_clicks, commit_clicks,
                       gitdir, message, git_user_name, git_user_email):
    
    if None in [git_user_name, git_user_email]:
        raise PreventUpdate
        
    gitdir = get_base_dir(gitdir)
    os.chdir(gitdir)
        
    cfg = OmegaConf.load('{}/{}'.format(gitdir, 'hourly.yaml'))
    cfg.work_log.bullet = '*'

    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')

    current_user = git.Actor(git_user_name, git_user_email)
        
    current_user_id = identify_user(current_user, cfg)
    
    print('current_user_id: {}'.format(current_user_id))
    
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
    if button_id == 'commit-button':
        cfg.commit.message = message
    
    if ('clock' in cfg.commit) | (len(cfg.commit.get('message', '')) > 0):
        user_work = get_user_work(clocks, current_user_id, identifier)
        print(user_work.head())
        try:
            process_commit(cfg, user_work, repo, current_user)
        except IOError as error_msg:
            print("Could not process commit for {}:\n{}".format(current_user_id, error_msg))
            raise PreventUpdate
        except:
            print('!!something wrong with Commit!!')
            raise

    
    # reloads work
    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')
    
    clocks = get_clocks(work, 
            start_date = start_date,
            end_date = end_date,
            errant_clocks = cfg.repo.errant_clocks,
            case_sensitive = cfg.repo.case_sensitive)
    
    clock_status, clock_in_label, clock_out_label = get_clock_status(clocks)
    
    
    for user_id, user_work in work.groupby(identifier):
        if user_id == current_user_id:
            break
    for user_id, user_clocks in clocks.groupby(identifier):
        if user_id == current_user_id:
            user_labor = get_labor(
                user_clocks,
                ignore = cfg.ignore, 
                match_logs = cfg.match_logs,
                case_sensitive = cfg.case_sensitive)
            break
    
    work_ = user_work.reset_index().iloc[::-1]
    work_columns = [{"name": i, "id": i} for i in work_.columns]
    work_records = work_.to_dict('records')
    
#     session_columns = [{"name": i, "id": i} for i in clocks.columns]
#     session_records = clocks.iloc[::-1].to_dict('records')

    user_labor.sort_values(by=['TimeIn'], inplace=True)
    labor_columns = [{"name": i, "id": i} for i in user_labor.columns]
    labor_records = user_labor.iloc[::-1].to_dict('records')
    
    if clock_in_label.lower() == 'clocked in':
        clock_in_color = 'secondary'
        clock_in_disabled = True
    else:
        clock_in_color = 'primary'
        clock_in_disabled = False
    
    if clock_out_label.lower() == 'clocked out':
        clock_out_color = 'secondary'
        clock_out_disabled = True
    else:
        clock_out_color = 'primary'
        clock_out_disabled = False
    
    return clock_status, clock_in_label, clock_out_label, \
            work_columns, work_records, \
            labor_columns, labor_records, \
            clock_in_color, clock_out_color, \
            clock_in_disabled, clock_out_disabled


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, mode='external', debug=True, extra_files=['hourly-dashboard.yaml'])


# -

def write_invoice(payment_request):
    with open('invoice', 'w') as f:
        f.write(payment_request)
write_invoice(payment_request)

import cryptography

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
public_key = private_key.public_key()

# +
# store private key
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('hourly_private_key.pem', 'wb') as f:
    f.write(pem)
# -

# load private key

with open("hourly_private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )
private_key

# +
# write public key
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('hourly_public_key.pem', 'wb') as f:
    f.write(pem)
# -

# load public key

with open("hourly_public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )
public_key

type(payment_request.encode())

type(str.encode(payment_request))

payment_request

# +
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

message = payment_request.encode()

encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
encrypted
# -

original_message = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
assert payment_request == original_message.decode()
print('finished invoice decryption!')

btc_price = get_btc_price('USD')
btc_price

# USD, GBP, EUR

# &euro;

100e6 # sats/btc

cfg.compensation

get_btc_price('USD')

data['bpi']['USD']
