"""Text -> SVG path conversion with real GPOS kerning.

Renders to outlines so the published SVG carries zero font dependency:
GitHub proxies README images through camo, where @font-face never resolves.
"""
import os

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


class Face:
    def __init__(self, path):
        self.name = os.path.basename(path)
        self.font = TTFont(path)
        self.upem = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.glyphset = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self.kern = self._load_kerning()

    def _load_kerning(self):
        """Flatten GPOS 'kern' PairPos lookups (format 1 and 2) into a dict."""
        pairs = {}
        if "GPOS" not in self.font:
            return pairs
        gpos = self.font["GPOS"].table
        if not gpos.LookupList or not gpos.FeatureList:
            return pairs

        kern_lookups = set()
        for rec in gpos.FeatureList.FeatureRecord:
            if rec.FeatureTag == "kern":
                kern_lookups.update(rec.Feature.LookupListIndex)

        for idx in sorted(kern_lookups):
            lookup = gpos.LookupList.Lookup[idx]
            for sub in lookup.SubTable:
                # Extension lookups wrap the real subtable.
                if getattr(sub, "LookupType", None) == 9 and hasattr(sub, "ExtSubTable"):
                    sub = sub.ExtSubTable
                fmt = getattr(sub, "Format", None)
                if not hasattr(sub, "Coverage"):
                    continue
                if fmt == 1:
                    for first, ps in zip(sub.Coverage.glyphs, sub.PairSet):
                        for rec in ps.PairValueRecord:
                            adj = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                            if adj:
                                pairs[(first, rec.SecondGlyph)] = adj
                elif fmt == 2:
                    c1 = sub.ClassDef1.classDefs
                    c2 = sub.ClassDef2.classDefs
                    covered = set(sub.Coverage.glyphs)
                    by_class2 = {}
                    for g, cls in c2.items():
                        by_class2.setdefault(cls, []).append(g)
                    for g1 in covered:
                        k1 = c1.get(g1, 0)
                        if k1 >= len(sub.Class1Record):
                            continue
                        rec1 = sub.Class1Record[k1]
                        for k2, rec2 in enumerate(rec1.Class2Record):
                            adj = getattr(rec2.Value1, "XAdvance", 0) if rec2.Value1 else 0
                            if not adj:
                                continue
                            for g2 in by_class2.get(k2, []):
                                pairs.setdefault((g1, g2), adj)
        return pairs

    def glyphs(self, text):
        out = []
        for ch in text:
            g = self.cmap.get(ord(ch))
            if g is None:
                # A subset that dropped a needed glyph would otherwise silently
                # collapse the run (notably: losing the space character).
                raise KeyError(
                    f"{self.name}: no glyph for {ch!r} (U+{ord(ch):04X}) in {text!r}")
            out.append(g)
        return out

    def width(self, text, size, tracking=0.0):
        """Advance width in px. `tracking` is in em, like CSS letter-spacing."""
        gs = self.glyphs(text)
        total = 0
        for i, g in enumerate(gs):
            if g is None:
                continue
            total += self.hmtx[g][0]
            if i + 1 < len(gs) and gs[i + 1] is not None:
                total += self.kern.get((g, gs[i + 1]), 0)
        return total * size / self.upem + tracking * size * max(len(text) - 1, 0)

    def path(self, text, size, x, y, tracking=0.0, anchor="start"):
        """SVG path `d` for `text`, baseline at (x, y)."""
        if anchor == "middle":
            x -= self.width(text, size, tracking) / 2
        elif anchor == "end":
            x -= self.width(text, size, tracking)

        s = size / self.upem
        gs = self.glyphs(text)
        pen_x = 0.0
        out = []
        for i, g in enumerate(gs):
            if g is None:
                continue
            spen = SVGPathPen(self.glyphset, ntos=lambda v: f"{v:.1f}")
            # Font y is up, SVG y is down -> negate the y scale.
            tpen = TransformPen(spen, Transform(s, 0, 0, -s, x + pen_x, y))
            self.glyphset[g].draw(tpen)
            d = spen.getCommands()
            if d:
                out.append(d)
            pen_x += self.hmtx[g][0] * s
            if i + 1 < len(gs) and gs[i + 1] is not None:
                pen_x += self.kern.get((g, gs[i + 1]), 0) * s
            pen_x += tracking * size
        return " ".join(out)
