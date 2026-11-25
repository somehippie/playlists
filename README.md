# Monthly rotation

A calendar of my monthly playlists, June 2025 onward, on Spotify and YouTube.

**Live:** https://somehippie.github.io/playlists/

Each month is a tile made from its Spotify cover, averaged down to 8×8 colours. Tap one for the songs, the Spotify and YouTube players, and links to every track. Below the calendar: search across every song, songs per month, the artists who keep coming back, and the songs that made more than one month.

## What's in the repo

| File | What it does |
| --- | --- |
| `index.html` | The whole site: calendar, month pages, players, search, stats |
| `data/playlists.json` | Every month's links, songs and cover colours. The only file you edit |
| `tools/refresh.py` | Re-reads the playlists from Spotify and YouTube and updates the data file |
| `.github/workflows/refresh.yml` | Runs the refresh every Monday and whenever the data file changes |
| `og.png` | The picture shown when the link is shared |

## Add a new month

Add one entry to `"months"` in `data/playlists.json` (GitHub's web editor is fine) and commit:

```json
{"key": "2026-12", "spotify": "https://open.spotify.com/playlist/…", "youtube": "https://www.youtube.com/playlist?list=…"},
```

Leave out `"youtube"` if that month isn't on YouTube yet. Within a few minutes the Action fills in the name, songs and cover colours, commits them, and GitHub Pages republishes. Songs you add to a playlist later show up after the Monday refresh, or right away if you run the workflow by hand (Actions tab → Refresh playlist data → Run workflow).

## Run it on your computer

```
python -m http.server
```

Then open http://localhost:8000. The page loads `data/playlists.json`, so opening `index.html` straight from disk won't work.

To refresh the data by hand:

```
pip install pillow
python tools/refresh.py
```

## Make your own

Fork the repo, replace the months in `data/playlists.json` with your playlists (a `key` and links are enough), change `owner` and `links`, edit the two header lines in `index.html`, run the refresh, and turn on GitHub Pages (Settings → Pages → Deploy from branch → `main`, `/`).

## Notes

- Song lists come from Spotify's public embed pages, which list the first 100 songs of a playlist. The embedded player always has the full playlist.
- Music, artwork and trademarks belong to their owners. This site links to and embeds Spotify and YouTube; it doesn't host any audio.
- Code is MIT licensed.
