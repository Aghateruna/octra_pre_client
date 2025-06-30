import requests
import json
import base64
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder

with open("wallet.json") as f:
    wallet = json.load(f)

rpc = wallet["rpc"]
priv = wallet["priv"]
sender = wallet["addr"]

sk = SigningKey(base64.b64decode(priv))

def send_tx(to, amount):
    tx = {
        "sender": sender,
        "recipient": to,
        "amount": str(amount)
    }
    tx_bytes = json.dumps(tx).encode()
    sig = sk.sign(tx_bytes, encoder=Base64Encoder).signature.decode()
    payload = {
        "tx": tx,
        "sig": sig
    }
    r = requests.post(f"{rpc}/send", json=payload)
    return r.json()

with open("recipients.txt") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        addr, amt = line.split()
        result = send_tx(addr, amt)
        print(f"✔️ Sent {amt} to {addr} → {result}")
