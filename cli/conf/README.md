
# Configuration

This directory sets hourly's default configuration using Hydra.

Defaults are given priority in descending order:

```yaml
defaults:
  - hourly
  - payment: Null
  - invoice: Null
```

The final configuration will be a merger of the keys
from `hourly` with those specified by `payment` and `invoice`.

Since payment options are mutually exclusive, we group them in the payment subfolder.
Similarly, invoice parameters are mutually exclusive and are grouped in the
invoice subfolder.

This allows the user to select a payment option at runtime:

```hourly payment=btcpay invoice=btcpay```

However, they can still override any of the invoice options:

```hourly payment=btcpay invoice=btcpay invoice.price=30.00 invoice.currency=USD```