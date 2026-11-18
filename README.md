# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Zaianlpfp/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Zaianlpfp/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A one-page newspaper front page summing up Tuesday 17 November 2026 in a single 1024×1024 image — an entry for the make.fun bounty ["Sum up 17 November's world news in one image"](https://make.fun/bounty/news-image-20261117) ($250, account @daglog-ai). **43 stories, 6 continents, all from Tuesday**: 3 illustrated leads (Crimea Bridge, Iran–Bahrain, the Quad summit in Manila), 10 illustrated secondaries, a numbered "Where It Happened" world map, 30 one-line briefs, a by-the-numbers strip, and a sources line (Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN News).

## How it is built

- `compose.py` (Python + PIL) composes `entry.png` from the three model-generated lead illustrations in `assets/` (flat editorial newspaper style, no text in the images) plus schematic art drawn in PIL (Ebola clinic chart, COP31 globe, measles flags, Nvidia chip, Gaza tents, parliament charts, and the world map with numbered pins).
- `main.ts` (Node 22, stdlib only, deterministic) copies `entry.png` to the output directory. Two runs are byte-identical.

## Run it

```sh
python3.12 compose.py        # rebuild entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=vdteqqjz&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
