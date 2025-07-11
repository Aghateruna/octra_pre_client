import asyncio, json, base64, re, time
from cli import mk, snd, session, sk, pub, μ, addr, ld

# Load wallet
if not ld():
    print("❌ Wallet tidak ditemukan atau tidak valid.")
    exit(1)

# Load recipients
recipients = []
with open("recipients.txt") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2 and re.match(r'^oct[1-9A-HJ-NP-Za-km-z]{44}$', parts[0]):
            recipients.append((parts[0], parts[1]))

if not recipients:
    print("❌ recipients.txt kosong atau format salah.")
    exit(1)

# Input nonce awal
starting_nonce = int(input("📝 Masukkan nonce awal: "))

async def send_bulk():
    nonce = starting_nonce
    print(f"\n🚀 Mulai kirim ke {len(recipients)} alamat, mulai dari nonce {nonce}\n")

    for i, (to_addr, amount_str) in enumerate(recipients):
        try:
            amount = float(amount_str)
            tx, _ = mk(to_addr.strip(), amount, nonce)
            success, tx_hash, _, res = await snd(tx)
            if success:
                print(f"[{i+1}] ✅ Terkirim ke {to_addr} [{amount}] OCT | {tx_hash}")
                nonce += 1
            else:
                print(f"[{i+1}] ❌ Gagal kirim ke {to_addr} | {res or 'unknown error'}")
        except Exception as e:
            print(f"[{i+1}] ❌ Exception kirim ke {to_addr}: {e}")

    # ✅ Tutup session aiohttp
    if session:
        await session.close()

# Jalankan
asyncio.run(send_bulk())
