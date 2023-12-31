from enum import IntEnum
from typing import List, Tuple, Union


class Opcodes(IntEnum):
    OP_0 = 0x00
    OP_FALSE = OP_0
    OP_PUSHDATA1 = 0x4c
    OP_PUSHDATA2 = 0x4d
    OP_PUSHDATA4 = 0x4e
    OP_1NEGATE = 0x4f
    OP_RESERVED = 0x50
    OP_1 = 0x51
    OP_TRUE = OP_1
    OP_2 = 0x52
    OP_3 = 0x53
    OP_4 = 0x54
    OP_5 = 0x55
    OP_6 = 0x56
    OP_7 = 0x57
    OP_8 = 0x58
    OP_9 = 0x59
    OP_10 = 0x5a
    OP_11 = 0x5b
    OP_12 = 0x5c
    OP_13 = 0x5d
    OP_14 = 0x5e
    OP_15 = 0x5f
    OP_16 = 0x60

    # control
    OP_NOP = 0x61
    OP_VER = 0x62
    OP_IF = 0x63
    OP_NOTIF = 0x64
    OP_VERIF = 0x65
    OP_VERNOTIF = 0x66
    OP_ELSE = 0x67
    OP_ENDIF = 0x68
    OP_VERIFY = 0x69
    OP_RETURN = 0x6a

    # stack ops
    OP_TOALTSTACK = 0x6b
    OP_FROMALTSTACK = 0x6c
    OP_2DROP = 0x6d
    OP_2DUP = 0x6e
    OP_3DUP = 0x6f
    OP_2OVER = 0x70
    OP_2ROT = 0x71
    OP_2SWAP = 0x72
    OP_IFDUP = 0x73
    OP_DEPTH = 0x74
    OP_DROP = 0x75
    OP_DUP = 0x76
    OP_NIP = 0x77
    OP_OVER = 0x78
    OP_PICK = 0x79
    OP_ROLL = 0x7a
    OP_ROT = 0x7b
    OP_SWAP = 0x7c
    OP_TUCK = 0x7d

    # splice ops
    OP_CAT = 0x7e
    OP_SUBSTR = 0x7f
    OP_LEFT = 0x80
    OP_RIGHT = 0x81
    OP_SIZE = 0x82

    # bit logic
    OP_INVERT = 0x83
    OP_AND = 0x84
    OP_OR = 0x85
    OP_XOR = 0x86
    OP_EQUAL = 0x87
    OP_EQUALVERIFY = 0x88
    OP_RESERVED1 = 0x89
    OP_RESERVED2 = 0x8a

    # numeric
    OP_1ADD = 0x8b
    OP_1SUB = 0x8c
    OP_2MUL = 0x8d
    OP_2DIV = 0x8e
    OP_NEGATE = 0x8f
    OP_ABS = 0x90
    OP_NOT = 0x91
    OP_0NOTEQUAL = 0x92

    OP_ADD = 0x93
    OP_SUB = 0x94
    OP_MUL = 0x95
    OP_DIV = 0x96
    OP_MOD = 0x97
    OP_LSHIFT = 0x98
    OP_RSHIFT = 0x99

    OP_BOOLAND = 0x9a
    OP_BOOLOR = 0x9b
    OP_NUMEQUAL = 0x9c
    OP_NUMEQUALVERIFY = 0x9d
    OP_NUMNOTEQUAL = 0x9e
    OP_LESSTHAN = 0x9f
    OP_GREATERTHAN = 0xa0
    OP_LESSTHANOREQUAL = 0xa1
    OP_GREATERTHANOREQUAL = 0xa2
    OP_MIN = 0xa3
    OP_MAX = 0xa4

    OP_WITHIN = 0xa5

    # crypto
    OP_RIPEMD160 = 0xa6
    OP_SHA1 = 0xa7
    OP_SHA256 = 0xa8
    OP_HASH160 = 0xa9
    OP_HASH256 = 0xaa
    OP_CODESEPARATOR = 0xab
    OP_CHECKSIG = 0xac
    OP_CHECKSIGVERIFY = 0xad
    OP_CHECKMULTISIG = 0xae
    OP_CHECKMULTISIGVERIFY = 0xaf

    # expansion
    OP_NOP1 = 0xb0
    OP_CHECKLOCKTIMEVERIFY = 0xb1
    OP_NOP2 = OP_CHECKLOCKTIMEVERIFY
    OP_CHECKSEQUENCEVERIFY = 0xb2
    OP_NOP3 = OP_CHECKSEQUENCEVERIFY
    OP_NOP4 = 0xb3
    OP_NOP5 = 0xb4
    OP_NOP6 = 0xb5
    OP_NOP7 = 0xb6
    OP_NOP8 = 0xb7
    OP_NOP9 = 0xb8
    OP_NOP10 = 0xb9

    OP_INVALIDOPCODE = 0xff


