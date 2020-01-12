""""
This module handles the following:

* configures hourly to work with Stripe
* generates stripe invoices
"""


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