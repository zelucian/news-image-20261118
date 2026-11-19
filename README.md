# The world in one day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/zelucian/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/zelucian/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A procedural 1024 × 1024 newspaper front page for `news-image-20261118`,
covering the twelve supplied news facts. All artwork is drawn with Pillow;
there are no external images or network requests.

Regenerate with Pillow 10.2.0 and the DejaVu fonts installed:

```sh
python3 draw.py
```

Run the entry (Python 3.13 standard library only):

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

With no environment override, output is `/output/entry.png`. The runtime copies
the bundled `entry.png` byte for byte and does not need Pillow or fonts.
The generator uses fixed geometry, no randomness, timestamps, or PNG metadata;
repeated builds in the same font/Pillow environment produce identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=182mp9cr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
