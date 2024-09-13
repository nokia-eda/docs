#!/usr/bin/env python3
"""
This script converts the output of the `make list-setter*` command
from the nokia-eda/playground repo to a markdown table to be featured in the docs.
"""

import re
import sys

print("| Name | Example Value | Type | Description|")
print("|------|-------|------|-|")

for line in sys.stdin:
    match = re.search(r"Name: (\w+), Value: (.*?), Type: (\w+)", line)
    if match:
        name, value, type_ = match.groups()
        if name == "LLM_API_KEY":
            value = "some-key"
        print(f"| `{name}` | `{value}` | `{type_}` |  |")
