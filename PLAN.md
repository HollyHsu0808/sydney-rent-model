# sydney-rent-model: plan (draft for review)

This is a local folder. Nothing in it has been pushed. Making it public needs the user's explicit OK.

## 1. Who it is for

**Reader:** Luke Metcalfe (Microburbs) and hiring managers. They should get the point in 2 minutes, then be able to check the details.

**Source:** everything is drawn from the private working repo `HollyHsu0808/microburbs-hackathon-2026`, local folder `Desktop/Microburbs Hackathon`. That repo stays unchanged.

## 2. Story core

1. **The puzzle.** Same building, same bedrooms, yet very different rents. The real dollar gap will come from `public_insights.py`, the within-building spread table.
2. **What others measured.** Other Task 4 teams tested floor level, found about $1–7 a floor, and dropped it.
3. **What the answer is.** It's the view, not the floor. Using NSW LiDAR to measure views, a water view adds 16–19% within the same building. Floor number adds only about 1.2% per 10 floors.
4. **Why you can trust the price.**
   - The model was frozen on 31 Jul. It was then checked on 1,898 real adverts from Aug–Sep: median error $45. On 1,061 October adverts the median error was $40 (v2).
   - Every flat gets an 80% range, and 80.2% of real later adverts fell inside it. The median width is $207.50, or $170 for flats with recent own history.
5. **What is still wrong, stated plainly.** The model reads about $20 high after the cut-off, consistent with Sydney unit rents easing. The ranges miss more often on the low side (14.2%) than the high side (5.5%).

## 3. Repo layout

```
sydney-rent-model/
  README.md          2-minute version: story, 3 numbers, 1 chart, how to run
  REPORT.md / report.html
                     full method, validation, post-cut-off results, limits
  VALIDATION.md      walk-forward protocol, v2 selection gates, lock + one-shot scoring
  src/rents/         model code (from rents-heat/src/rents, organiser-specific helpers removed)
  public-data/_scripts/
                     LiDAR view and public-feature scripts (NSW/ABS/OSM sources)
  synthetic/         synthetic data generator, so tests and a demo run without organiser data
  tests/             test suite (runs on synthetic data)
  figures/           aggregate charts only
  pitch/             45 s pitch script, 3 min demo script, slides
  LICENSE
```

## 4. In / out

**In:**
- Code
- Synthetic data and tests
- Aggregate results: tier tables and coverage tables from `post_eval_v2.md`, the walk-forward summary, the ML benchmark, the baseline ladder
- LiDAR method and aggregate view effects
- Charts built from aggregates

**Out:**
- The organiser CSVs, API pulls, anything under `data_private/`, and the team key
- The per-flat prediction CSV, because it uses organiser-selected ids
- Named-building rents, and any address-level example taken from organiser data
- The local Flat Rent Explorer
- The Codex/Console discussion records. They stay in the private repo.

**Check before any public step:**
1. Grep for gnaf ids, `.env`, key strings, organiser file names and building addresses.
2. Check that the repo is a fresh `git init` with no imported history.
3. Run the tests on synthetic data in a clean clone.

## 5. Build steps

1. Copy the code from `rents-heat/src/rents` and `public-data/_scripts`. Drop the explorer builder, the organiser loaders that only matter on the day, and the hard-coded paths into `data_private`. Run the tests on synthetic data.
2. Write README and REPORT from the numbers in `post_eval_v2.md`, `model-v2/README.md` and the 11-07 validation. Every number gets a source line.
3. Make the figures:
   - view vs floor effect within buildings;
   - baseline ladder (bond $100 → suburb $97 → own history $56 → ours $45);
   - 80% range coverage by tier;
   - the post-cut-off bias.
4. Write the pitch script (45 s) and demo script (3 min). How the videos get made is decided separately.
5. Run the privacy check (section 4), then review it with the user.

## 6. Pitch outline (45 s)

| time | content |
|---|---|
| 0–8 s | The puzzle: same building, same bedrooms, $X apart. |
| 8–20 s | Everyone measured floor level and found nothing; LiDAR shows it's the view (+16–19%). |
| 20–35 s | Frozen before August, checked on real adverts afterwards: $45 median error, and 80% ranges that held 80.2%. |
| 35–45 s | What it means for Microburbs: a per-flat rent with an honest range, ready for the property page. |

## 7. Open points

- The $X gap for the opening line. It needs one run of `public_insights.py` on local data; only the aggregate number leaves the machine.
- Whether to include the 3-minute slides, or rebuild them around the new story.
