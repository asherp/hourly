# Payments

With hourly, issuing invoices is a breeze. To issue a stripe invoice:

`hourly invoice=stripe stripe.customer.email=myclient@momandpop.com`

See the [Instructions for configuring hourly for Stripe](stripe.md).

To issue a `BTCPay` invoice connected to your BTCPay Server:

`hourly invoice=btcpay`

See the [Instructions for configuring hourly with a BTCPay server](btcpayserver.md).

Currently, only `BTCPay` and `Stripe` are supported. If you are interested
in adding support for other invoicing platforms, issue a pull request. 
If you want to sponsor development for an hourly feature, contact [Asher](about.md).

{! docs/stripe.md !}

{! docs/btcpayserver.md !}