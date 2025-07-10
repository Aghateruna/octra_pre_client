import asyncio
import json

from cli import snd, sign, addr, priv  # Pastikan cli.py punya semua ini

with open("recipients.txt", "r") as f:
    lines = f.readlines()

recipients = []
for line in lines:
    parts = line.strip().split()
    if len(parts) == 2:
        recipients.append((parts[0], float(parts[1])))

async def send_all():
    for to_addr, amount in recipients:
        tx = {
            "from": addr,
            "to": to_addr,
            "amount": amount,
            "token": "OCT",
            "timestamp": int(time.time())
        }
        tx["sig"] = sign(tx, priv)
        result = await snd(tx)
        print("Hasil:", result)
        await asyncio.sleep(1)

asyncio.run(send_all())
