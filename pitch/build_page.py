"""Put Astra's copy (astra-copy-codex.md) into story_template.html verbatim, then rebuild the page."""
import json, re, html
import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:/Users/c931u/Desktop/sydney-rent-model/pitch/page-copy.md"
txt = open(SRC, encoding="utf-8").read()
C = {}
sec = None
for line in txt.splitlines():
    m = re.match(r"## (S\d)\s*$", line)
    if m: sec = m.group(1); continue
    if line.startswith("## "): sec = None; continue
    m = re.match(r"([a-z0-9_]+): (.*?)\s*$", line)
    if sec and m: C[f"{sec}.{m.group(1)}"] = m.group(2)
e = lambda k: html.escape(C[k], quote=False)

import style_patch
s = style_patch.patch(open("story_template.pre-astra.html", encoding="utf-8").read())
def rep(old, new):
    global s
    assert s.count(old) == 1, ("not unique/missing", old[:80], s.count(old))
    s = s.replace(old, new)

# S0
rep('<div class="eyebrow rise">City of Sydney · NSW LiDAR 2020 · 1 m grid</div>', f'<div class="eyebrow rise">{e("S0.eyebrow")}</div>')
rep('<p class="sub rise d3">City of Sydney asking rents, with ranges checked on later adverts.</p>', f'<p class="sub rise d3">{e("S0.subtitle")}</p>')
rep('<p class="meta rise d3">65,777 flats · follow-up to Microburbs AI Hackathon Task 4 · [Your name]</p>', f'<p class="meta rise d3">{e("S0.meta")}</p>')
# S1
rep('<div class="eyebrow">The puzzle</div>', f'<div class="eyebrow">{e("S1.eyebrow")}</div>')
rep('<h2>Same building. Same bedrooms. Very different rents.</h2>', f'<h2>{e("S1.headline")}</h2>')
rep("<p class=\"lede\">Suburb medians can't explain that, and neither can a floor number. To find out what can, I needed to know what every flat looks out on.</p>", f'<p class="lede">{e("S1.lede")}</p>')
rep('$1,000<small>a week apart</small>', f'$1,000<small>{e("S1.number_label")}</small>')
rep('Largest raw gap between asking rents in one building, same bedroom count (3-bed, 8 flats), Jun–Jul 2026 adverts. Unadjusted; small groups; buildings not named.', e("S1.note"))
# S2
rep('<div class="eyebrow">Rebuilding the city</div>', f'<div class="eyebrow">{e("S2.eyebrow")}</div>')
rep('<h2>I rebuilt the city from laser scans and traced the view from every floor.</h2>', f'<h2>{e("S2.headline")}</h2>')
rep('Two public NSW LiDAR surveys, 2013 and 2020, at one metre. From each floor of every residential building I cast 36 sightlines, one every 10°, out to 1.5 km in 5 m steps. Towers and trees block them. Water and parks are recorded where a line reaches them.', e("S2.lede"))
rep('<div class="lbl">residential buildings</div>', f'<div class="lbl">{e("S2.label_4399")}</div>')
rep('<div class="lbl">floors measured</div>', f'<div class="lbl">{e("S2.label_29970")}</div>')
rep('<div class="lbl">sightlines per floor</div>', f'<div class="lbl">{e("S2.label_36")}</div>')
rep('<div class="lbl">buildings that appeared 2013→2020</div>', f'<div class="lbl">{e("S2.label_79")}</div>')
rep('New buildings found by comparing the two surveys, not from records. The whole precompute runs in under three minutes on a laptop.', e("S2.caption"))
# S3
rep('<div class="eyebrow">Climb one tower</div>', f'<div class="eyebrow">{e("S3.eyebrow")}</div>')
rep('<h2>The view opens up floor by floor.</h2>', f'<h2>{e("S3.headline")}</h2>')
rep('<div class="eyebrow">Floor</div>', f'<div class="eyebrow">{e("S3.label_floor")}</div>')
rep('<div class="eyebrow">Directions with water in sight</div>', f'<div class="eyebrow">{e("S3.label_water")}</div>')
rep('<div class="first" id="firstNote">Water first comes into sight on floor 9.</div>', f'<div class="first" id="firstNote">{e("S3.after_first").replace("{N}", "9")}</div>')
rep('water in line of sight</span>', f'{e("S3.legend_water")}</span>')
rep('land in line of sight</span>', f'{e("S3.legend_land")}</span>')
rep('the tower</span>', f'{e("S3.legend_tower")}</span>')
rep('<button id="play" type="button">Climb</button>', f'<button id="play" type="button">{e("S3.btn_start")}</button>')
rep('One residential tower near the harbour, shown as a location only. Views are per floor, because the direction a flat faces is unknown. Sources: NSW Spatial Services LiDAR (CC BY), OpenStreetMap water (ODbL).', e("S3.note"))
js = lambda k: json.dumps(C[k])
bf, af = C["S3.before_first"].split("{N}"), C["S3.after_first"].split("{N}")
rep('"Below floor " + FIRST + ": no water in any direction." : "Water first comes into sight on floor " + FIRST + "."',
    f'{json.dumps(bf[0])} + FIRST + {json.dumps(bf[1])} : {json.dumps(af[0])} + FIRST + {json.dumps(af[1])}')
