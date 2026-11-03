"""演奏会カードに並べるポスターの縮小版を作る。

index.html の concerts データに載っている全画像について、
thumbs/card/<元のファイル名（拡張子なし）>.jpg に幅300pxのJPEGを書き出す。
カードには縮小版を表示し、クリックで開く拡大表示は元画像を使う。
縮小版が無い画像は、ページ側で自動的に元画像を表示する。
ポスターを追加したら再実行する（更新が無い画像は飛ばす）。
  python3 tools/build_card_thumbs.py
"""
import re, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIDTH = 300
OUT = ROOT / "thumbs" / "card"

src = (ROOT / "index.html").read_text(encoding="utf-8")
start = src.index("const concerts = [")
body = src[start:src.index("];", start)]
files = sorted({f for block in re.findall(r"images: \[([^\]]*)\]", body) for f in re.findall(r'"([^"]+)"', block)})

OUT.mkdir(parents=True, exist_ok=True)
made = skipped = 0
for name in files:
    srcp = ROOT / name
    dst = OUT / (pathlib.Path(name).stem + ".jpg")
    if not srcp.exists():
        print("missing:", name)
        continue
    if dst.exists() and dst.stat().st_mtime >= srcp.stat().st_mtime:
        skipped += 1
        continue
    with Image.open(srcp) as im:
        im = im.convert("RGB")
        h = round(im.height * WIDTH / im.width)
        im.resize((WIDTH, h), Image.LANCZOS).save(dst, "JPEG", quality=75, optimize=True, progressive=True)
    made += 1
print(f"{made} made, {skipped} up to date, {len(files)} images")
