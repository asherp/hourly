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

```python
pub_key = priv_key.pubkey
pub_key
```

```python
pub_key.serialize()
```

```python

```

```python
!git log
```

```python

```
