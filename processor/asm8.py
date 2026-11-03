#!/usr/bin/env python3
"""Assembler for Processor V.0 -- only what the ISA doc (ratified v2) defines.

    python3 asm8.py prog.asm [-o prog.hex]

One instruction per line, ';' starts a comment.  Operands: xN (x0-x7), #imm, [xN] (LD/ST only).
Word = [7:5] opcode | [4] imm / LD-ST / UC | [3] trf / U-S / E | [2:0] Xn ; #imm adds one byte after it.
Output: one hex byte per line (loadable into instr_mem), and a listing on screen.
"""
import argparse, re, sys

# (mnemonic, operand form) -> (opcode, bit4, bit3).  Forms: r = Xn, i = #imm (+1 byte), m = [Xn]
ISA = {
    ("add", "r"): (0b000, 0, 0), ("trf", "r"): (0b000, 0, 1),
    ("add", "i"): (0b000, 1, 0), ("trf", "i"): (0b000, 1, 1),
    ("sub", "r"): (0b001, 0, 0), ("sub", "i"): (0b001, 1, 0),
    ("and", "r"): (0b010, 0, 0), ("and", "i"): (0b010, 1, 0),
    ("or",  "r"): (0b011, 0, 0), ("or",  "i"): (0b011, 1, 0),
    ("not", "r"): (0b100, 0, 0),
    ("cmp", "r"): (0b101, 0, 0), ("cmp", "i"): (0b101, 1, 0),   # U/S bit = 0 (unsigned)
    ("ld",  "m"): (0b110, 0, 0), ("st",  "m"): (0b110, 1, 0),   # bit4 = LD/ST
    ("b",   "r"): (0b111, 1, 0),                                # bit4 = UC, bit3 = E
    ("beq", "r"): (0b111, 0, 1), ("bgt", "r"): (0b111, 0, 0),
}
MNEMS = {m for m, _ in ISA}


def operand(tok):
    if m := re.fullmatch(r"x([0-7])", tok, re.I):
        return "r", int(m[1])
    if m := re.fullmatch(r"\[\s*x([0-7])\s*\]", tok, re.I):
        return "m", int(m[1])
    if tok.startswith("#"):
        s = tok[1:].strip()
        try:
            return "i", int(s, 0) if re.match(r"-?0[xXbB]", s) else int(s, 10)
        except ValueError:
            pass
    raise ValueError(f"bad operand '{tok}'")


def assemble(text):
    out, lst = bytearray(), []
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.split(";")[0].strip()
        if not line:
            continue
        mnem, rest = (line.split(None, 1) + [""])[:2]
        mnem, rest = mnem.lower(), rest.strip()
        try:
            if mnem not in MNEMS:
                raise ValueError(f"unknown mnemonic '{mnem}'")
            form, v = operand(rest)
            if (mnem, form) not in ISA:
                raise ValueError(f"'{mnem}' does not support operand '{rest}'")
            op, b4, b3 = ISA[(mnem, form)]
            word = op << 5 | b4 << 4 | b3 << 3
            if form == "i":
                if not -128 <= v <= 255:
                    raise ValueError(f"immediate {v} does not fit in 8 bits")
                bs = [word, v & 0xFF]
            else:
                bs = [word | v]
        except ValueError as e:
            sys.exit(f"line {ln}: {e}")
        lst.append(f"{len(out):04X}  {' '.join(f'{b:02X}' for b in bs):<6}{line}")
        out += bytes(bs)
    if len(out) > 1 << 16:
        sys.exit("program exceeds 64KB instruction memory")
    return out, lst


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Processor V.0 assembler")
    ap.add_argument("src")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    mem, lst = assemble(open(a.src).read())
    out = a.out or re.sub(r"\.\w+$", "", a.src) + ".hex"
    open(out, "w").write("".join(f"{b:02X}\n" for b in mem))
    print("\n".join(lst))
    print(f"{len(mem)} bytes -> {out}")
