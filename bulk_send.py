import asyncio
from cli import snd

def load_wallet():
    import json
    with open("wallet.json", "r") as f:
        return json.load(f)

def load_recipients():
    with open("recipients.txt", "r") as f:
        lines = f.readlines()
        result = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 2:
                result.append((parts[0], parts[1]))
        return result

def build_tx(wallet, to_addr, amount):
    return {
        "priv": wallet["priv"],
        "to": to_addr,
        "amount": float(amount)
    }

async def main():
    wallet = load_wallet()
    recipients = load_recipients()
    for to_addr, amount in recipients:
        tx = build_tx(wallet, to_addr, amount)
        try:
            result = await snd(tx)
            print("Hasil:", result)
        except Exception as e:
            print("Gagal:", e)

if __name__ == "__main__":
    asyncio.run(main())
