#!/usr/bin/env python3
import pandas as pd
from hourly import get_work_commits, is_clocked_in, is_clocked_out, update_log, commit_log, get_labor
from hourly import get_hours_worked, get_earnings, get_labor_range
from hourly import plot_labor, get_current_user, get_clocks
import plotly.graph_objs as go
import plotly.offline as po
from omegaconf import OmegaConf, DictConfig
import hydra
from os import path
import sys
import decimal
import logging
import copy

    
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

    if cfg.repo.ignore is not None:
        ignore =  cfg.repo.ignore.encode('ascii','ignore')

    gitdir = hydra.utils.to_absolute_path(cfg.repo.gitdir)

    work, repo = get_work_commits(gitdir, ascending = True, tz = 'US/Eastern')

    current_user = get_current_user(repo)
    current_user_id = identify_user(current_user, cfg)

    if cfg.repo.start_date is None:
        start_date = work.index[0]
    else:
        start_date = pd.to_datetime(cfg.repo.start_date)

    if cfg.repo.end_date is None:
        end_date = work.index[-1]
    else:
        end_date = pd.to_datetime(cfg.repo.end_date)

    if cfg.report.pandas is not None:
        pd_opts = flatten_dict(
            OmegaConf.to_container(cfg.report.pandas)) 
        for k,v in pd_opts.items():
            pd.set_option(k,v)

    identifier = list(cfg.commit.identity)
    if cfg.report.work:
        for user_id, user_work in work.groupby(identifier):
            print("\nWork for {}".format(user_id))

            # handle case where start and end dates have different utc offsets
            print(user_work.loc[start_date:].loc[:end_date])

    # parse work logs for clock in/out messages
    clocks = get_clocks(work, 
            start_date = start_date,
            end_date = end_date,
            errant_clocks = cfg.repo.errant_clocks,
            case_sensitive = cfg.repo.case_sensitive)

    if cfg.commit is not None:
        if (cfg.commit.clock is not None) | len(cfg.commit.message) > 0:
            
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
                user_work.drop(identifier, axis = 1),
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
                    earnings = get_earnings(hours_worked, compensation.wage, compensation.currency)

                if cfg.report.filename is not None:
                    save_report(cfg, labor, user_id)

                if user_id == current_user_id:
                    try:
                        if cfg.stripe is not None:
                            invoice = get_stripe_invoice(
                                copy.deepcopy(cfg), # don't leak customer info!
                                labor,
                                current_user,
                                compensation)
                        elif cfg.btcpay is not None:
                            invoice = get_btcpay_invoice(
                                copy.deepcopy(cfg), # don't leak customer info! 
                                labor, 
                                current_user, 
                                compensation)
                    except IOError as m:
                        print("Could not generate invoice: {}".format(m))
                        sys.exit()
                        
                if cfg.vis is not None:
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

        if cfg.vis is not None:
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
    if len(compensation) > 0:
        for user_, comp in compensation.groupby(identifier):
            if user_ == user_id:
                return OmegaConf.create(comp.iloc[0].to_dict())


def get_btcpay_invoice(cfg, labor, current_user, compensation):
    """generates invoice from btcpay config"""
    print("Generating btcpay invoice for {}".format(current_user))
    if compensation is None:
        raise IOError("No compensation provided.")

    # make sure btcpayserver configuration takes precedence

    client = get_btcpay_client(cfg)

    hours_worked = get_hours_worked(labor)

    if cfg.btcpay.invoice.price is None:
        if compensation.wage is not None:
            # can be fractions of btc
            earnings = float(hours_worked * compensation.wage) 
        else:
            raise IOError("Must specify compensation wage or invoice.price")
        cfg.btcpay.invoice.price = earnings

    if cfg.btcpay.invoice.itemDesc is None:
        cfg.btcpay.invoice.itemDesc = get_labor_description(labor)

    if cfg.btcpay.invoice.currency is None:
        if compensation.currency is not None:
            cfg.btcpay.invoice.currency = compensation.currency
        else:
            raise IOError("Must specify invoice.currency (e.g. USD, BTC) or compensation currency")

    print(cfg.btcpay.invoice.pretty())
    user_confirms = input("Is this correct? (yes/n): ")
    if user_confirms.lower() != 'yes':
        print("Ok, try again later")
        sys.exit()

    btcpay_d = OmegaConf.to_container(cfg.btcpay.invoice)
    invoice = client.create_invoice(OmegaConf.to_container(cfg.btcpay.invoice))

    result = OmegaConf.create(invoice)

    if cfg.btcpay.return_status:
        print(result.pretty())

    return result

