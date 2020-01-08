# Payments

Hourly can issue invoices based on your timesheets. Currently, only [BTCPay](https://btcpayserver.org/) and [Stripe](https://stripe.com/) are supported.

{! docs/stripe.md !}

## BTCPayServer

### Background

`BTCPay Server` is an open-source payment processing application for cryptocurrency.
Integration  with hourly means we can issue invoices and receive payments at 
command-line with minimal cost. You can use a third-party provider
or host it yourself - the only difference will be the domain
name used to create the local client.

### Setup

First you will need to register and create a store on a `BTCPay server`. 
There are a few free ones [listed on the BTCPay Server website](https://docs.btcpayserver.org/deployment/thirdpartyhosting), but please use caution. 
For maximum privacy and security, you can host one yourself.

Once you've chosen a server, connect a bitcoin wallet to your new store. This can be done in your store's general settings, under
`Derivation Scheme`, where you provide your wallet's `xpubkey` - BTCPay Server uses this key to generate a unique payment address for every invoice issued.

!!! warning
    A legitimate BTCPay Server should only ask for your wallet's `xpubkey` and **NEVER YOUR PRIVATE KEY**

Then you will need to install the btcpay-python client

	pip install btcpay-python

### Pairing with BTCPay server

Follow [these pairing instructions](https://github.com/btcpayserver/btcpay-python#creating-a-client-the-manual-way-not-necessary-if-you-used-the-easy-method-above) from the kind `BTCPay` developers.

!!! note
    These instructions correspond to "The manual way" - we want to be able to create a btcpay client on-demand without storing it in a database. 

I'm essentially repeating their instructions below:


#### Step 1 - Get a pairing code

* On your BTCPay server, browse to Stores > Store settings > Access tokens > Create new token
* Fill in the form:
	* Label: <any string that will help you remember what this pairing is used for>
	* Public key: leave blank
* Click save and then copy the 7 digit `pairing_code` from the success page

#### Step 2 - Generate a private key

This can be done with the following code:

```python
from btcpay import crypto
privkey = crypto.generate_privkey()

with open('btcpayserver.pem', 'w') as pem:
	pem.write(privkey)
```
Here we store the private key in a [`PEM`](https://wiki.openssl.org/index.php/Command_Line_Elliptic_Curve_Operations#EC_Private_Key_File_Formats) file. By default,
hourly will look for `btcpayserver.pem` in the top level of your git repo, 
but you can use a different name.


!!! warning
    Do not add the pem file to your git repo! List it in your .gitignore so you don't do so by accident.

#### Step 3 - Create a client

Cr#eate a client using host url of your `btcpayserver`  (e.g. https://btc.exitpay.org) and private key:

```python
client = BTCPayClient(host=host_url, pem=privkey)
```

Store your server's host url in the environment variable `BTCPAYSERVER_HOST`.

#### Step 4 - Generate a pairing token 

using the pairing code from Step 1

```python
token = client.pair_client(pairing_code)

merchant_token = token['merchant']
```

S#ave the merchant_token as an environment variable `BTCPAYSERVER_MERCHANT`

#### Step 5 - Recreate the client 

Whenever you like:

```python
client = BTCPayClient(
    host = host_store,
    pem = privkey,
    tokens = token,
)
```

#### Step 6 - Generate a test invoice

Assuming you have completed the steps to connect a wallet to your btcpayserver,
you should be able to run the following code to generate an invoice.

```python
new_invoice = client.create_invoice({"price": 20, "currency": "USD"})
print(new_invoice['url'])
```

This should give you a payment url you can email to your employer.

Depending on how you set up your BTCPay Server, the invoice will only be valid
for a short period of time (default is 15 minutes). There is a trade-off here: a short time period mitigates the risk of currency fluctuation, but requires that the employer must act quickly to pay the invoice.   
 
### Hourly configuration

Hourly creates a `BTCPayClient` through the following configuration:

```yaml
{! cli/conf/payment/btcpay.yaml !}
```

This allows hourly to access your environment variables and the `pem` file you created above.
Any of these parameters can be overridden when you run hourly. Here are some examples.

	hourly invoice=btcpay invoice.pem=<private key> 
	hourly invoice=btcpay invoice.pem=/path/to/other/btcpayserver.pem
	hourly invoice=btcpay invoice.host=https://myprivateserver.com

## Hourly Invoicing

If you configured hourly with BTCPay, you can generate an invoice for your git repo in a given date range. Here is what that looks like when applied to the hourly repo:

```console
hourly invoice=btcpay payment=btcpay repo.start_date="Jan 1, 2020" repo.end_date="Jan 6, 2020"

Processing timesheet for Asher Pembroke
pay period: 2020-01-03 18:44:04-05:00 -> 2020-01-05 18:34:41-05:00
ignoring pro bono
                     TimeIn     LogIn                email                   TimeOut     LogOut                email TimeDelta     Hours
0 2020-01-03 18:44:04-05:00  clock-in  apembroke@gmail.com 2020-01-03 20:31:57-05:00  clock-out  apembroke@gmail.com  01:47:53  1.798056
1 2020-01-03 20:45:54-05:00  clock-in  apembroke@gmail.com 2020-01-03 22:40:56-05:00  clock-out  apembroke@gmail.com  01:55:02  1.917222
2 2020-01-04 13:16:11-05:00  clock-in  apembroke@gmail.com 2020-01-04 14:01:43-05:00  clock-out  apembroke@gmail.com  00:45:32  0.758889
3 2020-01-04 14:55:18-05:00  clock-in  apembroke@gmail.com 2020-01-04 16:35:04-05:00  clock-out  apembroke@gmail.com  01:39:46  1.662778
4 2020-01-04 19:56:53-05:00  clock-in  apembroke@gmail.com 2020-01-04 21:06:20-05:00  clock-out  apembroke@gmail.com  01:09:27  1.157500
5 2020-01-04 23:59:21-05:00  clock-in  apembroke@gmail.com 2020-01-05 03:59:59-05:00  clock-out  apembroke@gmail.com  04:00:38  4.010556
6 2020-01-05 16:32:33-05:00  clock-in  apembroke@gmail.com 2020-01-05 17:03:22-05:00  clock-out  apembroke@gmail.com  00:30:49  0.513611
7 2020-01-05 17:29:01-05:00  clock-in  apembroke@gmail.com 2020-01-05 18:34:41-05:00  clock-out  apembroke@gmail.com  01:05:40  1.094444
0 days 12:54:47, 12.91 hours worked
1291.31 USD
generating invoice for current user Asher Pembroke
buyer:
  address1: null
  address2: null
  country: null
  email: null
  locality: null
  name: null
  notify: true
  phone: null
  postalCode: null
  region: null
currency: USD
extendedNotifications: true
fullNotifications: true
itemDesc: 12.91 hours worked from 2020-01-03T18:44:04-05:00 to 2020-01-05T18:34:41-05:00
notificationEmail: null
notificationURL: null
orderId: null
price: 1291.3055555555554
redirectURL: null
transactionSpeed: medium

Is this correct? (yes/n)yes
Success! Your invoice may be paid here: https://btc.exitpay.org/invoice?id=MoSbFujB7AwcrvfMN21gGC
```

Navigate to the payment url provided:

![Hourly Invoice](https://github.com/asherp/hourly/raw/master/docs/invoice_screen_shot.PNG "Hourly Invoice")
