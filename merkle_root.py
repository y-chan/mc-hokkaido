import binascii
from typing import List

from hash_util import sha256d

def calc_merkle_root(tx_hashes: List[str]) -> bytes:
    """
    マークルルートは、ブロックのトランザクションのハッシュを2つずつペアにして、それらを連結してハッシュ化していく。
    これを繰り返して、最終的に1つのハッシュ値を得る。
    このハッシュ値がマークルルートになる。
    """
    tx_hashes = [binascii.a2b_hex(tx_hash)[::-1] for tx_hash in tx_hashes]
    while len(tx_hashes) > 1:
        if len(tx_hashes) % 2 == 1:
            tx_hashes.append(tx_hashes[-1])
        tx_hashes = [sha256d(tx_hashes[i] + tx_hashes[i + 1]) for i in range(0, len(tx_hashes), 2)]
    return tx_hashes[0]


if __name__ == "__main__":
    # https://btc1.trezor.io/block/0000000000013b8ab2cd513b0261a14096412195a72a0c4827d229dcc7e0f7af
    tx_hashes = [
        'ef1d870d24c85b89d92ad50f4631026f585d6a34e972eaf427475e5d60acf3a3',
        'f9fc751cb7dc372406a9f8d738d5e6f8f63bab71986a39cf36ee70ee17036d07',
        'db60fb93d736894ed0b86cb92548920a3fe8310dd19b0da7ad97e48725e1e12e',
        '220ebc64e21abece964927322cba69180ed853bb187fbc6923bac7d010b9d87a',
        '71b3dbaca67e9f9189dad3617138c19725ab541ef0b49c05a94913e9f28e3f4e',
        'fe305e1ed08212d76161d853222048eea1f34af42ea0e197896a269fbf8dc2e0',
        '21d2eb195736af2a40d42107e6abd59c97eb6cffd4a5a7a7709e86590ae61987',
        'dd1fd2a6fc16404faf339881a90adbde7f4f728691ac62e8f168809cdfae1053',
        '74d681e0e03bafa802c8aa084379aa98d9fcd632ddc2ed9782b586ec87451f20'
    ]

    print(calc_merkle_root(tx_hashes)[::-1].hex())
