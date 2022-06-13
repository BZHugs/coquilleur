#!/usr/bin/env python

import os
import re
import sys
import copy
import glob
import struct
import capstone
import keystone

from flask import Flask, request, render_template
from flask_table import create_table, Col, LinkCol

from graph import generate_graph

DEBUG = (os.getenv('DEBUG_APP') != None)

app = Flask(__name__)

asm_exemple = """push rax
pop rsi

cmp rax, rsi
jne foo
mov rax, 1
jmp bar
foo:
mov rax, 0

bar:
ret
"""

bcode_exemple = "\\x50\\x5e\\x48\\x39\\xf0\\x75\\x09\\x48\\xc7\\xc0\\x01\\x00\\x00\\x00\\xeb\\x07\\x48\\xc7\\xc0\\x00\\x00\\x00\\x00\\xc3"


supported_archs = {
    "x86_64": (
        capstone.CS_MODE_64,
        capstone.CS_ARCH_X86,
        keystone.KS_MODE_64,
        keystone.KS_ARCH_X86,
    ),
    "x86": (
        capstone.CS_MODE_32,
        capstone.CS_ARCH_X86,
        keystone.KS_MODE_32,
        keystone.KS_ARCH_X86,
    ),
    "arm": (
        capstone.CS_MODE_ARM,
        capstone.CS_ARCH_ARM,
        keystone.KS_MODE_ARM,
        keystone.KS_ARCH_ARM,
    ),
    "aarch64": (
        capstone.CS_MODE_ARM,
        capstone.CS_ARCH_ARM64,
        keystone.KS_MODE_LITTLE_ENDIAN,
        keystone.KS_ARCH_ARM64,
    ),
}

themes = [theme.split("/")[-1].replace(".css", "") for theme in glob.glob("static/codeMirror/css/themes/*.css")]

themes = sorted(themes)

def _hex(n):
    return hex(n)[2:].zfill(2)


def pointer_to_escaped(lines):
    """Convert a list of hexadecimal words of 64bits to escaped opcodes.

    Parameters
    ----------
    lines : List[str]
        List of 64bits hexadecimal values.

    Returns
    -------
    str
        Escaped opcodes.
    """
    out = ""
    for line in lines:
        line = int(line.strip(), 16)
        opcodes = list(map(_hex,struct.unpack("BBBBBBBB", struct.pack("<Q", line))))
        out += "\\x"+"\\x".join(opcodes[:4])
        out += "\\x"+"\\x".join(opcodes[4:])
    return out


def html_format(text):
    return text.replace("\n", "<br />")


def hex_(n, zfill=2):
    return hex(n).replace("0x", "").zfill(zfill)


def format_opcodes(b_in):
    out = ""

    N = 1
    for b in b_in:
        if N > 4:
            out += "..."
            break

        out += hex_(b) + " "
        N += 1

    return out


def disasm(md, bcode, base=0x1000):
    md.skipdata_setup = (".db", None, None)
    md.skipdata = True
    md.detail = True

    disasm_table = {}

    for insn in md.disasm(bcode, base):
        disasm_table[hex(insn.address)] = {
                "opcodes": format_opcodes(insn.bytes),
                "mnemonic": insn.mnemonic,
                "operands": insn.op_str,
        }


    return disasm_table


def disasm_to_assembly(disasm_):
    disasm = copy.deepcopy(disasm_)

    label_count = 0
    for addr, item in disasm.items():
        if item['operands'] in disasm:
            label = f"label_{label_count}"
            disasm[item['operands']]["label"] = f"{label}:"
            disasm[addr]['operands'] = label
            label_count += 1

    assembly = []
    for addr, item in disasm.items():
        if "label" in item:
            assembly.append(item["label"])

        assembly.append(f"{item['mnemonic']} {item['operands']}")

    return "\r\n".join(assembly)

