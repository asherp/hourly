# Compensation

Hourly can be configured to assign developers' compensation on an indvidual basis:

```yaml
compensation:
  - name: Satoshi Nakamoto
    email: satoshi@vistomail.com
    wage: 75
    currency: BTC
    pubkey: <pubkey>
```

!!! note
    Hourly does not yet support public key signatures, but developers could include a signature in `invoice.itemDesc`

This creates some interesting consequences, depending on who authors the configuration.

## If compensation is public

Developer `compensation` can be made public by committing `hourly.yaml` to the master branch of your git repo. This implies that the listed developers:

1. may issue invoices for that repo
2. may be compensated according to the specified wage

As a consequence, if the developer is in high demand, there could be a bidding war between projects to attract that developer's attention.

## If compensation is private

Suppose there is no compensation set in the project's `hourly.yaml` (or you are not listed). Developers could issue invoices for any amount, but there is no expectation that maintainers would pay. However, there is still a benefit to using hourly!

1. Your contributions to open source projects can be measured in hours
2. It demonstrates how valuable your time on their project is, even if they haven't paid you!


