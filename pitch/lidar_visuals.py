"""LiDAR visuals for the Flat by Flat deck. Public data only (NSW LiDAR, OSM); no rents, no names.
V1 hero render, V2 sightline fans (low vs high floor), V3 water directions by floor, V4 new buildings 2013->2020.
Low memory: decimated reads for city-wide images, windowed reads for the fans."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd, rasterio, shapely
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
from rasterio.features import rasterize
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, LinearSegmentedColormap

PD = Path(r"C:/Users/c931u/Desktop/Microburbs Hackathon/public-data")
sys.path.insert(0, str(PD / "_scripts"))
import lidar_precompute as L

OUT = Path(r"C:/Users/c931u/Desktop/sydney-rent-model/figures"); OUT.mkdir(parents=True, exist_ok=True)
RAS = PD / "_derived" / "lidar_rasters"
NAVY = "#0E2A3B"; TEAL = "#2AA3B5"; SAND = "#E0A458"; GREY = "#8FA3AF"
BID = 328169331                    # tall residential tower near the harbour (no name used anywhere)
tp = Transformer.from_crs("EPSG:4326", "EPSG:7856", always_xy=True)

bf = pd.read_csv(PD / "_derived" / "buildings_features.csv")
lb = pd.read_parquet(PD / "_derived" / "lidar_buildings.parquet")
fv = pd.read_parquet(PD / "_derived" / "lidar_floor_view.parquet")


def water_shapes():
    out = []
    dw = json.load(open(PD / "osm" / "osm_water_bbox.json", encoding="utf-8"))
    for e in dw["elements"]:
        if e.get("tags", {}).get("natural") == "coastline":
            continue
        rings = []
        if e["type"] == "way" and "geometry" in e and len(e["geometry"]) >= 4:
            rings.append(e["geometry"])
        elif e["type"] == "relation":
            rings += [m["geometry"] for m in e.get("members", []) if m.get("role") == "outer" and "geometry" in m and len(m["geometry"]) >= 4]
        for gg in rings:
            try:
                p = shapely.Polygon([tp.transform(g["lon"], g["lat"]) for g in gg])
                if p.is_valid and p.area > 0:
                    out.append(p)
            except Exception:
                pass
    return out


WSH = water_shapes()


def read(name, bounds=None, scale=1):
    with rasterio.open(RAS / f"{name}.tif") as s:
        win = from_bounds(*bounds, s.transform) if bounds else None
        if scale == 1:
            a = s.read(1, window=win)
            tr = s.window_transform(win) if win else s.transform
        else:
            h, w = s.height // scale, s.width // scale
            a = s.read(1, out_shape=(h, w), resampling=Resampling.average)
            tr = s.transform * s.transform.scale(s.width / w, s.height / h)
    return a.astype(np.float32), tr


def water_mask(dem, ndsm, tr):
    m = rasterize(((g, 1) for g in WSH), out_shape=dem.shape, transform=tr, fill=0, dtype="uint8").astype(bool)
    return m | ((dem <= 0.5) & (np.abs(ndsm) < 1.0))


def shaded(dsm, ndsm, wat, res, vmax=150):
    """Colour LiDAR render: buildings and trees coloured by height (classic LiDAR ramp), lit dark ground, blue water."""
    ls = LightSource(azdeg=315, altdeg=40)
    hs = ls.hillshade(np.nan_to_num(dsm), vert_exag=2.5, dx=res, dy=res)
    h = np.clip(np.nan_to_num(ndsm), 0, None)
    rgb = np.array([0.20, 0.22, 0.24]) * (0.55 + 0.8 * hs[..., None])
    cm = LinearSegmentedColormap.from_list("lidar", ["#2B83BA", "#00B8A9", "#7CCF5B", "#F6D743", "#F79A3E", "#E8453C", "#FF5FA2"])
    t = np.clip((h - 3.0) / vmax, 0, 1) ** 0.5
    m = h > 3.0
    col = cm(t)[..., :3] * (0.55 + 0.6 * hs[..., None])
    rgb[m] = col[m]
    wr = wat | (((np.nan_to_num(dsm) - np.nan_to_num(ndsm)) <= 1.2) & (h < 2.0))   # render-only: fill no-return holes over the harbour
    rgb[wr] = np.array([0.07, 0.24, 0.52]) * (0.85 + 0.3 * hs[wr, None])
    return np.clip(rgb, 0, 1)


def save(fig, name):
    fig.savefig(OUT / name, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
    plt.close(fig); print("saved", OUT / name)


# ---------------- V1 hero: whole grid, 2 m
dsm, tr = read("dsm_2020", scale=2); dem, _ = read("dem_2020", scale=2); nd = dsm - dem
wat = water_mask(dem, nd, tr)
img = shaded(dsm, nd, wat, 2.0)
H, W = img.shape[:2]
# 16:9 crop centred on the CBD / harbour
cx, cy = tp.transform(151.207, -33.875)
c0 = int((cx - tr.c) / tr.a); r0 = int((cy - tr.f) / tr.e)
cw = min(W, 4000 // 2 * 2); ch = int(cw * 9 / 16)
x0 = int(np.clip(c0 - cw // 2, 0, W - cw)); y0 = int(np.clip(r0 - ch // 2, 0, H - ch))
fig = plt.figure(figsize=(16, 9), facecolor=NAVY); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.imshow(img[y0:y0 + ch, x0:x0 + cw], interpolation="lanczos")
save(fig, "v1_city_lidar.png")
del dsm, dem, nd, wat, img

# ---------------- V4 new buildings 2013 -> 2020 (same base, highlight)
new = lb[lb.new_2013_2020].merge(bf[["osm_type", "osm_id", "lon", "lat"]], on=["osm_type", "osm_id"])
print("new buildings:", len(new))
dsm, tr = read("dsm_2020", scale=4); dem, _ = read("dem_2020", scale=4); nd = dsm - dem
wat = water_mask(dem, nd, tr)
img = shaded(dsm, nd, wat, 4.0) * 0.6
fig = plt.figure(figsize=(10, 12.5), facecolor=NAVY); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.imshow(img, interpolation="lanczos")
xs, ys = tp.transform(new.lon.values, new.lat.values)
cc = (np.array(xs) - tr.c) / tr.a; rr = (np.array(ys) - tr.f) / tr.e
ax.scatter(cc, rr, s=260, color=SAND, alpha=0.18, linewidths=0)
ax.scatter(cc, rr, s=40, color=SAND, edgecolors="white", linewidths=0.6)
ax.set_xlim(0, img.shape[1]); ax.set_ylim(img.shape[0], 0)
save(fig, "v4_new_buildings.png")
del dsm, dem, nd, wat, img

# ---------------- V2 sightline fans from one tower, low vs high floor
row = bf.index[bf.osm_id == BID][0]
polys = L.load_footprints(bf.iloc[[row]].reset_index(drop=True), tp)
g = polys[0][0]; c = g.centroid
R = 1700.0
bounds = (c.x - R, c.y - R, c.x + R, c.y + R)
dsm, tr = read("dsm_2020", bounds); dem, _ = read("dem_2020", bounds); nd = dsm - dem
wat = water_mask(dem, nd, tr)
base = shaded(dsm, nd, wat, 1.0) * 0.75
b = lb[lb.osm_id == BID].iloc[0]
ground = float(b.ground_z_2020); h = float(b.h_p90_2020)
fl = fv[fv.osm_id == BID].sort_values("floor")
n_fl = int(fl.floor.max()) + 1
ang = np.linspace(0, 2 * np.pi, L.N_RAYS, endpoint=False)
d = np.arange(L.STEP, L.MAX_D, L.STEP, dtype=np.float32)
X = c.x + np.cos(ang)[:, None] * d; Y = c.y + np.sin(ang)[:, None] * d
own = shapely.contains_xy(g, X, Y)
col = ((X - tr.c) / tr.a).astype(int); rw = ((Y - tr.f) / tr.e).astype(int)
Z = dsm[rw, col].copy(); Z[own] = -1e3; WAT = wat[rw, col] & ~own


def vis_at(floor):
    E = ground + L.FLOOR_H * floor + L.EYE_H
    A = (Z - E) / d
    pm = np.maximum.accumulate(A, axis=1)
    pm = np.concatenate([np.full((A.shape[0], 1), -np.inf, np.float32), pm[:, :-1]], axis=1)
    return A >= pm - 1e-6


lo, hi = 2, n_fl - 1
fig, axs = plt.subplots(1, 2, figsize=(16, 8), facecolor=NAVY)
for ax, f in zip(axs, (lo, hi)):
    v = vis_at(f)
    ax.imshow(base, interpolation="lanczos"); ax.axis("off")
    for k in range(L.N_RAYS):
        vw = v[k] & WAT[k]; vl = v[k] & ~WAT[k] & ~own[k]
        ax.scatter(col[k][vl], rw[k][vl], s=1.2, color="#DCE6EA", alpha=0.55, linewidths=0)
        ax.scatter(col[k][vw], rw[k][vw], s=3.0, color=TEAL, alpha=0.95, linewidths=0)
    gx, gy = g.exterior.xy
    ax.fill((np.array(gx) - tr.c) / tr.a, (np.array(gy) - tr.f) / tr.e, color=SAND, zorder=5)
    wf = float(fl[fl.floor == f].water_view_frac.iloc[0])
    ax.set_title(f"Floor {f}  ·  water in {round(wf * 36)} of 36 directions", color="white", fontsize=18, pad=10, loc="left")
fig.subplots_adjust(wspace=0.03, left=0.01, right=0.99, top=0.92, bottom=0.01)
save(fig, "v2_sightlines_low_high.png")
print("tower floors:", n_fl, "low floor water frac", float(fl[fl.floor == lo].water_view_frac.iloc[0]), "high", float(fl[fl.floor == hi].water_view_frac.iloc[0]))

# ---------------- V3 water directions by floor for the same tower
fig, ax = plt.subplots(figsize=(6, 8), facecolor=NAVY); ax.set_facecolor(NAVY)
n = (fl.water_view_frac * 36).round().astype(int).values
ax.barh(fl.floor.values, n, color=[TEAL if x > 0 else "#34566A" for x in n], height=0.8)
ax.set_xlim(0, 36); ax.set_xlabel("directions with a water view (of 36)", color="white", fontsize=13)
ax.set_ylabel("floor", color="white", fontsize=13)
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(colors="#B8C4CC", labelsize=11)
first = int(fl[fl.water_view_frac > 0].floor.min())
ax.axhline(first - 0.5, color=SAND, lw=1.2, ls="--"); ax.text(35.5, first - 1.6, f"water first visible: floor {first}", color=SAND, ha="right", fontsize=12)
save(fig, "v3_water_by_floor.png")
print("first water floor", first)