def format_compile(bcode):
    bytescodes_table = {}

    bad_char = ["00", "0A"]

    raw_hex = ""
    escaped_str = ""
    array_literal = "{"
    bytes_array = bytearray()
    size = 0

    for b in bcode:
        h = hex_(b, 2)
        if h in bad_char:
            raw_hex += f"<b id='bad'>{h}</b>"
        else:
            raw_hex += h
        escaped_str += f"\\x{h}"
        array_literal += f"0x{h}, "
        bytes_array.append(b)
        size += 1

    array_literal = array_literal[:-2] + "}"

    bytescodes_table["raw_hex"] = raw_hex
    bytescodes_table["escaped_str"] = escaped_str
    bytescodes_table["array_literal"] = array_literal
    bytescodes_table["size"] = size
    bytescodes_table["bytes"] = bytes_array

    return bytescodes_table


@app.route("/", methods=["GET"])
def hello():
    return render_template(
        "index.html",
        bcode_value=bcode_exemple,
        asm_value=asm_exemple,
        themes=themes
    )

@app.route("/", methods=["POST"])
def actions():
    action = request.form.get("action")

    if action == "disasm":
        return disasm_post(request)
    elif action == "compile":
        return compile_post()
    else:
        return hello()



# @app.route("/disasm", methods=["POST"])
def disasm_post():
    original_bcode = request.form.get("bytecodes").strip()
    bcode_escaped = original_bcode
    # If the bcode is composed of leaked pointers, such as
    # 0xb940c26a110012e9\n0x540001486b0a013f\n, first convert it to escaped
    # bytecode first to keep the rest of the function generic
    if original_bcode.startswith("0x"):
        bcode_escaped = pointer_to_escaped(original_bcode.split())

    if bcode_escaped == "":
        return render_template(
            "index.html",
            error=f"Error: no bytecodes! (MAIS T'ES PAS NET BAUPTISTE)",
            bcode_value=bcode_escaped,
            themes=themes
        )

    bcode = (
        bcode_escaped.encode("utf8").decode("unicode_escape").encode("latin1")
    )

    arch = request.form.get("arch")
    if arch not in supported_archs:
        return render_template(
            "index.html",
            error=f"Error: Invalid arch!",
            bcode_value=bcode_escaped,
            themes=themes
        )

    raw_base = request.form.get("base")

    try:
        base = int(raw_base, 16)
        if base < 0:
            raise ValueError("No negative base please.")
    except ValueError as err:
        return render_template(
            "index.html",
            error=f"Error: {err}",
            bcode_value=bcode_escaped,
            themes=themes
        )

    cs_mode, cs_arch, _, _ = supported_archs[arch]

    md = capstone.Cs(cs_arch, cs_mode)

    disasm_table = disasm(md, bcode, base)
    code = disasm_to_assembly(disasm_table)

    dot_graph = generate_graph(bcode, arch, base)

    return render_template(
        "index.html",
        result=True,
        base=raw_base,
        asm_value=code,
        disasm_table=disasm_table,
        bcode_value=original_bcode,
        old_checked=arch,
        themes=themes,
        dot_graph=dot_graph
    )


# @app.route("/compile", methods=["POST"])
def compile_post():
    code = request.form.get("asm") + "\n"

    arch = request.form.get("arch")
    if arch not in supported_archs:
        return render_template(
            "index.html",
            error=f"Error: Invalid arch!",
            asm_value=code,
            themes=themes
        )

    cs_mode, cs_arch, ks_mode, ks_arch = supported_archs[arch]

    ks = keystone.Ks(ks_arch, ks_mode)
    md = capstone.Cs(cs_arch, cs_mode)

    code_without_comments = re.sub(";.+\\n", "\\n", code)

    try:
        x, _ = ks.asm(code_without_comments, 0)
        if x == None:
            raise ValueError("Invalid code (MAIS T'ES PAS NET BAUPTISTE)")
    except (keystone.keystone.KsError, ValueError) as err:
        return render_template(
            "index.html",
            error=f"Error: {err}",
            asm_value=code,
            themes=themes
        )

    bytescodes_table = format_compile(x)
    disasm_table = disasm(md, bytes(x), 0)

    
    dot_graph = generate_graph(bytescodes_table["bytes"], arch, 0)

    return render_template(
        "index.html",
        result=True,
        size=bytescodes_table["size"],
        disasm_table=disasm_table,
        bytescodes_table=bytescodes_table,
        asm_value=code,
        bcode_value=bytescodes_table["escaped_str"],
        old_checked=arch,
        themes=themes,
        dot_graph=dot_graph
    )


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=80)
