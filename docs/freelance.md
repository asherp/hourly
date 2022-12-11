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
def get_priv_key(priv_key_hex):
    """gets a private key object from a hex string"""
    priv_key_raw = secp256k1.PrivateKey().deserialize(priv_key_hex)
    return secp256k1.PrivateKey(priv_key_raw)
```

```python
priv_key_asher = get_priv_key(os.environ['HOURLY_PRIVATE_KEY'])
```

```python
priv_key_daniel = get_priv_key(os.environ['HOURLY_PRIVATE_KEY_DANIEL'])
```

```python
get_shared_secret(priv_key_asher, priv_key_daniel.pubkey)
```

```python
get_shared_secret(priv_key_daniel, priv_key_daniel.pubkey)
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
```

```python
asher_pub_key = secp256k1.PublicKey(pubkey=b64decode(asher_pub_key_str), raw=True)
```

```python
asher_pub_key
```

```python
assert priv_key_asher.pubkey == asher_pub_key
```

```python
assert priv_key_daniel.pubkey == daniel_pub_key
```

```python
daniel_pub_key = secp256k1.PublicKey(pubkey=b64decode(daniel_pub_key_str), raw=True)
```

```python
daniel_pub_key
```

## Generate shared secret

```python
priv_key_asher
```

```python
len(priv_key.deserialize(priv_key.serialize()))
```

```python
def get_shared_secret(priv_key, pub_key):
    shared_secret =  pub_key.tweak_mul(priv_key.deserialize(priv_key.serialize()))
    return b64encode(shared_secret.serialize())[:32].decode('ascii')
```

```python
shared_secret = get_shared_secret(priv_key, daniel_pub_key)
shared_secret
```

## Encrypt with shared secret

```python
from cryptography.fernet import Fernet
```

```python
def get_fernet(key_str):
    fernet_key = base64.urlsafe_b64encode(bytes(key_str.ljust(32).encode()))
    return Fernet(fernet_key)


def encrypt(key, message):
    # Fernet(base64.urlsafe_b64encode(b'(3,4)'.ljust(32)))

    key_str = str(key)

    f = get_fernet(key_str)
    token = f.encrypt(message.encode())

    encrypted_msg = token.decode('ascii')

    return encrypted_msg


def decrypt(key, message):
    f = get_fernet(str(key))
    decrypted_msg = f.decrypt(message.encode()).decode('ascii')

    return decrypted_msg
```

```python
# shared_secret = daniel_pub_key.tweak_mul(priv_key.deserialize(priv_key.serialize()))
# b64encode(shared_secret.serialize())

shared_secret = asher_pub_key.tweak_mul(priv_key.deserialize(priv_key.serialize()))
b64encode(shared_secret.serialize())
```

```python
assert pub_key.serialize() == pub_key_bytes
```

```python
decrypt(shared_secret, encrypted)
```

```python
labor
```

```python
wage = conf.compensation[0]['wage']
wage
```

```python
unit_price = int(labor.iloc[0].Hours*wage['sats'])
```

```python
unit_price # sats earned
```

## Prototyping

```python
from secp256k1 import PrivateKey, PublicKey

privkey = PrivateKey()
privkey_der = privkey.serialize()
assert privkey.deserialize(privkey_der) == privkey.private_key

sig = privkey.ecdsa_sign(b'hello')
verified = privkey.pubkey.ecdsa_verify(b'hello', sig)
assert verified

sig_der = privkey.ecdsa_serialize(sig)
sig2 = privkey.ecdsa_deserialize(sig_der)
vrf2 = privkey.pubkey.ecdsa_verify(b'hello', sig2)
assert vrf2

pubkey = privkey.pubkey
pub = pubkey.serialize()

pubkey2 = PublicKey(pub, raw=True)
assert pubkey2.serialize() == pub
assert pubkey2.ecdsa_verify(b'hello', sig)
```

```python
priv_key1 = PrivateKey()
priv_key1.serialize()
```

```python
priv_key2 = PrivateKey()
priv_key2.serialize()
```

```python
shared_1 = priv_key1.pubkey.tweak_mul(priv_key2.deserialize(priv_key2.serialize()))
print(priv_key1.serialize())
```

```python
shared_2 = priv_key2.pubkey.tweak_mul(priv_key1.deserialize(priv_key1.serialize()))
priv_key2.serialize()
```

```python
shared_1 == shared_2
```

## Asherp generating an invoice

```python
work_session0 = labor.iloc[0]
```

```python
import subprocess
import json
```

```python
work_session0.hash
```

```python
result = subprocess.run(["docker exec playground-lnd lncli --macaroonpath '/root/.lnd/data/chain/bitcoin/signet/admin.macaroon' addinvoice --amt={unit_price}"],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
result.stdout
```

```python
payment_invoice = json.loads(result.stdout)["payment_request"]
payment_invoice
```

```python
invoice_json = json.dumps(dict(invoice=payment_invoice, clock_in=work_session0.hash, clock_out=work_session0.hash))
```

```python
invoice_json
```

```python
shared_secret
```

```python
invoice_encrypted = encrypt(shared_secret, invoice)
```

Commit the above invoice to the repo!

```python
with open('invoices/invoice1.txt')
```

## Daniel paying the invoice

```python
invoice = decrypt(shared_secret, invoice_encrypted)
```

```python
result = subprocess.run([f"docker exec playground-lnd lncli --macaroonpath '/root/.lnd/data/chain/bitcoin/signet/admin.macaroon' sendpayment --pay_req={invoice} -f"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
```

```python
result
```

```python
assert result.returncode == 0
```

```python

```
