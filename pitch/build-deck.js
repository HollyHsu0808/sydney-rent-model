// Flat by Flat — pitch deck (pptxgenjs, 16:9 = 10 x 5.625 in)
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("C:/Users/c931u/.claude/skills/synced/ff4b7929-00f3-4102-ae26-b22e1cd4c9a8_e2a436a0-2451-4c7a-81b5-1660409ee7e7/pptx/scripts/apply_theme.js");

const OUT = "C:/Users/c931u/Desktop/sydney-rent-model/pitch/flat-by-flat-deck.pptx";

const HEX = { ink: "1B2631", navy: "0E2A3B", mist: "EEF3F5", teal: "1F7A8C", sand: "D9A05B", dot: "B8C4CC", muted: "5D6D7E", sea: "7FB7C2", deep: "2E4A5C" };
const THEME = {
  name: "Flat by Flat",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: HEX.ink, lt1: "FFFFFF", dk2: HEX.navy, lt2: HEX.mist,
    accent1: HEX.teal, accent2: HEX.sand, accent3: HEX.dot, accent4: HEX.muted, accent5: HEX.sea, accent6: HEX.deep,
    hlink: HEX.teal, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Flat by Flat";
pres.subject = "Sydney asking rents, with ranges checked on later adverts";
pres.author = "[Your name]";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const W = 10, H = 5.625, M = 0.55;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  margin: [0.5, 0.55, 0.5, 0.55],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.32, w: W - 2 * M, h: 0.75, fontSize: 26, bold: true, color: C.text2, align: "left", valign: "top", margin: 0 }, text: "" } },
    { text: { text: "Flat by Flat · follow-up to Microburbs AI Hackathon Task 4", options: { x: M, y: H - 0.38, w: 6, h: 0.25, fontSize: 9, color: C.accent4, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.5, y: H - 0.38, w: 0.5, h: 0.25, fontSize: 9, color: C.accent4, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 1.45, w: 5.6, h: 1.0, fontSize: 44, bold: true, color: C.background1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: M, y: 2.55, w: 5.6, h: 1.3, fontSize: 18, color: C.accent5, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});

// ---------- helpers ----------
const txt = (slide, text, o) => slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: C.text1, valign: "top" }, o));
function dot(slide, x, y, d, color, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0.5 }, objectName: name });
}
function num(slide, x, y, n, fill = C.accent1) {
  dot(slide, x, y, 0.42, fill, `step ${n}`);
  txt(slide, String(n), { x, y, w: 0.42, h: 0.42, fontSize: 15, bold: true, color: C.background1, align: "center", valign: "middle" });
}
function card(slide, x, y, w, h, name, fill = C.background2) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.1, objectName: name });
}
function stat(slide, x, y, w, big, label, color = C.accent1, bigSize = 36) {
  txt(slide, big, { x, y, w, h: 0.62, fontSize: bigSize, bold: true, color, fontFace: "Cambria" });
  txt(slide, label, { x, y: y + 0.64, w, h: 0.5, fontSize: 12, color: C.accent4 });
}
// 10x10 dot grid: 6 above (grey), 80 inside (teal), 14 below (sand)
function dotGrid(slide, x0, y0, step, d, faint = false) {
  for (let i = 0; i < 100; i++) {
    const r = Math.floor(i / 10), c = i % 10;
    let col = i < 6 ? C.accent3 : i < 86 ? C.accent1 : C.accent2;
    if (faint) col = C.accent6;
    dot(slide, x0 + c * step, y0 + r * step, d, col, `dot ${i + 1}`);
  }
}

// ---------- 1. title ----------
pres.addSection({ title: "Opening" });
let s = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" });
s.addText("Flat by Flat", { placeholder: "title" });
s.addText("Sydney asking rents, with ranges checked on later adverts", { placeholder: "body" });
txt(s, "65,777 City of Sydney flats · follow-up to Microburbs AI Hackathon Task 4 · [Your name] · Nov 2026", { x: M, y: H - 0.75, w: 6.2, h: 0.4, fontSize: 11, color: C.accent3 });
dotGrid(s, 6.75, 1.25, 0.29, 0.19, false);
s.addNotes("Flat by Flat estimates the next weekly asking rent for every City of Sydney flat, from the flat's own history, then its building, then its suburb. Each estimate comes with a range, and both were scored on adverts dated after the data cut-off.");

