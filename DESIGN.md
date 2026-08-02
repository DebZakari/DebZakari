# DESIGN.md — Interchange

The design system for this profile README. Derived from the shipped artifact,
not from intentions: every value below is one that `scripts/` actually emits.

This world is **local to this repository**. The portfolio site at
`DebZakari/portfolio` keeps its own monochrome design system, deliberately
untouched. Do not propagate these colours there.

---

## Thesis

**A stack is a network, not a logo wall.**

Colour names the *line* — the architectural layer — and never the vendor. Six
lines, six hues, held for the length of the page. A recruiter should be able to
point at anything orange and say "that's cloud" without a legend.

This refuses the category default for a profile README: a gradient banner over
ragged rows of vendor-coloured badges, where React blue sits beside Python blue
beside Docker blue and the colour means nothing at all.

## The world

Beck/Vignelli transit diagram. The London Underground map's grammar, applied to
a stack:

| Diagram element | What it carries here |
|---|---|
| Line | A stack layer (Languages, Web, AI & ML, Data, Cloud, Tooling) |
| Station tick | A named technology on that layer |
| 45° kink | The only permitted diagonal; lines run orthogonal otherwise |
| Circle-and-bar interchange | NovelVerse — where all six layers meet in one real system |
| Cartouche | The ruled title plate holding the name and role |

The interchange is the argument. Six lines that terminate nowhere would be a
list; six lines converging on one shipped platform is a claim about the work.

## Colour

Every line hue is drawn from GitHub Primer's accessible set and clears 4.5:1 on
its own canvas. Two sets exist because the README renders on both.

| Line | Dark canvas | Light canvas |
|---|---|---|
| Languages | `#FF6B5E` | `#CF222E` |
| Web | `#58A6FF` | `#0969DA` |
| AI & ML | `#A78BFA` | `#6639BA` |
| Data | `#3FD9A4` | `#04804D` |
| Cloud | `#FFB224` | `#BC4C00` |
| Tooling | `#F778BA` | `#BF3989` |

| Role | Dark | Light |
|---|---|---|
| Ink | `#E6EDF3` | `#1F2328` |
| Muted | `#8B949E` | `#59636E` |
| Rule | `#8B949E` @ 32% | `#59636E` @ 32% |

**Badge fills** are a third set (`scripts/build_readme.py: BULLET`). Shields.io
serves one static image to both canvases, so each fill is darkened until white
type clears 4.5:1 on the badge itself: `C22B24` `0B5FD0` `6D3EE8` `04804D`
`B4530A` `B32D77`. Same six-layer meaning, different constraint.

**`NEUTRAL = #57606A`** is reserved for Contact. Contact links are not stack
layers; painting them in a line colour would break the one rule the Stack
section spends the whole page establishing.

## Type

**Overpass** — 400, 600, 700. Chosen for its Highway Gothic lineage, which is
the signage tradition the transit form already belongs to.

All type in the SVGs is **converted to outlines** by `scripts/typeset.py`.
This is not a stylistic choice. GitHub proxies README images through camo,
where `@font-face` never resolves and `font-family` falls back to whatever the
viewer has. Outlines are the only way a README image can carry a typeface.

`typeset.py` flattens real GPOS `kern` pairs (PairPos formats 1 and 2,
including Extension-wrapped lookups) so the outlines are properly spaced rather
than metric-only.

**Tracking** is positive and wide on small caps labels (0.06–0.14em), slightly
negative on display sizes (−0.01 to −0.02em).

## Layout

Two fixed variants per theme, selected by `<picture>` at a 600px breakpoint —
GitHub allows no CSS, so this is the entire responsive mechanism available.

| | Wide | Narrow |
|---|---|---|
| Canvas | 1000 × 448 | 440 × 492 |
| Row pitch | 44px | 42px |
| Stations per line | 3 | 2 |
| Station label | Above the line, `y − 10` | Below the line, `y + 17` |
| Stroke | 6px | 5px |
| Interchange | Bar + r7 circles, right | Bar + r6 circles, centre |

Narrow labels sit *below* their line because the two-station layout puts them
where a kink would otherwise cross them. Verified clearance for the widest
narrow label ("Oracle Cloud", 63.4px): 20.3px.

## Rules

1. **Colour encodes layer, never vendor.** If a new technology arrives, it
   inherits its layer's hue. No exceptions, including for strong brand colours.
2. **Transparent ground.** Every generated SVG omits a background so it sits on
   GitHub's own canvas in light, dark, and dimmed.
3. **No logos.** Checked against the simple-icons catalog: Oracle Cloud, AWS,
   OpenAI, Playwright, Groq, Cohere, Jina, Infisical, Tiptap, Zustand, Voyage,
   Cartesia and Speechmatics have no entries. A logo set including the two the
   stack most needs to show is impossible, so the page uses none.
4. **Text must be measured.** `build_map.py` carries a `BLEED` guard that
   reports any string crossing the canvas edge. It exists because a hub caption
   silently clipped once.
5. **Missing glyphs raise.** `Face.glyphs()` throws rather than skipping. A
   subset that dropped the space character once collapsed every label in every
   asset to `DAVEZACHARYMACARAYO`.

## Generation

Nothing in `assets/` or `README.md` is hand-edited. Regenerate:

```bash
cd scripts
pip install fonttools
python build_map.py      # banner, 4 variants
python build_langs.py    # language panel, 4 variants (needs gh auth)
python build_readme.py   # README.md
```

`.github/workflows/refresh-stats.yml` reruns `build_langs.py` daily at 04:17
UTC and commits any change.

## Third-party widgets

Two remain, both under protest and both documented here so the tradeoff is not
rediscovered:

- **streak-stats** — renders in Segoe UI, cannot be restyled beyond its colour
  parameters. Every text node ships `opacity: 0` with a `fadein … forwards`
  animation, so headless screenshots of it are unreliable; verify in a browser.
- **activity-graph** — called with `hide_title=true&grid=false` to strip its own
  heading and dashed rules. The "Days" / "Contributions" axis labels are not
  removable. Thin at phone width; kept by explicit decision.

`github-readme-stats` and `top-langs` were removed: the shared public instance
answered HTTP 503 consistently. `build_langs.py` replaces them with an authored
panel that also counts private repositories.
