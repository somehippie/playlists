# Monthly Rotation - Music Calendar

A calendar of my monthly playlists, June 2025 onward, on Spotify and YouTube.

**Live:** https://somehippie.github.io/playlists/

Years run June to May and the calendar reads newest first: each year opens with its year-end compilation on its own cover photo (Midyears 25'26 for June 2025 to May 2026), then its seasons and months, latest at the top. A small label next to the newest year says what's coming up next. Each month is a tile made from its Spotify cover, averaged down to 8×8 colours. Tap one for the songs, links to every track, which songs made the year-end cut, and the same month a year earlier. Play a whole month or any single song in the player bar at the bottom, which keeps going while you browse. There's a light/dark switch next to the profile links; it follows your system until you pick the other one. Below the calendar: search across every song, songs per month, the artists who keep coming back, and the songs that made more than one month.

## What's in the repo

| File | What it does |
| --- | --- |
| `index.html` | The whole site: calendar, month pages, players, search, stats |
| `data/playlists.json` | Every month's and every year-end compilation's links, songs and cover colours. The only file you edit |
| `covers/` | Cover photos for the year-end compilations |
| `tools/refresh.py` | Re-reads the playlists from Spotify and updates the data file |
| `.github/workflows/refresh.yml` | Runs the refresh every Monday and whenever the data file changes |
| `og.png` | The picture shown when the link is shared |

## Add a new month

Add one entry to `"months"` in `data/playlists.json` (GitHub's web editor is fine) and commit:

```json
{"key": "2026-12", "spotify": "https://open.spotify.com/playlist/…", "youtube": "https://www.youtube.com/playlist?list=…"},
```

Leave out `"youtube"` if that month isn't on YouTube yet. The site shows months as Jun'26, Sep'26 and so on, whatever the playlist itself is called. Within a few minutes the Action fills in the name, songs and cover colours, commits them, and GitHub Pages republishes. Songs you add to a playlist later show up after the Monday refresh, or right away if you run the workflow by hand (Actions tab → Refresh playlist data → Run workflow).

## Add the year-end compilation

When the year's compilation is ready, add it to `"compilations"`:

```json
{"key": "midyears-26-27", "from": "2026-06", "to": "2027-05", "spotify": "https://open.spotify.com/playlist/…", "youtube": "https://www.youtube.com/playlist?list=…"}
```

It appears at the end of its year. To give it a cover, put a square photo in `covers/` (about 900 pixels wide is plenty) and add these two fields to its entry:

```json
"cover": "covers/midyears-26-27.webp", "coverAlt": "What the photo shows, for screen readers"
```

The Action works out the photo's colours, which tint the compilation's page. Until it has a cover, the compilation shows a strip of its months' colours.

Spotify's embed page only lists the first 100 songs of a playlist, so the Action fills in a compilation's song list only when it has fewer than 100 songs; a longer one needs its full list added once by hand (or ask Claude to pull it).

Years start in June (`"yearStarts": 6` in the data file).

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

Fork the repo, replace the months in `data/playlists.json` with your playlists (a `key` and links are enough), change `owner` and `links`, edit the two header lines in `index.html`, delete `covers/` and the `cover` lines (or use your own photos), run the refresh, and turn on GitHub Pages (Settings → Pages → Deploy from branch → `main`, `/`).

## Notes

- Song lists come from Spotify's public embed pages, which list the first 100 songs of a playlist. The embedded players always have the full playlist.
- Music, artwork and trademarks belong to their owners. This site links to and embeds Spotify and YouTube; it doesn't host any audio.
- Code is MIT licensed. The photo in `covers/` is mine and isn't part of that license.
