#!/usr/bin/env python3
"""Refresh data/playlists.json from the public Spotify and YouTube pages.

Run from the repo root:

    python tools/refresh.py

What it does, for every month in data/playlists.json:
  * re-reads the Spotify playlist (name, songs, cover, cover colour)
  * recomputes the 8x8 mosaic colours when the cover changed (needs Pillow: pip install pillow)
  * updates the YouTube video count when the month has a YouTube playlist
A playlist that can't be fetched keeps its old data. Nothing is ever deleted.

Adding a month: append an entry to "months" with just a key and links, for example
    {"key": "2026-12", "spotify": "https://open.spotify.com/playlist/...", "youtube": "https://www.youtube.com/playlist?list=..."}
then run this script. The GitHub Action in .github/workflows runs it for you on every change
to data/playlists.json, and every Monday.

Limit: Spotify's embed page lists the first 100 songs of a playlist, so a month with more than
100 songs would show only its first 100 here (the embedded player still has them all).
"""
import datetime
import io
import json
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "playlists.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
NBSP = " "


def get(url, tries=3):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read()
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(2 * (attempt + 1))


def spotify_id(value):
    value = (value or "").strip()
    m = re.search(r"playlist[/:]([A-Za-z0-9]{22})", value) or re.fullmatch(r"([A-Za-z0-9]{22})", value)
    return m.group(1) if m else None


def youtube_id(value):
    value = (value or "").strip()
    m = (re.search(r"[?&]list=([A-Za-z0-9_-]+)", value)
         or re.search(r"/browse/VL([A-Za-z0-9_-]+)", value)
         or re.fullmatch(r"(?:VL)?((?:PL|OL|UU|FL|RD)[A-Za-z0-9_-]+)", value))
    return m.group(1) if m else None


