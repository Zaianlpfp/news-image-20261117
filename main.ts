// news-image-20261117 — "Tuesday 17 November 2026 — The Day in World News".
// One dense newspaper front page summing up Tuesday 17 November 2026 in
// 43 stories: 3 illustrated leads, 10 illustrated secondaries, a numbered
// world map, 30 one-line briefs, a numbers strip and a sources line.
//
// The image itself is composed at build time by compose.py (PIL) from
// model-generated lead illustrations in assets/ plus schematic art, and
// stored in this repo as entry.png. This program is the simplest
// deterministic program the rules allow: it copies that image to the
// output directory. No network, no randomness, no dates read at runtime:
// two runs are byte-identical.
// Anchor: drand quicknet round 34053942.

const fs = require("node:fs");
const path = require("node:path");

function main() {
  const src = path.join(__dirname, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "out";
  fs.mkdirSync(outDir, { recursive: true });
  const buf = fs.readFileSync(src);
  const dst = path.join(outDir, "entry.png");
  fs.writeFileSync(dst, buf);
  console.log("wrote", dst, buf.length, "bytes");
}

main();
