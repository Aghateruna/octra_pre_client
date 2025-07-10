import asyncio
import json
from cli import snd  # hanya fungsi ini yang tersedia

async def send_bulk():
    with open("recipients.txt", "r") as f:
        recipients = [line.strip().split() for line in f if line.strip()]
    
    for address, amount in recipients:
        tx = {
            "to": address,
            "amount": float(amount)
        }
        result = await snd(tx)
        print("Hasil:", result)

asyncio.run(send_bulk())
