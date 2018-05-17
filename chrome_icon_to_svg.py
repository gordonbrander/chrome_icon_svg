#!/usr/bin/env python
"""
Quick-and-dirty script that converts Chrome .icon files into .svg files.
"""
import re
import argparse
from os import path
from xml.etree import ElementTree as ET


arg_parser = argparse.ArgumentParser(
    description="Converts Chrome .icon files to .svg")
arg_parser.add_argument("icon_path", help="The path to the .icon file")


def append_d(el, name, *values):
    d = el.get("d")
    el.set("d", d + name + " ".join(values))
    return el


def set_bounding_box(svg, width, height):
    svg.set("viewBox", "{} {}".format(width, height))
    # Create a dummy rect to mark viewbox. This helps preserve the viewbox when
    # importing into tools like Sketch.
    rect = ET.Element("rect", {
        "id": "bounding_box",
        "fill": "none",
        "stroke": "none",
        "x": "0",
        "y": "0",
        "width": width,
        "height": height
    })
    svg.insert(0, rect)
    return svg


def parse_value(s):
    """
    Quick-and-dirty way to parse C-style float literal strings into d-attribute
    compatible strings.
    """
    if s.endswith("f"):
        return s[0:-1]
    else:
        return s


def read_cmds(s):
    """
    Reads commands in file
    """
    lines = s.splitlines()
    # Match all lines that start with a word char
    cmd_lines = (line for line in lines if re.search("^\w", line))
    for line in cmd_lines:
        parts = re.split(",\s*", line)
        name = parts[0]
        values = tuple(parse_value(value) for value in parts[1:] if value is not "")
        yield name, values


def parse_cmds_to_svg(cmds):
    """
    Given a list of parsed Skia commands, builds an SVG Element tree.
    """
    svg = ET.Element("svg", {"xmlns": "http://www.w3.org/2000/svg"})
    # Append an initial path element.
    ET.SubElement(svg, "path", {
        "d": "",
        "stroke-linecap": "round"
    })
    for name, values in cmds:
        if name == "CANVAS_DIMENSIONS" and len(values) == 2:
            set_bounding_box(svg, values[0], values[1])
        elif name == "CANVAS_DIMENSIONS" and len(values) == 1:
            set_bounding_box(svg, values[0], values[0])
        elif name == "NEW_PATH":
            ET.SubElement(svg, "path", {
                "d": "",
                "stroke-linecap": "round"
            })
        # Stroke command is meant to switch from fill to stroke.
        elif name == "STROKE":
            path = svg.find("path[last()]")
            path.set("fill", "none")
            path.set("stroke", "black")
            path.set("stroke-width", values[0])
        elif name == "CAP_SQUARE":
            path = svg.find("path[last()]")
            path.set("stroke-linecap", "square")
        elif name == "CLOSE":
            path = svg.find("path[last()]")
            append_d(path, "Z")
        elif name == "MOVE_TO":
            path = svg.find("path[last()]")
            append_d(path, "M", values[0], values[1])
        elif name == "R_MOVE_TO":
            path = svg.find("path[last()]")
            append_d(path, "m", values[0], values[1])
        elif name == "LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "L", values[0], values[1])
        elif name == "R_LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "l", values[0], values[1])
        elif name == "H_LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "H", values[0])
        elif name == "R_H_LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "h", values[0])
        elif name == "V_LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "V", values[0])
        elif name == "R_V_LINE_TO":
            path = svg.find("path[last()]")
            append_d(path, "v", values[0])
        elif name == "CUBIC_TO":
            path = svg.find("path[last()]")
            append_d(path, "C", *values)
        elif name == "R_CUBIC_TO":
            path = svg.find("path[last()]")
            append_d(path, "c", *values)
        elif name == "CUBIC_TO_SHORTHAND":
            path = svg.find("path[last()]")
            append_d(path, "S", *values)
        elif name == "ARC_TO":
            path = svg.find("path[last()]")
            append_d(path, "A", *values)
        elif name == "R_ARC_TO":
            path = svg.find("path[last()]")
            append_d(path, "a", *values)
    return svg
    

if __name__ == "__main__":
    args = arg_parser.parse_args()
    file_name, ext = path.splitext(args.icon_path)
    output_path = file_name + ".svg"
    with open(args.icon_path) as f:
        contents = f.read()
    cmds = read_cmds(contents)
    svg = parse_cmds_to_svg(cmds)
    s = ET.tostring(svg)
    with open(output_path, "w") as f:
        f.write(s)
