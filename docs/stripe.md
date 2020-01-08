
## Stripe

Stripe's [one-time payment API](https://stripe.com/docs/payments/checkout/one-time) may be used to process hourly invoices. 

This allows us to generate invoices in a single command:

`hourly invoice=stripe`

### Setup

#### Step 1 - install the stripe python api:

`pip install --upgrade stripe`


#### Step 2 - Create a stripe account

You will need an account at [Stripe](https://stripe.com/). Be sure to follow the steps for a developer looking to handle one-time payments. You should also set up your [invoice template settings](https://dashboard.stripe.com/account/billing/invoice).

#### Step 3 - Set environment variables

From the Stripe [dashboard](https://dashboard.stripe.com/apikeys):

* copy the "Publishable key" and set it as an environment variable `STRIPE_API_KEY` 
* copy the "Secret key" and set it as an environment variable `STRIPE_API_SECRET_KEY`

!!! note
    You will probably want to use your `test_` API keys first!

### Generating Stripe invoices

To generate a stripe invoice for a given date range:

`hourly invoice=stripe repo.start_date="Jan 1, 2020" repo.end_date="Jan 7, 2020`

To check that invoice will work, select from one of their [testing cards](https://stripe.com/docs/testing#cards) to check that the invoice can be paid.