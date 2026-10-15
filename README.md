# ww-net

Een netwerk-checker die geduldig wacht, slim omgaat met DNS, en logt
via `arin_log`. Gebouwd voor langlopende pipelines die niet mogen vallen
als het internet even wegvalt.

## Waarom ww-net?

- **Checkt TCP, niet ICMP.** `ping` wordt vaak geblokkeerd door routers
  en firewalls. `ww-net` test poorten 80 en 443 — precies wat je browser
  ook doet. Daarom werkt het betrouwbaar achter een router.
- **Hamert het netwerk niet.** Wacht met oplopende intervallen (1s → 15s),
  niet met een vaste korte poll.
- **Kiest willekeurig een DNS-server.** Cloudflare, Google, Quad9, OpenDNS —
  als één plat ligt, probeert hij een andere.
- **Wacht uren als het moet.** Eén parameter (`wait`) in seconden; tot 12 uur
  of langer, zonder het netwerk te belasten.
- **Logt via `arin_log`.** Netwerkproblemen komen in je bestaande logbestand,
  niet in een apart spoor dat je later moet samenvoegen.
- **Werkt voor twee vragen.** "Is er internet?" én "Is déze host bereikbaar?"

## Installatie

    pip install ww-net

`arin_log` wordt automatisch mee geïnstalleerd als dependency.

> **Eerste gebruik:** bij de eerste import opent `arin_log` een dialoog om
> een folder voor de logbestanden te kiezen. Daarna wordt die keuze onthouden.

## Gebruik

    from ww_net import is_net, is_host

    # Controleer of er internet is (wacht tot 12 uur)
    if is_net(wait=43200):
        print("Internet is beschikbaar")

    # Controleer of een specifieke host bereikbaar is
    if is_host("https://www.google.com/", wait=43200):
        print("Host is bereikbaar")

## Demo

    python -m ww_net

Draait een snelle netwerk-check: is er internet, is een host bereikbaar,
en hoe wordt een niet-bestaande host afgehandeld?

## Screenshots

Console — schoon, zonder emoji's:

![ww-net console](https://raw.githubusercontent.com/marcus-aurelius-hu/ww_net/main/docs/console.png)

Logbestand — met emoji's en tijdstempels:

![ww-net logbestand](https://raw.githubusercontent.com/marcus-aurelius-hu/ww_net/main/docs/log_file.png)

## Wachten

De `wait`-parameter is de tijd (in seconden) waarna `ww_net` opgeeft.
De standaardwaarde is `3600` (1 uur). Omdat het in seconden gaat, kun je
gemakkelijk langere periodes instellen:

| Duur | Seconden |
|------|----------|
| 1 uur | 3600 |
| 4 uur | 14400 |
| 8 uur | 28800 |
| 12 uur | 43200 |

Tijdens het wachten loopt het interval op van 1 seconde tot 15 seconden.
Zo wordt het netwerk niet onnodig belast, maar blijft `ww_net` wel alert.

## API

| Functie | Beschrijving |
|---------|--------------|
| `is_net(wait=None, logloc=None)` | Controleert of er internet is. Wacht tot `wait` seconden. |
| `is_host(host, wait=None, logloc=None)` | Controleert of `host` bereikbaar is. Wacht tot `wait` seconden. |

Beide functies retourneren `True` of `False`.

## Logging

`ww_net` logt via `arin_log`. De `logloc`-parameter bepaalt in welk
logbestand de berichten terechtkomen:

    from ww_net import is_net

    # Zonder logloc: berichten gaan naar het standaardbestand (ww_net)
    is_net(wait=3600)

    # Met logloc: berichten gaan naar een eigen logbestand (mijn_pipeline)
    is_net(wait=3600, logloc="mijn_pipeline")

Zo kun je netwerkproblemen in het logbestand van je eigen pipeline plaatsen.

Korte hikken (< 2,5 seconde) worden niet gelogd. Alleen echte
onderbrekingen komen in het logbestand. Zo blijft het logbestand schoon
en zie je alleen wat de moeite waard is.

## Licentie

MIT — zie [LICENSE](LICENSE).

## Status

**Alpha (0.1.6).** The core works. Tests are still in development.