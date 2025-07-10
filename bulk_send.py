import asyncio
from cli import ld, mk, snd, st

async def send_bulk():
    if not ld():
        print("❌ Failed to load wallet.")
        return

    nonce, balance = await st()
    
    with open("recipients.txt", "r") as f:
        recipients = []
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                recipients.append((parts[0], float(parts[1])))

    for to_addr, amount in recipients:
        tx, _ = mk(to_addr, amount, nonce)
        success, txhash, delay, _ = await snd(tx)
        if success:
            print(f"✅ Sent {amount} OCT to {to_addr} in {delay:.2f}s - TX: {txhash}")
            nonce += 1
        else:
            print(f"❌ Failed to send {amount} OCT to {to_addr}: {txhash}")

asyncio.run(send_bulk())