def parse_embed(html):
    """Pull the playlist out of Spotify's embed page (the JSON in its __NEXT_DATA__ script)."""
    m = re.search(rb'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        raise ValueError("Spotify's embed page had no playlist data")
    entity = json.loads(m.group(1))["props"]["pageProps"]["state"]["data"]["entity"]
    tracks = []
    for t in entity.get("trackList") or []:
        tid = (t.get("uri") or "").split(":")[-1]
        if not tid:
            continue
        # Spotify separates artists with "," + no-break space; a plain ", " belongs to a name.
        artists = [a.strip() for a in (t.get("subtitle") or "").split("," + NBSP) if a.strip()]
        tracks.append([tid, t.get("title") or "", artists, round((t.get("duration") or 0) / 1000)])
    sources = sorted((entity.get("coverArt") or {}).get("sources") or [], key=lambda s: s.get("width") or 0)
    big = sources[-1]["url"] if sources else ""
    small = next((s["url"] for s in sources if (s.get("width") or 0) >= 64), big)
    bg = (entity.get("visualIdentity") or {}).get("backgroundBase") or {}
    rgb = [bg.get("red", 83), bg.get("green", 83), bg.get("blue", 83)]
    return {"label": entity.get("name") or entity.get("title") or "", "tracks": tracks,
            "cover": big, "cover_small": small, "rgb": rgb}


def pixels(image_bytes):
    """Average a cover down to 8x8 colours, returned as 64 hex triples in one string."""
    from PIL import Image  # optional dependency
    im = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((64, 64), Image.LANCZOS)
    px, out = im.load(), []
    for gy in range(8):
        for gx in range(8):
            r = g = b = 0
            for y in range(gy * 8, gy * 8 + 8):
                for x in range(gx * 8, gx * 8 + 8):
                    pr, pg, pb = px[x, y]
                    r, g, b = r + pr, g + pg, b + pb
            out.append("%02x%02x%02x" % (round(r / 64), round(g / 64), round(b / 64)))
    return "".join(out)


def youtube_count(list_id):
    html = get(f"https://www.youtube.com/playlist?list={list_id}")
    m = re.search(rb'"(\d[\d,]*) videos?"', html)
    return int(m.group(1).replace(b",", b"")) if m else None


def dump(data):
    """Readable, diff-friendly JSON: one song per line."""
    out = ["{"]
    for k in [k for k in data if k != "months"]:
        out.append(f"  {json.dumps(k)}: {json.dumps(data[k], ensure_ascii=False)},")
    out.append('  "months": [')
    months = sorted(data.get("months", []), key=lambda m: m.get("key", ""))
    for i, m in enumerate(months):
        out.append("    {")
        for k in [k for k in m if k != "tracks"]:
            out.append(f"      {json.dumps(k)}: {json.dumps(m[k], ensure_ascii=False)},")
        tracks = m.get("tracks") or []
        out.append('      "tracks": [')
        for j, t in enumerate(tracks):
            out.append("        " + json.dumps(t, ensure_ascii=False) + ("," if j < len(tracks) - 1 else ""))
        out.append("      ]")
        out.append("    }" + ("," if i < len(months) - 1 else ""))
    out.append("  ]")
    out.append("}")
    return "\n".join(out) + "\n"


def refresh(data, log):
    changed = False

    def setv(obj, key, value):
        nonlocal changed
        if obj.get(key) != value:
            obj[key] = value
            changed = True

    for m in data.get("months", []):
        key = m.get("key", "")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", key):
            log(f"Skipped a month without a YYYY-MM key: {json.dumps(m)[:80]}")
            continue
        sid = spotify_id(m.get("spotify"))
        if not sid:
            log(f"{key}: no Spotify playlist link")
            continue
        setv(m, "spotify", sid)
        if m.get("youtube"):
            yid = youtube_id(m["youtube"])
            if yid:
                setv(m, "youtube", yid)
            else:
                log(f"{key}: couldn't read the YouTube link, left it as is")
        try:
            info = parse_embed(get(f"https://open.spotify.com/embed/playlist/{sid}"))
        except Exception as e:  # keep old data
            log(f"{key}: Spotify didn't answer ({e}); kept the old data")
            continue
        if not info["tracks"] and m.get("tracks"):
            log(f"{key}: Spotify returned no songs; kept the old list")
        else:
            setv(m, "tracks", info["tracks"])
        if info["label"]:
            setv(m, "label", info["label"])
        setv(m, "rgb", info["rgb"])
        has_pixels = bool(re.fullmatch(r"[0-9a-f]{384}", m.get("pixels") or ""))
        if info["cover"] and (m.get("cover") != info["cover"] or not has_pixels):
            try:
                setv(m, "pixels", pixels(get(info["cover_small"])))
                setv(m, "cover", info["cover"])
            except ImportError:
                log("Pillow isn't installed (pip install pillow), so cover colours weren't refreshed")
                setv(m, "cover", info["cover"])
            except Exception as e:
                log(f"{key}: couldn't read the cover image ({e})")
        if m.get("youtube"):
            try:
                n = youtube_count(m["youtube"])
                if n is not None:
                    setv(m, "youtubeCount", n)
            except Exception as e:
                log(f"{key}: YouTube didn't answer ({e})")
    for x in data.get("extras", []):
        if x.get("youtube"):
            try:
                n = youtube_count(youtube_id(x["youtube"]) or x["youtube"])
                if n is not None:
                    setv(x, "youtubeCount", n)
            except Exception as e:
                log(f"{x.get('key')}: YouTube didn't answer ({e})")
    return changed


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    notes = []
    changed = refresh(data, notes.append)
    if changed:
        data["updated"] = datetime.date.today().isoformat()
        DATA.write_text(dump(data), encoding="utf-8")
    prefix = "::warning::" if "GITHUB_ACTIONS" in __import__("os").environ else "warning: "
    for n in notes:
        print(prefix + n)
    print("Updated data/playlists.json" if changed else "Already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
