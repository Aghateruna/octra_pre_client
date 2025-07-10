import json
import os
from cli import send_transaction  # Pastikan fungsi ini sesuai dengan implementasi di cli.py

WALLET_PATH = "wallet.json"
RECIPIENTS_FILE = "recipients.txt"

# Load wallet
with open(WALLET_PATH, "r") as f:
    wallet = json.load(f)

priv = wallet.get("priv")
addr = wallet.get("addr")
rpc = wallet.get("rpc")

# Load recipients
recipients = []
with open(RECIPIENTS_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) == 2:
                recipient_addr, amount = parts
                recipients.append((recipient_addr, float(amount)))

# Send to each recipient
for recipient_addr, amount in recipients:
    print(f"Sending {amount} OCT to {recipient_addr}...")
    try:
        tx = send_transaction(priv, addr, rpc, recipient_addr, amount)
        print("Success:", tx)
    except Exception as e:
        print("Error sending to", recipient_addr, ":", str(e))