def script_int_to_bytes(num: int) -> bytes:
    """
    整数を文字列として埋め込む場合に用いる
    """
    if num < Opcodes.OP_PUSHDATA1:
        return num.to_bytes(1, "little")
    elif num <= 0xff:
        hed = Opcodes.OP_PUSHDATA1
        return hed.to_bytes(1, "little") + num.to_bytes(1, "little")
    elif num <= 0xffff:
        hed = Opcodes.OP_PUSHDATA2
        return hed.to_bytes(1, "little") + num.to_bytes(2, "little")
    else:
        hed = Opcodes.OP_PUSHDATA4
        return hed.to_bytes(1, "little") + num.to_bytes(4, "little")


def script_int_to_bytes_contain_opcode(num: int) -> bytes:
    """
    -1以上16以下の整数を文字列としてではなく整数として埋め込む場合、OPCodeのことを考慮して、OP_0～OP_16を用いる
    それ以上の整数は文字列として埋め込む場合と同じように扱われる
    """
    if num == -1 or 1 <= num <= 16:
        return bytes([num + (Opcodes.OP_1 - 1)])
    elif num == 0:
        return bytes([Opcodes.OP_0])
    else:
        return script_int_to_bytes(num)


def opcode_search(opcode: int) -> Tuple[int, bool]:
    for i in Opcodes:
        if opcode == i:
            return i, True
    return opcode, False


def parse_script(script: bytes) -> List[Union[Opcodes, bytes]]:
    parsed_script = []
    data_len = 0
    data_len_size = 0
    data_len_bytes = b""
    parsed_data = b""
    for i in range(len(script)):
        if data_len > 0:
            data_len -= 1
            parsed_data += script[i:i + 1]
            if data_len == 0:
                parsed_script.append(parsed_data)
                parsed_data = b""
            continue
        elif data_len_size > 0:
            data_len_size -= 1
            data_len_bytes += script[i:i + 1]
            if data_len_size == 0:
                data_len = int.from_bytes(data_len_bytes, "little")
                data_len_bytes = b""
        opcode = script[i]
        opcode, is_opcode = opcode_search(opcode)
        if not is_opcode:
            data_len = opcode
            continue
        elif opcode == Opcodes.OP_PUSHDATA1:
            data_len_size = 1
            continue
        elif opcode == Opcodes.OP_PUSHDATA2:
            data_len_size = 2
            continue
        elif opcode == Opcodes.OP_PUSHDATA4:
            data_len_size = 4
            continue
        parsed_script.append(opcode)
    return parsed_script


if __name__ == "__main__":
    import binascii
    result = parse_script(
        binascii.a2b_hex(
            "483045022100f570245fdfc5f5adf435f9888d97de7c6173aace9785f3b3601b859ab9522582022030434c7883546a5f8573910d8a6bf9e0254a7c767f24f41eb50d5559e74d6d33014104f35021fa17cdffc2ce05526a0305a55d34e92dd88d8a63a5a55963e3884166cca2bc894fbaf56d0fa6f673be9d6605962d56ad034f507ffe6f5671c91cec7617" +
            "76a9143af9b12d9a0cac3fe115355a9fbb3acd0113852188ac"
        )
    )
    print("verify result:", "ok" if result else "ng")
