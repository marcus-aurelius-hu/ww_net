"""
ww_net
------
Een lichtgewicht netwerk-checker voor langlopende pipelines.

Controleert of er internet is of dat een specifieke host bereikbaar is.
Wacht geduldig tot de verbinding terugkomt, met oplopende intervallen,
en logt ondertussen via arin_log.

Publieke API
------------
    is_net(host=None, wait=None, logloc=None)
        Controleert de netwerkverbinding.
        Als 'host' is ingevuld, wordt de specifieke host gecontroleerd.
        Anders wordt de status van het internet gecontroleerd.

De functie retourneert True of False.
"""

__version__ = "0.1.10"

from ww_net.net import (is_net,)

__all__ = ["is_net",]