rep('btn.textContent = "Climb again"', f'btn.textContent = {js("S3.btn_again")}')
rep('btn.textContent = "Climbing…"', f'btn.textContent = {json.dumps(C["S3.btn_running"] + "…")}')
rep('btn.textContent = "Climb"; draw();', f'btn.textContent = {js("S3.btn_start")}; draw();')
# S4
rep('<div class="eyebrow">What the view is worth</div>', f'<div class="eyebrow">{e("S4.eyebrow")}</div>')
rep('<h2>The building sets most of the price. The view separates flats inside it.</h2>', f'<h2>{e("S4.headline")}</h2>')
rep('<p>of measured floors can see water in at least one direction.</p>', f'<p>{e("S4.cap_15_5")}</p>')
rep('<p>more rent, within the same building, for water in a quarter of the directions.</p>', f'<p>{e("S4.cap_plus4")}</p>')
rep('<p>buildings compared from the inside, across 22,905 adverts.</p>', f'<p>{e("S4.cap_2912")}</p>')
rep('Within-building estimate on the Jun–Jul 2026 holdout: 0.168 log points per full share of water directions; no confidence interval yet. Reading it as "building first, view second" is an interpretation of this small coefficient beside the strong same-building comparables, not a measured decomposition.', e("S4.note"))
# S5
rep('<div class="eyebrow">How a rent is built</div>', f'<div class="eyebrow">{e("S5.eyebrow")}</div>')
rep('<h2>Each flat is priced from the best evidence it has.</h2>', f'<h2>{e("S5.headline")}</h2>')
rep("That finding shaped the model. Price the flat from its own history when it is fresh, then from its building, then its suburb, and use the view only to adjust within the building.", e("S5.lede"))
old_rungs = [
 '<h3>Its own past adverts</h3><p>The latest same-bedroom advert, moved to today by a same-flat repeat-rent index.</p>',
 '<h3>Only while it is fresh</h3><p>Own history older than 36 months is set aside. 75% of flats with history last advertised over a year ago.</p>',
 '<h3>Its building</h3><p>Same bedrooms, latest advert per neighbouring flat: one flat, one vote.</p>',
 "<h3>Its view, inside the building</h3><p>A small LiDAR adjustment for the difference between this flat's floor and its neighbours'.</p>",
 '<h3>Its suburb</h3><p>Suburb, bedrooms and parking, when nothing closer exists. Rounded to $5, as 84% of real asking rents end in 0.</p>']
for i, o in enumerate(old_rungs, 1):
    rep(o, f'<h3>{e(f"S5.rung{i}_title")}</h3><p>{e(f"S5.rung{i}_text")}</p>')
# S6
rep('<div class="eyebrow">Frozen, then checked</div>', f'<div class="eyebrow">{e("S6.eyebrow")}</div>')
rep('<h2>Scored on adverts dated after its data cut-off.</h2>', f'<h2>{e("S6.headline")}</h2>')
rep('median miss a week: the hackathon file, unchanged, on 1,898 Aug–Sep adverts in 937 buildings', e("S6.cap_45"))
rep('of the same adverts fell inside the nominal 80% ranges (CI 78.3–82.2)', e("S6.cap_80_2"))
def tl(k):
    t = C[k]
    if " · " in t:
        a, b = t.split(" · ", 1); return f"<b>{html.escape(a)}</b>{html.escape(b)}"
    return f"<b>{html.escape(t)}</b>"
rep('<b>31 Jul 2026</b>data cut-off', tl("S6.tl1"))
rep('<b>Aug–Sep</b>$45 · 76.9% within $100', tl("S6.tl2"))
rep('<b>1 Oct–1 Nov</b>$45 · extended horizon', tl("S6.tl3"))
rep('$45 is v1, the hackathon submission. The ranges are v2, a revision made after that check, selected on pre-cut-off walk-forward data only, locked by hash, scored once; 81.5% covered over 1 Oct–1 Nov. Misses fall more often below the range (14.2%) than above (5.5%), consistent with rents easing after July. Own sample of later adverts via the Microburbs API; asking rents. On the Jun–Jul holdout: $45 against $46.1 for gradient-boosted trees on the same features, $97 for suburb medians.', e("S6.note"))
# S7
rep("<div class=\"eyebrow\">What I'd build next</div>", f'<div class="eyebrow">{e("S7.eyebrow")}</div>')
rep('<h2>Three next steps.</h2>', f'<h2>{e("S7.headline")}</h2>')
old_next = [
 '<h3>Ranges by evidence and horizon</h3><p>Check coverage, width and bias separately for own-history, building and suburb estimates, on a shared evaluation set.</p>',
 '<h3>A trend adjustment after the cut-off</h3><p>Misses lean below the range. A market-trend adjustment for the months after the data stops is the clear next fix.</p>',
 '<h3>Views with confidence</h3><p>Put a confidence interval on the view effect, then test whether same-flat growth and suburb medians diverge where new towers rose.</p>']
for i, o in enumerate(old_next, 1):
    rep(o, f'<h3>{e(f"S7.item{i}_title")}</h3><p>{e(f"S7.item{i}_text")}</p>')
# S8
rep('<section class="ask">\n  <div class="wrap stack">\n    <div class="eyebrow">Flat by Flat</div>', f'<section class="ask">\n  <div class="wrap stack">\n    <div class="eyebrow">{e("S8.eyebrow")}</div>')
rep('<h2>A rent, a range, and a measured hit rate.</h2>', f'<h2>{e("S8.headline")}</h2>')
rep("I set the direction and did the modelling for this Task 4 entry, and I want to keep improving it. I'm looking for short-term part-time modelling work.", e("S8.lede"))
rep('<p class="line">[email] · [link]</p>', f'<p class="line">{e("S8.contact")}</p>')

open("story_template.html", "w", encoding="utf-8").write(s)
a = json.load(open("anim_assets.json"))
t = s.replace("__HERO__", a["hero"]).replace("__NEWB__", a["newb"]).replace("__TOWER__", a["tower"]).replace("__RAYS__", json.dumps(a["rays"], separators=(",", ":")))
open(r"C:/Users/c931u/Desktop/sydney-rent-model/pitch/flat-by-flat-story.html", "w", encoding="utf-8").write(t)
print("applied", len(C), "fields")
