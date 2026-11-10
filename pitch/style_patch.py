"""Visual patches on top of the base template (legend, tower contrast, canvas rays, hero wrap)."""
R = [
(".legend { display: flex; flex-wrap: wrap; gap: 8px 18px; font: 400 12px/1.4 var(--mono); color: var(--mist); }\n.legend i { display: inline-block; width: 18px; height: 3px; vertical-align: middle; margin-right: 7px; border-radius: 2px; }",
 ".legend { display: flex; flex-wrap: wrap; gap: 10px; font: 500 13.5px/1.2 var(--mono); color: var(--fog); }\n.legend span { display: inline-flex; align-items: center; gap: 10px; padding: 8px 14px 8px 12px; background: #17384B; border: 1px solid #3A6378; border-radius: 999px; }\n.legend i { display: inline-block; width: 28px; height: 6px; border-radius: 3px; box-shadow: 0 0 10px currentColor; }"),
('<span><i style="background:var(--sea)"></i>', '<span><i style="background:var(--sea);color:var(--sea)"></i>'),
('<span><i style="background:#cfdbe1"></i>', '<span><i style="background:#F2F6F8;color:rgba(242,246,248,.5)"></i>'),
('<span><i style="background:var(--sand)"></i>', '<span><i style="background:var(--sand);color:var(--sand)"></i>'),
(".tower .fl { fill: #16364A; transition: fill .25s; }", ".tower .fl { fill: #2B5267; stroke: #4A7488; stroke-width: .6; transition: fill .25s; }"),
(".tower .wb { fill: var(--sea); opacity: .22; transition: opacity .25s; }", ".tower .wb { fill: #3E7F8C; opacity: .55; transition: opacity .25s; }\n.tower .wb.past { fill: var(--sea); }"),
(".tower .t { font: 500 11px var(--mono); fill: var(--mist); }", ".tower .t { font: 500 12px var(--mono); fill: var(--fog); }"),
('ctx.fillStyle = "rgba(6,20,28,.45)"; ctx.fillRect(0, 0, W, W);', 'ctx.fillStyle = "rgba(6,20,28,.38)"; ctx.fillRect(0, 0, W, W);'),
('ctx.strokeStyle = w ? "rgba(53,180,198,.95)" : "rgba(207,219,225,.42)";', 'ctx.strokeStyle = w ? "rgba(80,230,255,1)" : "rgba(255,255,255,.85)";'),
('ctx.lineWidth = w ? lw * 2.2 : lw;', 'ctx.lineWidth = w ? lw * 2.8 : lw * 1.3;'),
(".hero .sub { font-size: clamp(17px, 2vw, 24px); color: var(--fog); max-width: 30ch; }", ".hero .sub { font-size: clamp(17px, 2vw, 24px); color: var(--fog); max-width: 46ch; text-wrap: balance; }\n.hero .meta { max-width: none; }"),
("p { margin: 0; max-width: 62ch; }", "p { margin: 0; max-width: 62ch; text-wrap: pretty; }"),
(".hero::after { content: \"\"; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(7,24,34,.92) 0%, rgba(7,24,34,.55) 42%, rgba(7,24,34,0) 70%); pointer-events: none; }",
 ".hero::after { content: \"\"; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(7,24,34,.96) 0%, rgba(7,24,34,.9) 38%, rgba(7,24,34,.35) 62%, rgba(7,24,34,0) 78%); pointer-events: none; }"),
]
def patch(s):
    for a, b in R:
        assert s.count(a) == 1, "style patch missing: " + a[:60]
        s = s.replace(a, b)
    return s
