"""BTCPay interface

This module handles:

* configuration of hourly to pair with a BTCPay server,
* Generates a BTCPay client using configuration credential
* Processing of BTCPay invoices
"""

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
        print(btcpay_not_installed)
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

