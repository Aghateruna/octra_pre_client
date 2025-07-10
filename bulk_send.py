import asyncio
import json
import os
from cli import snd, sign  # load tidak perlu

# Baca wallet
wallet_path = os.path.expanduser("~/.octra/wallet.json")
if not os.path.exists(wallet_path):
    wallet_path = "wallet.json"

with open(wallet_path, "r") as f:
    wallet = json.load(f)

priv = wallet["priv"]
addr = wallet["addr"]

# Baca daftar penerima
recipients = []
with open("recipients.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            recipients.append((parts[0], float(parts[1])))

# Kirim transaksi satu per satu
async def send_all():
    for to_addr, amount in recipients:
        tx = {
            "from": addr,
            "to": to_addr,
            "amount": amount,
        }
        sign(tx, priv)
        result = await snd(tx)
        print("Hasil:", result)

asyncio.run(send_all())
