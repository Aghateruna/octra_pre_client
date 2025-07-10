import json
import os
import time

# Load wallet
with open("wallet.json", "r") as f:
    wallet = json.load(f)

    priv = wallet["priv"]
    addr = wallet["addr"]
    rpc = wallet["rpc"]

    # Load recipients
    recipients = []

    with open("recipients.txt", "r", encoding="utf-8") as f:
        for line in f:
                parts = line.strip().split()
                        if len(parts) == 2:
                                    address = parts[0].strip()
                                                try:
                                                                amount = float(parts[1])
                                                                                recipients.append((address, amount))
                                                                                            except ValueError:
                                                                                                            print(f"❌ Invalid amount on line: {line.strip()}")

                                                            # Fungsi untuk kirim transaksi (dummy)
                                                            def send_transaction(to_addr, amount):
                                                                print(f"Mengirim {amount} OCT ke {to_addr} dari {addr}")
                                                                    # Tambahkan fungsi transaksi asli di sini
                                                                        time.sleep(0.5)  # delay simulasi

                                                                        # Kirim semua transaksi
                                                                        for to_addr, amount in recipients:
                                                                            send_transaction(to_addr, amount)

                                                                            print("✅ Selesai mengirim semua.")