# Bitcoinのスクリプトによって送金を処理するスタックマシン

import binascii
from hash_util import hash160
from script import Opcodes, parse_script


def stack_machine(script: bytes):
    stack = []
    script_array = parse_script(script)

    for script in script_array:
        if type(script) == bytes:
            stack.append(script)
        elif script == Opcodes.OP_DUP:
            stack.append(stack[-1])
        elif script == Opcodes.OP_HASH160:
            stack.append(hash160(stack.pop()))
        elif script == Opcodes.OP_EQUALVERIFY:
            result = stack.pop() == stack.pop()
            if not result:
                return result
        elif script == Opcodes.OP_EQUAL:
            stack.append(stack.pop() == stack.pop())
        elif script == Opcodes.OP_VERIFY:
            result = stack.pop()
            if not result:
                return result
        elif script == Opcodes.OP_CHECKSIG:
            stack.pop()  # pubkey
            stack.pop()  # signature
            # 本当は検証処理をやりたかった.....
            stack.append(True)
        else:
            raise ValueError(f"not supported: {script}")
    return stack.pop()


if __name__ == "__main__":
    result = stack_machine(
        binascii.a2b_hex(
            "483045022100f570245fdfc5f5adf435f9888d97de7c6173aace9785f3b3601b859ab9522582022030434c7883546a5f8573910d8a6bf9e0254a7c767f24f41eb50d5559e74d6d33014104f35021fa17cdffc2ce05526a0305a55d34e92dd88d8a63a5a55963e3884166cca2bc894fbaf56d0fa6f673be9d6605962d56ad034f507ffe6f5671c91cec7617" +
            "76a9143af9b12d9a0cac3fe115355a9fbb3acd0113852188ac"
        )
    )
    print("verify result:", "ok" if result else "ng")
