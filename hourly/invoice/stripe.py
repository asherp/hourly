""""
This module handles the following:

* configures hourly to work with Stripe
* generates stripe invoices
"""
from omegaconf import OmegaConf
import logging
import sys
import decimal
from hourly.hourly import get_labor_description


def initalize_stripe(cfg):
    pass

def get_stripe_invoice(cfg, labor, current_user, earnings):
    print("Generating stripe invoice for {}".format(current_user))
    try:
        import stripe
    except ImportError:
        print("You must install stripe first!\n\tpip install --upgrade stripe")
        print("See https://stripe.com/ for more info")
        sys.exit()


    stripe_ = cfg.invoice.stripe
    if 'email' not in stripe_.customer:
        raise IOError("invoice.stripe.customer.email required for stripe invoicing")

    logger = logging.getLogger('stripe')
    logger.setLevel(cfg.invoice.stripe.logging)

    stripe.api_key = stripe_.secret_key

    if 'customer_id' not in stripe_:
        print("creating new customer")    
        customer = stripe.Customer.create(**cfg.invoice.stripe.customer)
        stripe_.customer_id = customer['id']
        print("new customer_id: {}".format(cfg.invoice.stripe.customer_id))

    stripe_.invoice_item.customer = stripe_.customer_id
    stripe_.invoice.customer = stripe_.customer_id


    if 'currency' not in stripe_.invoice_item:
        if len(earnings) > 0:
            currency = input('choose currency {}:'.format(earnings))
            if currency not in earnings:
                print('need to choose from {}'.format(tuple(earnings.keys())))
                sys.exit()
            stripe_.invoice_item.currency = currency
        else:
            raise IOError("Must specify stripe.invoice_item.currency " +\
                " (e.g. USD, GBP) or compensation currency")
        stripe_.invoice_item.currency = stripe_.invoice_item.currency.lower()


    if 'amount' not in stripe_.invoice_item:
        if len(earnings) > 0:
            earnings_ = decimal.Decimal(earnings[stripe_.invoice_item.currency])
        else:
            raise IOError("Must specify compensation wage or invoice.price")
        
        # stripe requires payment to be made in cents
        cent = decimal.Decimal('0.01')
        earnings_ = int(100*float(earnings_.quantize(cent, rounding = decimal.ROUND_UP)))
        stripe_.invoice_item.amount = earnings_

    if 'description' not in stripe_.invoice_item:
        stripe_.invoice_item.description = get_labor_description(labor)


    if stripe_.send_invoice:
        stripe_.invoice.auto_advance = False

    print(cfg.invoice.stripe.pretty())
    user_confirms = input("Is this correct? (yes/n): ")
    if user_confirms.lower() != 'yes':
        print("Ok, try again later")
        sys.exit()

    invoice_item_d = OmegaConf.to_container(cfg.invoice.stripe.invoice_item)
    invoice_item = stripe.InvoiceItem.create(**invoice_item_d)

    invoice_d = OmegaConf.to_container(cfg.invoice.stripe.invoice)
    invoice = stripe.Invoice.create(**invoice_d)

    if stripe_.send_invoice:
        result = invoice.send_invoice()
        result = OmegaConf.create(result)
    else:
        result = OmegaConf.create(invoice)

    if stripe_.return_status:
        print(result.pretty())
    else:
        print("Success!")
        print("Invoice will be sent to {}".format(result.customer_email))

    if 'hosted_invoice_url' in result:
        print("Invoice may be paid at {}".format(result.hosted_invoice_url))

    print("View your invoice at https://dashboard.stripe.com")
    return result