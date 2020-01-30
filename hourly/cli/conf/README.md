
# Configuration

The `hourly/cli/conf` directory sets hourly's default configuration using [Hydra's composition rules](https://hydra.cc/docs/tutorial/composition/). Options that are mutually exclusive are grouped in the same subfolder.

Defaults are given priority in ascending order:

```yaml
defaults:
  - hourly
  - payment: Null
  - invoice: Null
```

In other words, your `invoice` config overrides the `payment` config which overrides `hourly` config, such that the final configuration will be a merger of the keys and values from all of the above.

Since payment options are mutually exclusive, we group them in the payment subfolder.
Similarly, invoice parameters are mutually exclusive and are grouped in the
invoice subfolder.

This allows the user to select a payment option at runtime:

```hourly payment=btcpay invoice=btcpay```

However, they can still override any of the invoice options:

```hourly payment=btcpay invoice=btcpay invoice.price=30.00 invoice.currency=USD```