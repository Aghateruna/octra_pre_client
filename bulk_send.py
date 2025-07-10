import asyncio
from cli import ld, mk, snd, st

async def send_bulk():
    if not ld():
        print("Gagal load wallet.")
        return

<<<<<<< Updated upstream
    try:
        with open("recipients.txt", "r") as f:
            recipients = [
                line.strip().split(",") 
                for line in f.readlines() 
                if line.strip() and "," in line
            ]
    except Exception as e:
        print(f"Gagal baca file: {e}")
        return

    nonce, _ = await st()
    if nonce is None:
        print("Gagal ambil nonce.")
        return
=======
    nonce, _ = await st()
    
    with open("recipients.txt", "r") as f:
        recipients = []
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                recipients.append((parts[0], float(parts[1])))
>>>>>>> Stashed changes

    for to_addr, amount in recipients:
        try:
            tx, _ = mk(to_addr.strip(), float(amount.strip()), nonce)
            success, tx_hash, t, res = await snd(tx)
            print(f"Hasil: ({success}, {tx_hash}, {t}, {res})")
            nonce += 1
        except Exception as e:
            print(f"Gagal kirim ke {
