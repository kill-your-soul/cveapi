import re
from typing import Any, BinaryIO


def extract_links_from_file(f: BinaryIO) -> tuple[list[Any], list[Any]]:
    poc_links = []
    ref_links = []

    content = f.read().decode("UTF-8")
    poc_section = re.search(r"#### Github(.*?)(###|$)", content, re.DOTALL)
    ref_section = re.search(r"#### Reference(.*?)####", content, re.DOTALL)
    if poc_section:
        poc_links = list(map(str.strip, re.findall(r"https?://\S+", poc_section.group(1))))
    if ref_section:
        ref_links = list(map(str.strip, re.findall(r"https?://\S+", ref_section.group(1))))
    return poc_links, ref_links
