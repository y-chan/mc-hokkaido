import hashlib


def sha256(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


def sha256d(x: bytes) -> bytes:
    return sha256(sha256(x))


def ripemd160(x: bytes) -> bytes:
    md = hashlib.new('ripemd160')
    md.update(x)
    return md.digest()


def hash160(x: bytes) -> bytes:
    return ripemd160(sha256(x))