def get_btcpay_client(cfg):
    """Reconstruct client credentials"""

    try: 
        from btcpay import BTCPayClient
    except ImportError:
        print("You must install btcpay-python first:\n\tpip install btcpay-python")
        print("See BTCPay Server for more info:\n\thttps://btcpayserver.org/")
        print("See btcpay python api for configuration:")
        print("\thttps://bitpay.com/api/#rest-api-resources-invoices-create-an-invoice")
        sys.exit()


    # extract host, private key and merchant token
    host = cfg.btcpay.host
    pem = cfg.btcpay.pem
    tokens = dict(merchant = cfg.btcpay.tokens.merchant)

    # see if private key points to a pem file
    pem_file = hydra.utils.to_absolute_path(cfg.btcpay.pem)
    if path.exists(pem_file):
        with open(pem_file) as f:
            pem = f.read()

    client = BTCPayClient(host = host, pem = pem, tokens = tokens)
    return client


def get_labor_description(labor):
    hours_worked = get_hours_worked(labor)
    start, end = get_labor_range(labor)
    labor_description = "{:.2f} hours worked from {} to {}".format(
        round(hours_worked,2), # YYYY-MM-DDTHH:mm:ssZ
        start.isoformat(),
        end.isoformat())
    return labor_description

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




def get_stripe_invoice(cfg, labor, current_user, compensation):
    print("Generating stripe invoice for {}".format(current_user))
    try:
        import stripe
    except ImportError:
        print("You must install stripe first!\n\tpip install --upgrade stripe")
        print("See https://stripe.com/ for more info")
        sys.exit()

    if cfg.stripe.customer.email is None:
        raise IOError("stripe.customer.email required for stripe invoicing")

    logger = logging.getLogger('stripe')
    logger.setLevel(cfg.stripe.logging)

    stripe.api_key = cfg.stripe.secret_key

    if compensation is None:
        raise IOError("No compensation provided.")

    if cfg.stripe.customer_id is None:
        print("creating new customer")    
        customer = stripe.Customer.create(**cfg.stripe.customer)
        cfg.stripe.customer_id = customer['id']
        print("new customer_id: {}".format(cfg.stripe.customer_id))

    cfg.stripe.invoice_item.customer = cfg.stripe.customer_id
    cfg.stripe.invoice.customer = cfg.stripe.customer_id

    hours_worked = get_hours_worked(labor)

    if cfg.stripe.invoice_item.amount is None:
        if compensation.wage is not None:
            earnings = decimal.Decimal(hours_worked * compensation.wage)
        else:
            raise IOError("Must specify compensation wage or invoice.price")
        
        # stripe requires payment to be made in cents
        cent = decimal.Decimal('0.01')
        earnings = int(100*float(earnings.quantize(cent, rounding = decimal.ROUND_UP)))
        cfg.stripe.invoice_item.amount = earnings

    if cfg.stripe.invoice_item.description is None:
        cfg.stripe.invoice_item.description = get_labor_description(labor)

    if cfg.stripe.invoice_item.currency is None:
        if compensation.currency is not None:
            cfg.stripe.invoice_item.currency = compensation.currency
        else:
            raise IOError("Must specify stripe.invoice_item.currency " +\
                " (e.g. USD, GBP) or compensation currency")
        cfg.stripe.invoice_item.currency = cfg.stripe.invoice_item.currency.lower()

    if cfg.stripe.send_invoice:
        cfg.stripe.invoice.auto_advance = False

    print(cfg.stripe.pretty())
    user_confirms = input("Is this correct? (yes/n): ")
    if user_confirms.lower() != 'yes':
        print("Ok, try again later")
        sys.exit()

    invoice_item_d = OmegaConf.to_container(cfg.stripe.invoice_item)
    invoice_item = stripe.InvoiceItem.create(**invoice_item_d)

    invoice_d = OmegaConf.to_container(cfg.stripe.invoice)
    invoice = stripe.Invoice.create(**invoice_d)

    if cfg.stripe.send_invoice:
        result = invoice.send_invoice()
        result = OmegaConf.create(result)
    else:
        result = OmegaConf.create(invoice)

    if cfg.stripe.return_status:
        print(result.pretty())
    else:
        print("Success!")
        print("Invoice will be sent to {}".format(result.customer_email))

    if result.hosted_invoice_url is not None:
        print("Invoice may be paid at {}".format(result.hosted_invoice_url))

    print("View your invoice at https://dashboard.stripe.com")
    return result


@hydra.main(config_path="conf/config.yaml")
def main(cfg):
    cfg = config_override(cfg)
    run(cfg)

def entry():
    main()

@hydra.main(config_path="conf/config.yaml")
def cli_in(cfg):
    cfg = config_override(cfg)
    cfg.commit.clock = 'in'
    cfg.vis = None
    cfg.report.work = False
    cfg.report.timesheet = False
    run(cfg)


def hourly_in():
    cli_in()


@hydra.main(config_path="conf/config.yaml")
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
