import requests
import json
import base64
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder
import time
import hashlib

μ = 1_000_000

# Load wallet
with open("wallet.json") as f:
    wallet = json.load(f)

rpc = wallet["rpc"].rstrip("/")
priv = wallet["priv"]
sender = wallet["addr"]

sk = SigningKey(base64.b64decode(priv))
pub = base64.b64encode(sk.verify_key.encode()).decode()

def make_tx(to, amount, nonce):
    tx = {
        "from": sender,
        "to_": to,
        "amount": str(int(amount * μ)),
        "nonce": nonce,
        "ou": "1" if amount < 1000 else "3",
        "timestamp": time.time()
    }
    body = json.dumps(tx, separators=(",", ":"))
    sig = base64.b64encode(sk.sign(body.encode()).signature).decode()
    tx.update(signature=sig, public_key=pub)
    return tx

def send_tx(tx):
    try:
        r = requests.post(f"{rpc}/send-tx", json=tx)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except Exception as e:
        return 0, {"error": str(e)}

# Fetch nonce
def get_nonce():
    try:
        r = requests.get(f"{rpc}/balance/{sender}")
        data = r.json()
        return int(data.get("nonce", 0))
    except:
        return 0

# Load recipients
with open("recipients.txt") as f:
    lines = [l.strip() for l in f if l.strip()]

nonce = get_nonce()

for i, line in enumerate(lines):
    try:
        to, amt = line.split()
        amt = float(amt)
        tx = make_tx(to, amt, nonce + i + 1)
        status, result = send_tx(tx)

        if status == 200 and result.get("status") == "accepted":
            print(f"✅ Sent {amt} OCT to {to} → {result.get('tx_hash')}")
        else:
            print(f"❌ Failed {amt} to {to} → Status {status}, Response: {result}")
    except Exception as e:
        print(f"⚠️ Error on line {i+1}: {e}")
