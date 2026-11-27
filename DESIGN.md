# Design notes

Monthly Rotation is a calendar of monthly playlists. This file explains how the site looks and why, so anyone forking it knows what each choice is for and what it's safe to change.

The current design went live in November 2026. It was designed and built with Claude Opus 5.5. The first design is commit `33ca4a5`, if you want to compare.

## The idea

Each year is pressed as one record. It has twelve grooves, one per month, with June at the rim and May by the label, the way a record plays from the edge inward. Each groove is coloured from that month's playlist cover: `tools/refresh.py` keeps an 8 by 8 grid of colours for every cover, and the page reads that grid around a circle to colour the groove. The record shows the year's music before you read a single title.

The year-end playlist is the record's centre label. A year that's still going gets a plain label with the year and "so far" until its year-end playlist exists. The month that's coming next is a dashed ring, the same dashed line the calendar uses for "Up next".

Below the record, the calendar shows every month as a sleeve: newest year first, then its seasons and months, newest first. The record is for browsing and playing; the calendar is the precise view.

## Using the turntable

| You do | What happens |
|---|---|
| Drag the arm | It follows your pointer around its pivot and settles on the nearest month. The month under the needle shows next to the record |
| Tap a groove | That month opens |
| Tap the label | That year's year-end playlist opens |
| Tap the arm | The month it's on opens |
| Arrow keys on the arm | Move one month at a time. Home and End jump to the first and last month. Enter opens the month |
| Play | Plays the month in the player bar. The record turns while Spotify says it's playing. Drop the needle on another groove while it plays and that month starts |
| Records | Switches between years |
| Open a month anywhere on the page | The turntable moves to that month, so it always shows what you last looked at |

## Research behind it

| Looked at | What stood out | What the design took |
|---|---|---|
| Spotify Wrapped 2025 | Built around physical media: mixtapes, CDs, scrapbooks, mostly black and white with colour from covers | A physical object as the main picture; colour comes only from covers |
| Streaming apps generally | Headers tinted with colour taken from the album art | Groove colours and the month page tint both come from each cover |
| Apple Music Replay | Monthly recaps, and songs that come back into your rotation | The songs-that-came-back list and the year-earlier and year-later links |
| NTS | Archives named by month, installable as an app | Month names as titles, the app manifest |
| Bandcamp | A page for every album | Every month and year-end playlist has its own link, like `#nov-26` |
| Massimo Vignelli's Stendig calendar (1966) | A calendar as a graphic object, with huge numerals | The huge condensed year numbers |
| Factory Records catalogue numbers | Numbers as identity | Each month's catalogue number, No. 1 onward |
| White-label test pressings and price stickers | Record-shop vernacular | The plain label for an unfinished year, the yellow "latest" sticker |
| Radial timeline studies | Circles suit things that repeat yearly but are harder to read precisely than a line | The record is for browsing; exact comparisons stay in the grid and the bar chart |
| Teenage Engineering hardware | Monochrome instruments with one accent colour | A black and grey deck with one yellow accent |
| Monthly playlist culture | People treat monthly playlists as a diary and revisit the same month years later | The year-earlier and year-later links on every month |

## Colour

The page stays neutral so the covers supply the colour. Vinyl is black in both themes; the only colour that isn't from a cover is sticker yellow, used for the latest month and the Play button.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--bg` | `#f5f5f2` | `#16121f` | Page: sleeve paper by day, violet at night |
| `--ink` | `#000000` | `#f5f2fb` | Text and heavy rules |
| `--mute` | `#5a5a60` | `#aba4bc` | Secondary text |
| `--line` | `#d8d8d2` | `#2e2840` | Hairlines and outlines |
| `--soft` | `#ebebe5` | `#1f1a2b` | Panels and the player bar |
| `--chip` | `#e2e2db` | `#2a2338` | Chips and hover fills |
| `--vinyl` | `#080808` | `#050407` | The record |
| `--arm` | `#9d9da3` | `#8e889e` | The tonearm |
| `--stk` | `#ffe14d` | `#ffe14d` | The sticker: latest month, Play |

## Type

One family, Archivo, self-hosted in `fonts/` under the SIL Open Font License. It's a variable font with weight from 100 to 900 and width from 62% to 125%, and the width does most of the talking.

| Role | Weight | Width | Size |
|---|---|---|---|
| Site title | 850 | 68% | 46 to 94px |
| Year numbers | 900 | 66% | 60 to 124px |
| Month page titles | 900 | 66% | 64 to 132px |
| Section headings | 850 | 70% | 34 to 60px |
| Month names on sleeves | 800 | 78% | 19px |
| Catalogue numbers | 600 | 118% | 13px |
| Text | 400 | 100% | 16px |

## Motion

There's one moment on load: the record settles and the arm swings from its rest onto the latest month. After that the arm moves quickly when you pick a month. The record only turns while music is playing, at 33⅓ rpm, and the light on it stays still the way it would on a real deck. Where the browser supports it, a month page grows out of the sleeve you tapped.

With reduced motion turned on, the record doesn't turn, the arm doesn't swing and pages open without the morph.

## Accessibility

The arm is a slider for screen readers and keyboards, with month names as its values. Focus shows as a yellow ring with a dark edge, so it's visible on the record and on the page. Everything the record does is also available from the calendar, the buttons and the links, so nothing depends on dragging.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole site: layout, styles and code |
| `fonts/` | Archivo, self-hosted, with its license |
| `icons/` | The favicon and app icons, a record drawn from the 25'26 covers |
| `manifest.webmanifest` | Lets phones add the site to the home screen |
| `og.jpg` | The picture shown when the link is shared |
