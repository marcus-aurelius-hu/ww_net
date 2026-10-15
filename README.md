# ww-net

Een lichtgewicht netwerk-checker die geduldig wacht, slim omgaat met DNS en logt via `arin_log`. Speciaal gebouwd voor langlopende datastromen en pipelines die niet mogen crashen als de internetverbinding tijdelijk wegvalt.

## Waarom ww-net?

- **TCP in plaats van ICMP:** Het traditionele `ping`-commando wordt vaak geblokkeerd door routers en firewalls. `ww-net` test via de poorten 80 en 443 — precies zoals een webbrowser dat doet. Hierdoor werkt de controle altijd betrouwbaar, ook achter strikte firewalls.
- **Geen netwerkbelasting:** De tool bestookt het netwerk niet met constante aanvragen. Tijdens een onderbreking loopt het interval stapsgewijs op van 1 naar 15 seconden.
- **Dynamische DNS-keuze:** Er wordt willekeurig gekozen uit betrouwbare DNS-servers (Cloudflare, Google, Quad9, OpenDNS). Mocht er één server onbereikbaar zijn, dan schakelt de tool direct over naar een andere.
- **Urenlang geduld:** Met de parameter `wait` stel je eenvoudig de maximale wachttijd in seconden in (bijvoorbeeld tot 12 uur of langer), zonder dat dit extra resources kost.
- **Geïntegreerde logging:** Dankzij de integratie met `arin_log` worden netwerkstoringen direct in je bestaande logbestanden weggeschreven. Je hoeft achteraf dus geen losse logbestanden samen te voegen.
- **Eén slimme functie:** "Is er algemeen internet?" óf "Is deze specifieke host bereikbaar?". Beide vragen worden beantwoord vanuit dezelfde intuïtieve functie.

## Installatie

```bash
pip install ww-net
```

De library `arin_log` wordt automatisch als afhankelijkheid (dependency) meegeïnstalleerd.

> **Eerste gebruik:** Bij de allereerste import opent `arin_log` een dialoogvenster waarin je een map voor de logbestanden kunt kiezen. Deze keuze wordt vervolgens definitief onthouden.

## Gebruik

```python
from ww_net import is_net

# 1. Controleer of er algemeen internet is (wacht maximaal 12 uur)
if is_net(wait=43200):
    print("Internet is beschikbaar")

# 2. Controleer of een specifieke host bereikbaar is (wacht maximaal 12 uur)
if is_net(host="https://google.com", wait=43200):
    print("Host is bereikbaar")
```

## Demo

Twee manieren om de demonstratie te starten:

```bash
ww-net
```

```bash
python -m ww_net
```

Beide starten dezelfde demonstratie: de algemene internet-check, de bereikbaarheid van een specifieke host en de nette afhandeling van een niet-bestaande host.


## Screenshots

**Console** — Schoon en zonder emoji's:

![ww-net console](https://raw.githubusercontent.com/marcus-aurelius-hu/ww_net/main/docs/console.png)

**Logbestand** — Inclusief emoji's en exacte tijdstempels:

![ww-net logbestand](https://raw.githubusercontent.com/marcus-aurelius-hu/ww_net/main/docs/log_file.png)

## Wachttijden en intervallen

De `wait`-parameter bepaalt na hoeveel seconden `ww_net` definitief opgeeft. De standaardwaarde is `3600` seconden (1 uur). Handige referentiewaarden voor langere periodes:

| Gewenste duur | Waarde in seconden |
| :--- | :--- |
| 1 uur | `3600` |
| 4 uur | `14400` |
| 8 uur | `28800` |
| 12 uur | `43200` |

Tijdens het wachten loopt het controle-interval stapsgewijs op van 1 seconde naar maximaal 15 seconden. Dit voorkomt onnodig netwerkverkeer, terwijl de library alert blijft op herstel van de verbinding.

## API-referentie

### `is_net(host=None, wait=None, logloc=None)`

Controleert de netwerkverbinding en retourneert `True` of `False`.

| Parameter | Type | Standaardwaarde | Beschrijving |
| :--- | :--- | :--- | :--- |
| `host` | `str` | `None` | De URL of het IP-adres dat je wilt controleren. Indien weggelaten (`None`), wordt een algemene internet-check uitgevoerd. |
| `wait` | `int` | `3600` | De maximale tijd in seconden dat de functie blijft proberen de verbinding te herstellen. |
| `logloc` | `str` | `None` | De naam van het logbestand waarin de gebeurtenissen moeten worden opgeslagen. |

## Logging-configuratie

`ww_net` maakt gebruik van `arin_log`. Met de `logloc`-parameter bepaal je zelf in welk logbestand de netwerkberichten worden weggeschreven:

```python
from ww_net import is_net

# Zonder logloc: berichten worden opgeslagen in het standaardbestand (ww_net)
is_net(wait=3600)

# Met logloc: netwerklogica wordt direct weggeschreven naar je eigen pipeline-log
is_net(wait=3600, logloc="mijn_pipeline")
```

Korte netwerkhikken van minder dan 2,5 seconde worden automatisch genegeerd. Alleen daadwerkelijke onderbrekingen worden geregistreerd. Hierdoor blijven je logbestanden overzichtelijk en vrij van ruis.

## Licentie

Dit project is gelicentieerd onder de MIT-licentie — zie het [LICENSE](LICENSE)-bestand voor details.

## Status

**Alpha (0.1.8).** De kernfunctionaliteit is stabiel en volledig operationeel. Geautomatiseerde tests zijn momenteel in ontwikkeling.
