import binascii
import json

from dataclasses import dataclass
from hash_util import sha256d


@dataclass
class Block:
    version: int
    hash_prev_block: bytes
    hash_merkle_root: bytes
    time: int
    bits: int
    nonce: int

    def as_bin_block_header(self) -> bytes:
        """
        ブロックハッシュの元となる部分だけを切り出したもの
        バージョン(little、4bytes)、前ブロックのハッシュ(little)、マークルルート(little)、時間(little、4bytes)、
        bits(難易度のやつ、little、4bytes)、nonce(little、4bytes)で構成される
        """
        block_bin = self.version.to_bytes(4, byteorder="little")
        block_bin += self.hash_prev_block[::-1]
        block_bin += self.hash_merkle_root[::-1]
        block_bin += self.time.to_bytes(4, byteorder="little")
        block_bin += self.bits.to_bytes(4, byteorder="little")
        block_bin += self.nonce.to_bytes(4, byteorder="little")
        return block_bin

    def block_hash(self) -> bytes:
        block_bin = self.as_bin_block_header()
        return sha256d(block_bin)


if __name__ == "__main__":
    block = Block(
        version=0x26882000,
        hash_prev_block=binascii.a2b_hex("00000000000000000000bff6b5b07d9ea4708b78cb39924d3cfa510dee056ea0"),
        hash_merkle_root=binascii.a2b_hex("eb24e516075d43708db632481dceff054805909e8a8d14f7d31bd96891f7fa1e"),
        time=1699678954,
        bits=0x17048194,
        nonce=2757659172
    )
    print(f"explorer url: https://btc1.trezor.io/block/{block.block_hash()[::-1].hex()}")
