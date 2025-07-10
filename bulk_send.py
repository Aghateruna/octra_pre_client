import asyncio
from cli import snd

def load_wallet():
    import json
    with open("wallet.json", "r") as f:
        return json.load(f)

def load_recipients():
    with open("recipients.txt", "r") as f:
        lines = f.readlines()
        return [line.strip().split() for line in lines if line.strip()]

def build_tx(wallet, to_addr, amount):
    return {
        "priv": wallet["priv"],
        "to": to_addr,
        "amount": float(amount)
    }

def send_all():
    wallet = load_wallet()
    recipients = load_recipients()
    for to_addr, amount in recipients:
        tx = build_tx(wallet, to_addr, amount)
        result = asyncio.run(snd(tx))
        print("Hasil:", result)

if __name__ == "__main__":
    send_all()
