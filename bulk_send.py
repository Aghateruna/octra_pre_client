import asyncio
import json
from cli import mk, snd, st

def load_wallet():
    try:
        with open("wallet.json", "r") as f:
            data = json.load(f)
            priv = data["priv"]
            addr = data["addr"]
            return priv, addr
    except Exception as e:
        print(f"[X] Gagal load wallet.json: {e}")
        return None, None

async def send_bulk():
    priv, addr = load_wallet()
    if not priv or not addr:
        return

    try:
        with open("recipients.txt", "r") as f:
            recipients = [
                line.strip().split()  # Format: octraAddress amount
                for line in f.readlines()
                if line.strip()
            ]
    except Exception as e:
        print(f"[X] Gagal baca file recipients.txt: {e}")
        return

    try:
        nonce, balance = await st()
        if nonce is None:
            print("[X] Gagal ambil nonce.")
            return
    except Exception as e:
        print(f"[X] Gagal ambil nonce: {e}")
        return

    for to_addr, amount in recipients:
        try:
            tx, _ = mk(to_addr.strip(), float(amount.strip()), nonce)
            success, tx_hash, t, res = await snd(tx)
            print(f"Hasil: {success}, tx_hash: {tx_hash}")
            nonce += 1
        except Exception as e:
            print(f"[X] Gagal kirim ke {to_addr.strip()}: {e}")

if __name__ == "__main__":
    asyncio.run(send_bulk())
