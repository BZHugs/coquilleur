import os
import re
import tempfile

import r2pipe


r2_arch_options = {
    "arm": ["-a", "arm", "-b", "32"],
    "aarch64": ["-a", "arm", "-b", "64"],
    "x86": ["-a", "x86", "-b", "32"],
    "x86_64": ["-a", "x86", "-b", "64"],
}


def generate_graph(code, arch, base):
    """Generate a graph thanks to radare2 and its dot capabilites.
    
    Parameters
    ----------
    code : bytes
        Bytes of the program to generate a graph for.
    arch : str
        Architecture of the program.

    Returns
    -------
    str
        Graph of the program in dot format.

    """
    f = None
    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as tmp:
        f = tmp.name
        tmp.write(code)
    options = r2_arch_options.get(arch)
    options.append("-m")
    options.append(str(base))

    r = r2pipe.open(f, options)
    r.cmd("aaaa")

    outfile = tempfile.NamedTemporaryFile(delete=False).name
    r.cmd(f"agfd . > {outfile}")

    graph = open(outfile).read()

    os.remove(f)
    os.remove(outfile)

    return clean_graph(graph)


def clean_graph(graph: str):
    """Clean the graph generated by radare2 by removing non sane defaults.
    
    Parameters
    ----------
    graph : str
        Graph of the program in dot format.

    """  
    

    # Remove special comments with register values
    pattern = r";--.*?\\l(\s)?"
    graph = re.sub(pattern, "", graph)

    # Remove regular comments (XREFs) without removing end of line delimiter
    pattern = r";.*?\\l(\s)?"
    graph = re.sub(pattern, r"\\l", graph)

    # Remove function header
    pattern = r"\d?\d?\d?\d?:\sfcn.\d\d\d\d\d\d\d\d \(.*?\)"
    graph = re.sub(pattern, "", graph)

    # Remove fillcolors and colors
    pattern = "fillcolor=\".*?\","
    graph = re.sub(pattern, "", graph)
    pattern = "color=\".*?\","
    graph = re.sub(pattern, "", graph)

    # Remove fill colors in node
    pattern = "fillcolor=.*?\s"
    graph = re.sub(pattern, "", graph)

    # Fix the graph by removing trailing whitespace left in comment deletion
    pattern = "label=\"\s+"
    graph = re.sub(pattern, "label=\"", graph)

    # Recreate new lines for the Javascript library
    pattern = r"\\l"
    graph = re.sub(pattern, "\n", graph)

    return graph