#!/usr/bin/env python3
"""Assembler for Processor V.0 -- only what the ISA doc (ratified v2) defines.

    python3 asm8.py prog.asm [-o prog.hex]

One instruction per line, ';' starts a comment.  Operands: xN (x0-x7), #imm (a bare number also works), [xN] (LD/ST only).
          cmp = unsigned, cmp.s = signed (U/S bit).  not #imm exists in the RTL / cocotb (0x90).
Labels:   '.name' on its own line defines one.
Branches: 'b xN' / 'beq xN' / 'bgt xN' encode the register as written (you load the offset yourself).
          'b name' / 'beq .name' uses the register of the most recent 'trf xN' before it.  If that is
          'trf #off ; trf xN ; b name' back to back, #off is replaced by (label address - branch address),
          since the RTL adds the offset to the branch's own address (waveform: branch at 9, offset 2 -> pc 11).
          Otherwise nothing is changed and the listing says what the register must hold.
Output:   one hex byte per line (loadable into instr_mem), and a listing on screen.
"""
import argparse, re, sys

# (mnemonic, operand form) -> (opcode, bit4, bit3).  Forms: r = Xn, i = #imm (+1 byte), m = [Xn]
ISA = {
    ("add", "r"): (0b000, 0, 0), ("trf", "r"): (0b000, 0, 1),
    ("add", "i"): (0b000, 1, 0), ("trf", "i"): (0b000, 1, 1),
    ("sub", "r"): (0b001, 0, 0), ("sub", "i"): (0b001, 1, 0),
    ("and", "r"): (0b010, 0, 0), ("and", "i"): (0b010, 1, 0),
    ("or",  "r"): (0b011, 0, 0), ("or",  "i"): (0b011, 1, 0),
    ("not", "r"): (0b100, 0, 0), ("not", "i"): (0b100, 1, 0),   # NOT #imm: in RTL + cocotb (0x90), not in ISA doc
    ("cmp", "r"): (0b101, 0, 0), ("cmp", "i"): (0b101, 1, 0),   # U/S bit = 0 (unsigned)
    ("cmp.s", "r"): (0b101, 0, 1), ("cmp.s", "i"): (0b101, 1, 1),   # U/S bit = 1 (signed); spelling not in ISA doc
    ("ld",  "m"): (0b110, 0, 0), ("st",  "m"): (0b110, 1, 0),   # bit4 = LD/ST
    ("b",   "r"): (0b111, 1, 0),                                # bit4 = UC, bit3 = E
    ("beq", "r"): (0b111, 0, 1), ("bgt", "r"): (0b111, 0, 0),
}
MNEMS = {m for m, _ in ISA}
BRANCHES = {"b", "beq", "bgt"}
LABEL_DEF = re.compile(r"\.([A-Za-z_]\w*):?")
REG = re.compile(r"x[0-7]", re.I)


def operand(tok):
    if m := re.fullmatch(r"x([0-7])", tok, re.I):
        return "r", int(m[1])
    if m := re.fullmatch(r"\[\s*x([0-7])\s*\]", tok, re.I):
        return "m", int(m[1])
    s = tok[1:].strip() if tok.startswith("#") else tok
    if re.fullmatch(r"-?(0[xX][0-9a-fA-F]+|0[bB][01]+|\d+)", s):
        return "i", int(s, 0) if re.match(r"-?0[xXbB]", s) else int(s, 10)
    if not tok.startswith("#") and (m := re.fullmatch(r"\.?([A-Za-z_]\w*)", tok)):
        return "l", m[1].lower()
    raise ValueError(f"bad operand '{tok}'")


def assemble(text):
    items, labels, refs, hist, pc = [], {}, [], [], 0
    trfx = None
    for ln, raw in enumerate(text.splitlines(), 1):
        line = raw.split(";")[0].strip()
        if not line:
            continue
        m = re.fullmatch(r"([A-Za-z][A-Za-z.]*)\s*(.*)", line)           # also accepts 'st[x6]'
        mnem, rest = (m[1].lower(), m[2].strip()) if m else (line.split()[0].lower(), "")
        try:
            if m := LABEL_DEF.fullmatch(line):
                name = m[1].lower()                                         # labels are case-insensitive
                if name in labels or REG.fullmatch(name):
                    raise ValueError(f"bad or duplicate label '.{m[1]}'")
                labels[name] = pc
                items.append(dict(addr=pc, bs=[], text=line))
                continue
            if mnem not in MNEMS:
                raise ValueError(f"unknown mnemonic '{mnem}'")
            form, v = operand(rest)
            lab = None
            if mnem in BRANCHES and form == "l":
                if trfx is None:
                    raise ValueError(f"'{mnem} {rest}' needs a 'trf xN' before it (xN holds the offset)")
                lab, form, v = v, "r", trfx["reg"]
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
        item = dict(addr=pc, bs=bs, text=line, key=(mnem, form), reg=v)
        if lab:
            fill = hist[0] if len(hist) == 2 and hist[1] is trfx and hist[0]["key"] == ("trf", "i") else None
            refs.append((ln, lab, item, fill))
        if (mnem, form) == ("trf", "r"):
            trfx = item
        items.append(item)
        hist = (hist + [item])[-2:]
        pc += len(bs)
    for ln, name, br, t in refs:                         # resolve label branches
        if name not in labels:
            sys.exit(f"line {ln}: undefined label '{name}'")
        off = labels[name] - br["addr"]
        if not -128 <= off <= 127:
            sys.exit(f"line {ln}: offset {off} to '.{name}' does not fit in 8 bits")
        if t:                                            # 'trf #off ; trf xN ; b name' back to back
            t["bs"][1] = off & 0xFF
            t["text"] += f"   ; offset to .{name} = {off}"
        else:                                            # register loaded earlier: leave the code alone
            br["text"] += f"   ; x{br['reg']} must hold {off} (offset to .{name})"
    if pc > 1 << 16:
        sys.exit("program exceeds 64KB instruction memory")
    out = bytearray(b for it in items for b in it["bs"])
    lst = [f"{it['addr']:04X}  {' '.join(f'{b:02X}' for b in it['bs']):<6}{it['text']}" for it in items]
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
