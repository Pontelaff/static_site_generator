#!/usr/bin/env python3

import sys
from textnode import TextNode, TextType

def main() -> int:
    print(TextNode("yo I'm a node", TextType.PLAIN, "https://youtu.be/dQw4w9WgXcQ?si=_Uy8eYDTiVCcaA0j"))

    return 0

if __name__ == "__main__":
    sys.exit(main())