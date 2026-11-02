"""ポスター帯（marquee.html）用のサムネイルと posters.json を作る。

index.html の concerts データから各演奏会の1枚目の画像を取り出し、
thumbs/ に幅280pxのJPEGを書き出す。ポスターを追加したら再実行する。
  python3 tools/build_marquee.py
"""
import json, re, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
WIDTH = 280

src = (ROOT / "index.html").read_text(encoding="utf-8")
start = src.index("const concerts = [")
body = src[start:src.index("];", start)]
entries = re.split(r"\n  \{\n", body)[1:]

(ROOT / "thumbs").mkdir(exist_ok=True)
posters = []
for e in entries:
    date = re.search(r'date: "([\d-]+)"', e).group(1)
    title = re.search(r'title: "([^"]+)"', e).group(1)
    imgs = re.search(r"images: \[([^\]]*)\]", e)
    files = re.findall(r'"([^"]+)"', imgs.group(1)) if imgs else []
    if not files:
        continue
    out = f"thumbs/{date}.jpg"
    with Image.open(ROOT / files[0]) as im:
        im = im.convert("RGB")
        h = round(im.height * WIDTH / im.width)
        im.resize((WIDTH, h), Image.LANCZOS).save(ROOT / out, "JPEG", quality=72, optimize=True, progressive=True)
    posters.append({"date": date, "title": title, "thumb": out})

posters.sort(key=lambda p: p["date"])
(ROOT / "posters.json").write_text(json.dumps(posters, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{len(posters)} posters")
