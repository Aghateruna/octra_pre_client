import asyncio
import json
from cli import mk, snd, st, sk, pub

μ = 1_000_000  # konversi ke satuan raw

# Load wallet.json langsung
def load_wallet():
    try:
        with open("wallet.json", "r") as f:
            data = json.load(f)
            priv = data["priv"]
            addr = data["addr"]
            return priv, addr
    except Exception as e:
        print(f"❌ Gagal load wallet.json: {e}")
        return None, None

async def send_bulk():
    priv, addr = load_wallet()
    if not priv or not addr:
        return

    try:
        with open("recipients.txt", "r") as f:
            recipients = [
                line.strip().split()
                for line in
