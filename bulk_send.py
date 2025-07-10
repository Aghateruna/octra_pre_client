bulk_send.py

import json, asyncio from cli import send_transaction

Path ke wallet dan daftar penerima

wallet_path = "wallet.json" recipients_path = "recipients.txt"

Load wallet

with open(wallet_path, "r") as f: wallet = json.load(f)

Load recipients

with open(recipients_path, "r") as f: lines = f.readlines() recipients = [] for line in lines: parts = line.strip().split() if len(parts) == 2: recipients.append((parts[0], float(parts[1])))

Fungsi kirim satu transaksi

async def send_all(): for address, amount in recipients: print(f"Sending {amount} OCT to {address}...") await send_transaction(wallet, address, amount) await asyncio.sleep(3)  # delay agar tidak overload

Jalankan

asyncio.run(send_all())

