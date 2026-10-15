"""
ww_net
------
Een lichtgewicht netwerk-checker voor langlopende pipelines.

Controleert of er internet is en of een specifieke host bereikbaar is.
Wacht geduldig tot de verbinding terugkomt, met oplopende intervallen,
en logt ondertussen via arin_log.

Publieke API
------------
    is_net(wait=None, logloc=None)
        Controleert of er internet is.

    is_host(host, wait=None, logloc=None)
        Controleert of een specifieke host bereikbaar is.

Beide functies retourneren True of False.
"""

__version__ = "0.1.6"

from ww_net.net import (
    is_net,
    is_host,
)

__all__ = [
    "is_net",
    "is_host",
]