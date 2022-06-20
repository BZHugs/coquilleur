const SHELLCODES = [
    {
        'name':'x86_64: exemple',
        'arch': 'x86_64',
        'shellcode': "cHVzaCByYXgKcG9wIHJzaQoKY21wIHJheCwgcnNpCmpuZSBmb28KbW92IHJheCwgMQpqbXAgYmFyCmZvbzoKbW92IHJheCwgMAoKYmFyOgpyZXQ=",
    },
    {
        'name':'x64: execve("/bin/sh")',
        'arch': 'x86_64',
        'shellcode': "eG9yICAgICByZHgsIHJkeAptb3YgICAgIHJieCwgMHgyZjJmNjI2OTZlMmY3MzY4OyAnLy9iaW4vc2gnCnNociAgICAgcmJ4LCAweDgKcHVzaCAgICByYngKbW92ICAgICByZGksIHJzcApwdXNoICAgIHJheApwdXNoICAgIHJkaQptb3YgICAgIHJzaSwgcnNwCm1vdiAgICAgYWwsIDB4M2IKc3lzY2FsbA==",
    },
    {
        'name':'arm: set registers then break',
        'arch': 'arm',
        'shellcode': "bW92dyByMCwgIzB4NDE0MQptb3Z0IHIwLCAjMHg0MTQxCgptb3Z3IHIxLCAjMHg0MjQyCm1vdnQgcjEsICMweDQyNDIKCm1vdncgcjIsICMweDQzNDMKbW92dCByMiwgIzB4NDM0MwoKbW92dyByMywgIzB4NDQ0NAptb3Z0IHIzLCAjMHg0NDQ0Cgpia3B0ICMw",
    },
    {
        'name':'aarch64: set registers then break',
        'arch': 'aarch64',
        'shellcode': "bW92eiB4MCwgMHg0MTQxCm1vdmsgeDAsIDB4NDE0MSwgbHNsIDE2Cm1vdmsgeDAsIDB4NDE0MSwgbHNsIDMyCm1vdmsgeDAsIDB4NDE0MSwgbHNsIDQ4Cgptb3Z6IHgxLCAweDQyNDIKbW92ayB4MSwgMHg0MjQyLCBsc2wgMTYKbW92ayB4MSwgMHg0MjQyLCBsc2wgMzIKbW92ayB4MSwgMHg0MjQyLCBsc2wgNDgKCm1vdnogeDIsIDB4NDM0Mwptb3ZrIHgyLCAweDQzNDMsIGxzbCAxNgptb3ZrIHgyLCAweDQzNDMsIGxzbCAzMgptb3ZrIHgyLCAweDQzNDMsIGxzbCA0OAoKbW92eiB4MywgMHg0NDQ0Cm1vdmsgeDMsIDB4NDQ0NCwgbHNsIDE2Cm1vdmsgeDMsIDB4NDQ0NCwgbHNsIDMyCm1vdmsgeDMsIDB4NDQ0NCwgbHNsIDQ4CgpicmsgIzA=",
    }
]