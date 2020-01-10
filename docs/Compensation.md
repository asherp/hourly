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

This has some interesting consequences, depending on who authors the configuration!


## Market signaling through compensation

`compensation` details can be made public by committing `hourly.yaml` to the master branch of your git repo. This implies that the listed developers may issue invoices for that repo and might be compensated according to the specified wage. So, if a developer is in high demand, there could be a bidding war between projects to attract that developer's attention.

Conversely, setting your own compensation is an indication of the rates you're offering (and in what currencies). This represents the supply side of a fully decentralized labor market, where "order matching" could be done through email!


## Market signaling through time

Suppose there is no compensation set in the project's `hourly.yaml` (or you are not a listed developer). There is still a benefit to using hourly: your contributions to open source projects can be measured *in hours*, thereby demonstrating the value of your time. 

!!! note
    Developers could still issue invoices for any amount, but there is no expectation that maintainers would pay (at least not publicly).

