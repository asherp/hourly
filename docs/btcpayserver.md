
# BTCPayServer

## Motivation

`BTCPay Server` is an open-source payment processing application for cryptocurrency.
Integration  with hourly means we can issue invoices and receive payments at 
command-line with minimal cost. You can use a third-party provider
or host it yourself - the only only difference will be the domain
name used to create the local client.

## Setup

First you will need to register and create a store on a `BTCPay server`. 
There are a few free ones [listed on the BTCPay Server website](https://docs.btcpayserver.org/deployment/thirdpartyhosting), but please use caution. 
For maximum privacy and security, you can host one yourself.

Connect a bitcoin wallet to your new store. This can be done in your store's general settings, under
`Derivation Scheme`, where you provide your wallet's `xpubkey` - BTCPay Server uses this key to generate a unique payment address for every invoice issued.

!!! warning
    A legitimate BTCPay Server should only ask for your wallet's `xpubkey` and **NEVER YOUR PRIVATE KEY**

Then you will need to install the btcpay-python client

	pip install btcpay-python

## Pairing

Follow [these pairing instructions](https://github.com/btcpayserver/btcpay-python#creating-a-client-the-manual-way-not-necessary-if-you-used-the-easy-method-above) from the kind folks at `BTCPay Server`.

!!! note
    These instructions correspond to "The manual way" - we want to be able to create a btcpay client on-demand without storing it in a database. 

I'm essentially repeating their instructions below:


### Step 1 - Get a pairing code

* On your BTCPay server, browse to Stores > Store settings > Access tokens > Create new token
* Fill in the form:
	* Label: <any string that will help you remember what this pairing is used for>
	* Public key: leave blank
* Click save and then copy the 7 digit pairing code from the success page

### Step 2 - Generate a private key

This can be done with the following code:

```python
from btcpay import crypto
privkey = crypto.generate_privkey()
```
This needs to be written down somewhere, probably set as an environment variable.

### Step 3 - Create a client

Create a client using the name of your `btcpayserver`  (e.g. https://btc.exitpay.org) and private key:

```python
client = BTCPayClient(host=host_store, pem=privkey)
```

### Step 4 - Generate a pairing token 

using the pairing code from Step 1

```python
token = client.pair_client(pairing_code)
```

**This token will be stored in your hourly-config.yaml**

### Step 5 - Recreate the client 

Whenever you like:

```python
client = BTCPayClient(
    host = host_store,
    pem = privkey,
    tokens = token,
)
```

## Generating an invoice

Assuming you have completed the steps to connect a wallet to your btcpayserver,
you should be able to run the following code to generate an invoice.

```python
new_invoice = client.create_invoice({"price": 20, "currency": "USD"})
```

Depending on how you set up your BTCPay Server, the invoice will only be valid
for a short period of time.
 
