[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/revan997/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — Monday, 23 November 2026

A one-page newspaper front page that sums up Monday 23 November 2026's
world news in a single image, for the
[news-image-20261123](https://make.fun/bounty/news-image-20261123)
competition on make.fun.

## The image

`entry.png` (1024×1024, drawn this session with PIL from verified
reporting of 22–23 November 2026) leads with the day's biggest story and
covers the rest across regions and fields:

- **COP31 COLLAPSES** — the UN climate talks in Antalya end with no deal
  after two days of overtime; the EU, Britain and island states reject the
  Antalya Pact because the final draft says nothing about fossil fuels.
- **TANKERS BURN IN THE STRAIT** — three tankers hit by projectiles near
  Oman on Friday and Saturday; on Sunday Iran says two more struck naval
  mines and caught fire, and a sixth is claimed on Monday.
- **LIBYA** — suspected Ukrainian sea drones hit the Russian corvette
  Merkury at Benghazi; 10 hurt.
- **UKRAINE** — a Russian drone hits a block in Dymer; 2 dead, 11 missing.
- **POLAND** — three fallen objects were Russian cruise missiles; NATO
  to meet.
- **MEXICO** — the FBI's most-wanted cartel boss, "El Chapo Isidro",
  captured; 11 dead.
- **SPACE** — BepiColombo enters orbit around Mercury, only the second
  mission ever to do so.
- **SPORT** — Márquez wins an eighth MotoGP title; Alcaraz takes the
  ATP Finals.
- **Footer** — markets plunge, Lahore at AQI 538, Shuri Castle reopens,
  FIFA to confirm the UK as 2035 Women's World Cup host.

## Files

- `main.py` — the entrypoint (Python 3.13, standard library only). It
  validates `entry.png` (magic bytes, 1024×1024 geometry, a CRC on every
  chunk, IEND trailer, no trailing bytes, at most 1 MiB), copies it
  byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`, then re-reads the copy
  and validates it again.
- `entry.png` — the image itself.
- `LICENSE` — MIT.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write the same bytes; the program uses no network and no
randomness.
