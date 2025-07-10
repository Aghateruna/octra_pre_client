import asyncio
from cli import load, snd, sign, addr, priv
import json

async def main():
    if not load():
        print("Gagal memuat wallet.")
        return

    recipients = []
    with open("recipients.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                to_addr, amount = parts
                try:
                    amount = float(amount)
                    recipients.append((to_addr, amount))
                except ValueError:
                    print(f"Jumlah tidak valid: {amount}")

    for to_addr, amount in recipients:
        tx = {
            "from_addr": addr,
            "to_addr": to_addr,
            "amount": amount,
            "data": "",
        }
        tx["signature"] = sign(tx, priv)
        result = await snd(tx)
        print("Hasil:", result)

asyncio.run(main())
