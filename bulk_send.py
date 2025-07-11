import asyncio
from cli import ld, mk, snd, st
import aiohttp

async def send_bulk():
    if not ld():
        print("❌ Gagal load wallet.")
        return

    # Baca daftar penerima
    try:
        with open("recipients.txt", "r") as f:
            recipients = [
                line.strip().split()
                for line in f if line.strip()
            ]
    except Exception as e:
        print(f"❌ Gagal baca recipients.txt: {e}")
        return

    # Ambil nonce awal
    nonce, _ = await st()
    if nonce is None:
        print("❌ Gagal ambil nonce (kemungkinan RPC down).")
        return

    print(f"✅ Mulai kirim ke {len(recipients)} alamat, mulai dari nonce {nonce}")

    for i, (to_addr, amount_str) in enumerate(recipients):
        try:
            amount = float(amount_str)
            tx, _ = mk(to_addr.strip(), amount, nonce)
            success, tx_hash, t, res = await snd(tx)
            if success:
                print(f"[{i+1}] ✅ Terkirim ke {to_addr} | {amount} OCT | tx_hash: {tx_hash}")
            else:
                print(f"[{i+1}] ❌ Gagal kirim ke {to_addr} | {res or 'unknown error'}")
            nonce += 1
        except Exception as e:
            print(f"[{i+1}] ❌ Exception kirim ke {to_addr}: {e}")

# Jalankan
asyncio.run(send_bulk())
