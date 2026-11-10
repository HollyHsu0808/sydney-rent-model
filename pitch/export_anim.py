"""Export ray data (all floors, 36 rays) + base images for the animated HTML. Public data only."""
import json, io, base64
import numpy as np
exec(open("lidar_visuals.py", encoding="utf-8").read().split("# ---------------- V1 hero")[0])
from PIL import Image
# tower window (same as V2)
row = bf.index[bf.osm_id == BID][0]
polys = L.load_footprints(bf.iloc[[row]].reset_index(drop=True), tp)
g = polys[0][0]; c = g.centroid; R = 1700.0
bounds = (c.x - R, c.y - R, c.x + R, c.y + R)
dsm, tr = read("dsm_2020", bounds); dem, _ = read("dem_2020", bounds); nd = dsm - dem
wat = water_mask(dem, nd, tr)
base = shaded(dsm, nd, wat, 1.0)
b = lb[lb.osm_id == BID].iloc[0]; ground = float(b.ground_z_2020)
fl = fv[fv.osm_id == BID].sort_values("floor"); n_fl = int(fl.floor.max()) + 1
ang = np.linspace(0, 2*np.pi, L.N_RAYS, endpoint=False)
d = np.arange(L.STEP, L.MAX_D, L.STEP, dtype=np.float32)
X = c.x + np.cos(ang)[:, None]*d; Y = c.y + np.sin(ang)[:, None]*d
own = shapely.contains_xy(g, X, Y)
col = ((X - tr.c)/tr.a).astype(int); rw = ((Y - tr.f)/tr.e).astype(int)
Z = dsm[rw, col].copy(); Z[own] = -1e3; WAT = wat[rw, col] & ~own
floors = []
for f in range(n_fl):
    E = ground + L.FLOOR_H*f + L.EYE_H
    A = (Z - E)/d
    pm = np.maximum.accumulate(A, axis=1)
    pm = np.concatenate([np.full((A.shape[0], 1), -np.inf, np.float32), pm[:, :-1]], axis=1)
    v = (A >= pm - 1e-6) & ~own
    rays = []
    for k in range(L.N_RAYS):
        runs = []; cur = None
        for j in range(len(d)):
            if v[k, j]:
                t = 1 if WAT[k, j] else 0
                if cur and cur[2] == t and cur[1] == j - 1: cur[1] = j
                else:
                    if cur: runs.append(cur)
                    cur = [j, j, t]
            else:
                if cur: runs.append(cur); cur = None
        if cur: runs.append(cur)
        rays.append(runs)
    wdir = int(round(float(fl[fl.floor == f].water_view_frac.iloc[0]) * 36))
    floors.append({"w": wdir, "r": rays})
gx, gy = g.exterior.xy
fp = [[round((x - tr.c)/tr.a, 1), round((y - tr.f)/tr.e, 1)] for x, y in zip(gx, gy)]
data = {"px": base.shape[1], "step": 5, "ang0": 0, "cx": round((c.x - tr.c)/tr.a, 1), "cy": round((c.y - tr.f)/tr.e, 1), "fp": fp, "floors": floors}
im = Image.fromarray((base*255).astype("uint8")).resize((1400, 1400), Image.LANCZOS)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=82); tower_b64 = base64.b64encode(buf.getvalue()).decode()
data["scale"] = 1400 / base.shape[1]
# hero: reuse saved V1 png, compress
hero = Image.open(OUT / "v1_city_lidar.png").convert("RGB").resize((2000, 1125), Image.LANCZOS)
buf = io.BytesIO(); hero.save(buf, "JPEG", quality=80); hero_b64 = base64.b64encode(buf.getvalue()).decode()
nb = Image.open(OUT / "v4_new_buildings.png").convert("RGB"); nb = nb.resize((900, int(900*nb.height/nb.width)), Image.LANCZOS)
buf = io.BytesIO(); nb.save(buf, "JPEG", quality=80); nb_b64 = base64.b64encode(buf.getvalue()).decode()
json.dump({"rays": data, "tower": tower_b64, "hero": hero_b64, "newb": nb_b64}, open("anim_assets.json", "w"))
print("floors", n_fl, "water dirs by floor", [f["w"] for f in floors])
print("sizes KB", len(json.dumps(data))//1024, len(tower_b64)//1024, len(hero_b64)//1024, len(nb_b64)//1024)
