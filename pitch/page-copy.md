# Flat by Flat 網頁文案（可直接修改）

改法說明：
- 只改冒號後面的文字，冒號前的欄位名稱（例如 headline:）請不要動。
- {N} 會自動換成「第一次看得到水的樓層」，請保留。
- [Your name]、[email]、[link] 是待填的位置，可以直接換成你的資料。
- 欄位對應網頁：S0 開場、S1 謎題、S2 重建城市、S3 爬大樓、S4 景觀價值、S5 模型、S6 驗證、S7 下一步、S8 結尾。
- 最後的「45-second voiceover」是影片旁白，不會放進網頁。
- 改好存檔後跟我說，我會重新產生網頁。

## S0

eyebrow: A city rebuilt, flat by flat
subtitle: I traced Sydney's views to understand why rents split inside the same building.
meta: [Your name] · City of Sydney rental modelling · Microburbs Hackathon Task 4 follow-up

## S1

eyebrow: One address
headline: The address matches. The asking rents don't.
lede: I found flats sharing a building and bedroom count with asking rents far apart. I wanted to see what the address left out, so I started with the city around them.
number_label: a week apart
note: Largest raw, unadjusted spread in the Jun–Jul 2026 holdout. Same building, 3-bed, 8 flats. Small group; no names.

## S2

eyebrow: Rebuild the city
headline: To look out from every floor, I rebuilt the city.
lede: The scans gave me streets, trees and rooftops. I traced 36 sightlines from each floor, one every 10°, out to 1.5 km in 5 m steps. Each line showed where buildings and trees blocked the view. Then I climbed.
label_4399: residential buildings
label_29970: floors measured
label_36: sightlines per floor
label_79: buildings appearing between surveys
caption: Public NSW surveys, 2013 and 2020, on a 1 m grid. New buildings identified from scan differences.

## S3

eyebrow: Come up with me
headline: At first, the harbour is hidden.
label_floor: Floor
label_water: Directions with water
before_first: Water stays hidden until floor {N}.
after_first: The harbour first appears at floor {N}.
legend_water: Water visible
legend_land: Land visible
legend_tower: This tower
btn_start: Start climbing
btn_running: Climbing
btn_again: Climb again
note: This tower first sees water at floor 9; floor 43 sees it in 15 of 36 directions. Measures describe possible views from a floor; a flat's orientation is unknown.

## S4

eyebrow: Read the pattern
headline: The building anchors the rent. The view helps separate flats.
cap_15_5: of measured floors have water in sight in at least one direction.
cap_plus4: rent associated with water in a quarter of directions, versus none, within the same building.
cap_2912: building groups in the view analysis, covering 22,905 adverts.
note: Within-building estimate, Jun–Jul 2026 holdout. 0.168 log points per full share of water-view directions; no CI yet. “Building first, view second” is my interpretation, not a measured decomposition.

## S5

eyebrow: Follow the evidence
headline: I price the flat from the evidence closest to it.
lede: That became my modelling rule. Start with the flat's own adverts, then its building, then its suburb. Keep the view adjustment inside the building, where the comparison makes sense.
rung1_title: Start with its own adverts
rung1_text: I move past asking rents to the valuation date using a same-flat repeat-rent index.
rung2_title: Check how old they are
rung2_text: I set own history aside after 36 months, so an old advert cannot anchor the estimate indefinitely.
rung3_title: Let neighbouring flats count equally
rung3_text: I use same-building comparables with one flat, one vote. Repeated adverts for one flat cannot dominate.
rung4_title: Adjust views within the building
rung4_text: I apply a small LiDAR view adjustment within the building, using the view measured for each floor.
rung5_title: Widen to the suburb
rung5_text: When closer evidence runs out, I use suburb and bedroom comparisons.

## S6

eyebrow: Frozen, then checked
headline: The next adverts put my estimates to the test.
cap_45: median absolute error per week for unchanged v1 on my 1,898 Aug–Sep adverts.
cap_80_2: of those adverts fell inside exploratory v2's nominal 80% ranges from historical walk-forward errors.
tl1: 31 Jul 2026 · training-advert cut-off
tl2: November · v1 built; Aug–Sep adverts checked
tl3: v2 locked after v1 check; scored once
note: v2 followed v1's scores; it was selected on pre-cut-off walk-forward data, hash-locked and scored once. Own sample; asking rents. Aug–Sep misses were 14.2% below and 5.5% above. Over the 1 Oct–1 Nov extended horizon, v2 coverage was 81.5%. On the same Jun–Jul 2026 holdout, median errors were $45 here versus $46.1 for GBDT on the same features. Dots round the percentages.

## S7

eyebrow: Keep improving
headline: Now I know what to test next.
item1_title: Check every kind of estimate
item1_text: I'll check coverage, width and bias by tier and horizon on a shared evaluation set. Aug–Sep coverage remains inconclusive in each no-own-history tier.
item2_title: Test an adjustment for bias
item2_text: More misses fell below the ranges than above. I'll select a bias adjustment using earlier data and test it on separate data.
item3_title: Put bounds on the view
item3_text: I'll estimate a confidence interval for the view association, then test whether changing building stock helps explain gaps between same-flat growth and suburb medians.

## S8

eyebrow: Let's keep building
headline: I'd like to keep doing this work.
lede: I set the direction and did the modelling for this Task 4 entry. I'm looking for short-term, part-time modelling work, and I'd like to keep improving Flat by Flat with Microburbs.
contact: [email] · [link]

## 45-second voiceover

Same building. Same bedrooms. Why are the rents so far apart?

I rebuilt Sydney from laser scans and traced the view from every floor. Climb this tower and the harbour appears.

I read the pattern as building first, view second. My model starts with a flat's own adverts, then its building and suburb.

Unchanged v1 missed later asking rents by a median forty-five dollars a week. After that check, I locked v2; its nominal eighty-percent ranges covered eighty percent of those adverts.

Next, I'll test bias and range coverage.

I'm looking for short-term, part-time modelling work.
