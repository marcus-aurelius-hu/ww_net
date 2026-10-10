"""
demo.py
-------
Eerste kennismaking met ww_net.

Laat zien:
    - hoe je controleert of er internet is
    - hoe je controleert of een host bereikbaar is

Draai met:
    python -m ww_net.demo
"""

from time import time
from ww_net import is_net, is_host


def demo():
    t0 = time()
    result = is_net(wait=30)
    print(f"🌐 internet ; {result} ; {(time() - t0) * 1000:.2f} msec")

    t0 = time()
    result = is_host("https://www.google.com/", wait=30)
    print(f"🌍 www.google.com ; {result} ; {(time() - t0) * 1000:.2f} msec")


if __name__ == "__main__":
    demo()
    exit(0)