// ---------- 2. hook ----------
pres.addSection({ title: "The check" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The check" });
s.addText("Scored on adverts dated after the data cut-off", { placeholder: "title" });
dotGrid(s, M + 0.05, 1.35, 0.3, 0.21);
const lx = M + 0.05, ly = 4.45;
dot(s, lx, ly + 0.04, 0.16, C.accent1, "key inside"); txt(s, "inside the range", { x: lx + 0.22, y: ly, w: 1.3, h: 0.25, fontSize: 10, color: C.accent4 });
dot(s, lx + 1.45, ly + 0.04, 0.16, C.accent2, "key below"); txt(s, "below", { x: lx + 1.67, y: ly, w: 0.6, h: 0.25, fontSize: 10, color: C.accent4 });
dot(s, lx + 2.2, ly + 0.04, 0.16, C.accent3, "key above"); txt(s, "above", { x: lx + 2.42, y: ly, w: 0.6, h: 0.25, fontSize: 10, color: C.accent4 });
stat(s, 4.3, 1.3, 2.4, "$45", "median miss a week, hackathon file unchanged (1,898 Aug–Sep adverts)", C.text2, 40);
stat(s, 7.0, 1.3, 2.4, "80.2%", "of the same adverts fell inside the nominal 80% ranges (CI 78.3–82.2)", C.accent1, 40);
card(s, 4.3, 2.85, 5.15, 1.35, "finding card");
txt(s, [
  { text: "What the check found", options: { bold: true, color: C.text2, breakLine: true } },
  { text: "Misses fall more often below the range (14.2%) than above (5.5%), consistent with rents easing after July. That points to the next fix: a bias adjustment for easing markets.", options: { color: C.text1 } },
], { x: 4.5, y: 2.98, w: 4.8, h: 1.15, fontSize: 13 });
txt(s, "$45: v1, the hackathon submission. Ranges: v2, a revision locked before scoring. My own advert sample via the Microburbs API; asking rents.", { x: 4.3, y: 4.35, w: 5.15, h: 0.45, fontSize: 10, color: C.accent4 });
s.addNotes("I left my hackathon rent model untouched, then scored it on adverts dated after its data cut-off. Median miss on nearly nineteen hundred later adverts: forty-five dollars a week. A revision built on earlier data and locked before scoring adds a nominal eighty-percent range; eighty percent of the same adverts fell inside. And I checked which side the misses fell: more below than above, which tells me exactly what to fix next.");

// ---------- 3. method ----------
pres.addSection({ title: "Method" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
s.addText("Each flat is priced from the best evidence it has", { placeholder: "title" });
const steps = [
  ["Its own past adverts", "Latest same-bedroom advert, moved to today by a same-flat (repeat-rent) index"],
  ["Fresh, or set aside", "Own history older than 36 months is not trusted"],
  ["Its building", "Same bedrooms, latest advert per neighbouring flat: one flat, one vote"],
  ["Its suburb", "Suburb × bedrooms × parking ladder when nothing closer exists"],
];
steps.forEach(([h, b], i) => {
  const y = 1.25 + i * 0.82;
  num(s, M, y, i + 1);
  txt(s, h, { x: M + 0.6, y: y - 0.02, w: 4.6, h: 0.3, fontSize: 15, bold: true, color: C.text2 });
  txt(s, b, { x: M + 0.6, y: y + 0.28, w: 4.6, h: 0.45, fontSize: 12, color: C.text1 });
});
card(s, 6.05, 1.25, 3.4, 1.55, "stat card 1");
stat(s, 6.3, 1.38, 3.0, "75%", "of flats with their own history last advertised over 12 months ago, so the index does real work", C.accent1, 34);
card(s, 6.05, 3.0, 3.4, 1.55, "stat card 2");
stat(s, 6.3, 3.13, 3.0, "84%", "of real asking rents end in 0, so estimates are rounded to $5", C.accent2, 34);
s.addNotes("Flat by Flat starts from each flat's own adverts, updated by how the same flats' rents have moved. If that history is missing or over three years old, it uses other flats in the same building, one vote each, then the suburb.");

// ---------- 4. holdout ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Method" });
s.addText("On the holdout, well ahead of simple baselines", { placeholder: "title" });
s.addChart(pres.charts.BAR, [{ name: "Median absolute error ($/week)", labels: ["NSW bond data", "Suburb median", "Own history + index", "GBDT, same features", "Flat by Flat"], values: [100, 97.2, 56.1, 46.1, 45] }], {
  x: M, y: 1.15, w: 5.6, h: 3.55, barDir: "bar", catAxisOrientation: "maxMin",
  chartColors: [HEX.dot, HEX.dot, HEX.dot, HEX.dot, HEX.teal],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "$0.0", dataLabelFontSize: 12, dataLabelColor: HEX.ink, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, catAxisLabelColor: HEX.ink, catAxisLabelFontFace: "+mn-lt",
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, valAxisMinVal: 0, valAxisMaxVal: 115,
  showLegend: false, showTitle: true, title: "Median absolute error, $ a week", titleFontSize: 12, titleColor: HEX.muted, titleFontFace: "+mn-lt",
  barGapWidthPct: 45,
});
stat(s, 6.6, 1.3, 2.9, "$40", "flats with their own history (2,151 adverts)", C.accent1, 34);
stat(s, 6.6, 2.5, 2.9, "$60", "flats without it (747 adverts)", C.accent2, 34);
stat(s, 6.6, 3.7, 2.9, "R² 0.88", "77% of adverts within $100", C.text2, 28);
txt(s, "Trained on adverts to 31 May 2026; tested on 2,898 adverts, 1 Jun–31 Jul 2026.", { x: M, y: 4.75, w: 5.6, h: 0.3, fontSize: 10, color: C.accent4 });
s.addNotes("On the same 2,898-advert holdout, median error was $45 for this model and $46.1 for the tested GBDT, against $97 for suburb medians and $100 for bond data.");

// ---------- 5. frozen then checked ----------
pres.addSection({ title: "Proof" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Proof" });
s.addText("Frozen at the cut-off, then checked twice", { placeholder: "title" });
const ty = 2.05;
s.addShape(pres.shapes.LINE, { x: M + 0.2, y: ty, w: W - 2 * M - 0.4, h: 0, line: { color: C.accent3, width: 2 }, objectName: "timeline" });
const marks = [
  [M + 0.2, "31 Jul 2026", "Data cut-off for training adverts", C.text2],
  [3.55, "Aug–Sep", "Hackathon file, unchanged", C.accent1],
  [6.75, "1 Oct–1 Nov", "Extended horizon", C.accent1],
];
marks.forEach(([x, h, b, col], i) => {
  dot(s, x - 0.14, ty - 0.14, 0.28, col, `mark ${i + 1}`);
  txt(s, h, { x: x - 0.14, y: ty - 0.72, w: 2.6, h: 0.3, fontSize: 14, bold: true, color: C.text2 });
  txt(s, b, { x: x - 0.14, y: ty + 0.22, w: 2.6, h: 0.3, fontSize: 11, color: C.accent4 });
});
card(s, 3.41, 2.75, 2.95, 1.75, "aug-sep card");
stat(s, 3.6, 2.88, 2.6, "$45", "median miss · 76.9% within $100 · 1,898 adverts in 937 buildings", C.accent1, 36);
card(s, 6.61, 2.75, 2.85, 1.75, "oct card");
stat(s, 6.8, 2.88, 2.5, "$45", "median miss · 78.6% within $100 · 1,061 adverts", C.accent1, 36);
txt(s, [
  { text: "Same file, ", options: { bold: true, color: C.text2 } },
  { text: "no retuning, two later periods, the same median miss.", options: { color: C.text1 } },
], { x: M, y: 2.85, w: 2.65, h: 1.2, fontSize: 14 });
txt(s, "My own sample of later adverts, pulled through the Microburbs API; asking rents.", { x: M, y: 4.62, w: 8.9, h: 0.3, fontSize: 10, color: C.accent4 });
s.addNotes("The hackathon submission's training adverts stop at 31 July 2026. I left the file unchanged and scored it on later adverts: $45 median miss in August and September, and $45 again over the extended horizon to 1 November.");

// ---------- 6. ranges ----------
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Proof" });
s.addText("A locked revision gives every flat a range that held", { placeholder: "title" });
const proto = ["Select on 6 pre-cut-off origins (15,747 adverts)", "One change passes preset gates", "Lock every file by SHA-256 hash", "Score once on later adverts"];
proto.forEach((p, i) => {
  const x = M + i * 2.27;
  card(s, x, 1.2, 2.07, 0.95, `protocol ${i + 1}`, i === 3 ? C.accent1 : C.background2);
  txt(s, p, { x: x + 0.15, y: 1.28, w: 1.8, h: 0.8, fontSize: 12, bold: i === 3, color: i === 3 ? C.background1 : C.text2, valign: "middle" });
  if (i < 3) txt(s, "›", { x: x + 2.07, y: 1.38, w: 0.2, h: 0.5, fontSize: 22, color: C.accent4, align: "center", valign: "middle" });
});
s.addChart(pres.charts.BAR, [{ name: "Share of adverts inside the nominal 80% range", labels: ["Aug–Sep", "1 Oct–1 Nov"], values: [80.2, 81.5] }], {
  x: M, y: 2.35, w: 4.3, h: 2.35, barDir: "col",
  chartColors: [HEX.teal], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0\"%\"", dataLabelFontSize: 12, dataLabelColor: HEX.ink, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 12, catAxisLabelColor: HEX.ink, catAxisLabelFontFace: "+mn-lt",
  valAxisMinVal: 0, valAxisMaxVal: 100, valAxisLabelFontSize: 10, valAxisLabelColor: HEX.muted, valAxisLabelFontFace: "+mn-lt", valGridLine: { color: "DDE4E8", size: 0.5 }, catGridLine: { style: "none" },
  showLegend: false, showTitle: true, title: "Adverts inside the nominal 80% range", titleFontSize: 12, titleColor: HEX.muted, titleFontFace: "+mn-lt", barGapWidthPct: 90,
});
stat(s, 5.3, 2.5, 2.0, "$207.50", "median range width", C.text2, 28);
stat(s, 7.5, 2.5, 2.0, "$170", "with fresh own history", C.accent1, 28);
txt(s, "Ranges come from each evidence tier's historical walk-forward errors. CIs: 78.3–82.2 (Aug–Sep) and 79.2–83.7 (1 Oct–1 Nov). The revision was made after the first check, selected on pre-cut-off data only, then scored once.", { x: 5.3, y: 3.75, w: 4.15, h: 0.95, fontSize: 10, color: C.accent4 });
s.addNotes("After the first check I built a revision using only pre-cut-off data, under gates fixed in advance, locked it by hash and scored it once. Its nominal 80% ranges contained 80.2% of August–September adverts and 81.5% over the extended horizon.");

// ---------- 7. next ----------
pres.addSection({ title: "Next" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Next" });
s.addText("What I would build next", { placeholder: "title" });
const nexts = [
  ["Ranges by tier and horizon", "Check coverage, width and bias for own-history, building and suburb estimates on a shared evaluation set"],
  ["Adjust for easing markets", "Misses lean below the range; a market-trend adjustment after the cut-off is the clear next fix"],
  ["Test two promising leads", "LiDAR water views (about +4% for a quarter of view directions) and same-flat growth vs suburb medians"],
];
nexts.forEach(([h, b], i) => {
  const x = M + i * 3.05;
  card(s, x, 1.25, 2.85, 2.55, `next ${i + 1}`);
  num(s, x + 0.25, 1.45, i + 1, i === 1 ? C.accent2 : C.accent1);
  txt(s, h, { x: x + 0.25, y: 2.05, w: 2.4, h: 0.6, fontSize: 15, bold: true, color: C.text2 });
  txt(s, b, { x: x + 0.25, y: 2.7, w: 2.4, h: 1.5, fontSize: 12, color: C.text1 });
});
txt(s, "Leads are preliminary: the view effect has no CI yet; Zetland's suburb median rose 46.7% from Jul 2019 to Jul 2026 while the same flats rose 29.8% (indicative).", { x: M, y: 4.0, w: 8.9, h: 0.4, fontSize: 10, color: C.accent4 });
s.addNotes("The next step I'd like to take is checking those ranges on a shared evaluation set, by evidence tier and by horizon, and adding a market-trend adjustment for the period after the cut-off.");

// ---------- 8. close ----------
pres.addSection({ title: "Close" });
s = pres.addSlide({ masterName: "DARK", sectionTitle: "Close" });
s.addText("A rent, a range, and a measured hit rate", { placeholder: "title" });
s.addText("Looking for short-term part-time modelling work · [email] · [link]", { placeholder: "body" });
dotGrid(s, 6.75, 1.25, 0.29, 0.19, false);
s.addNotes("A rent, a range, and a measured hit rate. I'm looking for short-term part-time modelling work and would welcome a conversation.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("wrote", OUT);
})();
