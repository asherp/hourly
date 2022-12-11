## Freelance prototype

```python
from hourly import get_work_commits
```

```python
from hourly import get_clocks, get_labor
```

```python
work, repo = get_work_commits('..', branch='btc_plus_plus')
```

```python
clocks = get_clocks(work, start_date = "Dec 11, 2022")
clocks
```

```yaml
errant_clocks: # list of commit hashes to skip
    - d9ec537b36475b565df6b28d0cab6edc3a89f2da
    - ef37f8ad13118305776aa43d8acd2d18b0b61827
```

```python
labor = get_labor(clocks, match_logs=False, ignore = 'pro bono', return_hashes=True)
labor.tail()
```

```python
for work_index, work_session in labor.iterrows():
    print(work_session.hash, work_session.Hours)
```

## Generate private key

```python
import secp256k1
```

```python
secp256k1.PrivateKey?
```

```python
priv_key = secp256k1.PrivateKey()
```

```python
priv_key.serialize() # set this as enviornment variable
```

## Load private key


Store the above key in your local .env

```python
from dotenv import load_dotenv
```

```python
ls ../.env
```

```python
load_dotenv('../.env')
```

```python
import os
```

```python
secp256k1.PrivateKey.deserialize()
```

```python
def get_priv_key(priv_key_hex):
    """gets a private key object from a hex string"""
    priv_key_raw = secp256k1.PrivateKey().deserialize(priv_key_hex)
    return secp256k1.PrivateKey(priv_key_raw)
```

```python
priv_key = get_priv_key(os.environ['HOURLY_PRIVATE_KEY'])
```

## Generate pub key

```python
from base64 import b64encode, b64decode
```

```python
pub_key = priv_key.pubkey
pub_key
```

```python
b64encode(pub_key.serialize())
```

Save the above key to your config (in compensation)


## Load pub keys

```python
from omegaconf import OmegaConf
```

```python
conf = OmegaConf.load('../hourly.yaml')
conf
```

```python
asher_pub_key_str = conf.compensation[0]['pub_key']
asher_pub_key_str
```

```python
daniel_pub_key_str = conf.compensation[2]['pub_key']
daniel_pub_key_str
```

```python
asher_pub_key = secp256k1.PublicKey(pubkey=b64decode(asher_pub_key_str), raw=True)
```

```python
daniel_pub_key = secp256k1.PublicKey(pubkey=b64decode(daniel_pub_key_str), raw=True)
```

```python
daniel_pub_key
```

## Generate shared secret

```python
priv_key.keypair?
```

```python
priv_key.deserialize(priv_key.serialize())
```

```python
# shared_secret = daniel_pub_key.tweak_mul(priv_key.deserialize(priv_key.serialize()))
# b64encode(shared_secret.serialize())

shared_secret = asher_pub_key.tweak_mul(priv_key.deserialize(priv_key.serialize()))
b64encode(shared_secret.serialize())
```

```python

```

```python
assert pub_key.serialize() == pub_key_bytes
```

```python
import base64
```

```python
base64.decode?
```

```python
bytes(pub_key_raw.encode('utf-8'))
```

```python
pub_key_bytes = pub_key.serialize()
pub_key_bytes
```

```python
from base64 import b64encode, b64decode
```

```python
b64encode(pub_key_bytes)
```

```python
b64decode(asher_pub_key)
```

```python
!git log
```

## Asherp generating an invoice

```python
import subprocess
import json
```

```python
result = subprocess.run(["docker exec playground-lnd lncli --macaroonpath '/root/.lnd/data/chain/bitcoin/signet/admin.macaroon' addinvoice --amt=10000"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
result.stdout
```

```python
invoice = json.loads(result.stdout)["payment_request"]
invoice
```

## Daniel paying the invoice

```python
result = subprocess.run([f"docker exec playground-lnd lncli --macaroonpath '/root/.lnd/data/chain/bitcoin/signet/admin.macaroon' sendpayment --pay_req={invoice} -f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
```

```python
assert result.returncode == 0
```
