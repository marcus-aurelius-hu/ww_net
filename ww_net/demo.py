"""
demo.py
-------
Eerste kennismaking met ww_net.

Laat zien:
    - hoe je controleert of er internet is
    - hoe je controleert of een host bereikbaar is
    - hoe een niet-bestaande host netjes wordt afgehandeld

Draai met:
    python -m ww_net
"""

from arin_log import log_start, log_exit, log_notes, tijd, cls
from time import time, sleep
from ww_net import is_net

prgnm = 'ww_net'
br = chr(10)


def demo():
    cls()
    log_start(prgnm, logloc=prgnm)

    # --- 1. Internet check ---
    tmp = f"{prgnm} ; is_net ; {tijd()}"
    log_notes(tmp)
    log_notes(f"🌐 {tmp}", cons=False, logloc=prgnm)

    t0 = time()
    result = is_net(wait=30)
    eltm = time() - t0
    tmp = f"internet ; {result} ; {eltm * 1000:.2f} msec{br}"
    log_notes(tmp)
    log_notes(f"✅ {tmp}", cons=False, logloc=prgnm)

    sleep(1)

    # --- 2. Host check (bestaande host) ---
    tmp = f"{prgnm} ; is_host ; {tijd()}"
    log_notes(tmp)
    log_notes(f"🌍 {tmp}", cons=False, logloc=prgnm)

    t0 = time()
    result = is_net(host="https://google.com", wait=30)
    eltm = time() - t0
    tmp = f"google.com ; {result} ; {eltm * 1000:.2f} msec{br}"
    log_notes(tmp)
    log_notes(f"✅ {tmp}", cons=False, logloc=prgnm)

    sleep(1)

    # --- 3. Host check (niet-bestaande host -> staged exception) ---
    tmp = "Demo staged exception for host: http://nonexistent.host"
    log_notes(tmp)
    log_notes(f"🌍 {tmp}", cons=False, logloc=prgnm)

    t0 = time()
    result = is_net(host="http://nonexistent.host", wait=5)
    eltm = time() - t0
    tmp = f"nonexistent.host; {result} ; time: {eltm:.3f} sec"
    log_notes(tmp)
    log_notes(f"⚠️ {tmp}", cons=False, logloc=prgnm)

    log_exit(prgnm, logloc=prgnm)
    return


if __name__ == "__main__":
    demo()

    