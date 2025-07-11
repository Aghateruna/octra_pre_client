import json
from cli import ld, mk, snd, st

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
                for line in f.readlines()
                if line.strip()
            ]
    except Exception as e:
        print(f"❌ Gagal baca recipients.txt: {e}")
        return

    nonce, _ = await st()
    if nonce is None:
        print("❌ Gagal ambil nonce.")
        return

    for to_addr, amount in recipients:
        try:
            tx, _ = mk(to_addr.strip(), float(amount.strip()), nonce)
            success, tx_hash, t, res = await snd(tx)
            print(f"Hasil kirim ke {to_addr}: ({success}, {tx_hash})")
            nonce += 1
        except Exception as e:
            print(f"❌ Gagal kirim ke {to_addr}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_bulk())
