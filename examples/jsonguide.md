# JSON structure
```json
{
  "id": "sha256:...",
  "map": {
    "center": {"lat": 0, "lon": 0},
    "crater_transient_diameter_m": null,
    "crater_final_diameter_m": null,
    "rings": [
      {"id": "kpa70", "threshold_kpa": 70, "radius_m": 0}
    ]
  },
  "panel": {
    "energy_released_megatons": 0,
    "crater_final": {"formed": false, "diameter_m": null, "depth_m": null},
    "rings": [
      {"threshold_kpa": 70, "radius_m": 0, "arrival_time_s": 0, "delta_to_next_s": null, "population": 0, "estimated_deaths": 0, "blurb": ""}
    ],
    "entry": {"h1_breakup_begin_m": null, "h2_peak_energy_m": null, "h3_airburst_or_surface_m": 0, "terminal_type": "airburst"},
    "totals": {"total_estimated_deaths": 0}
  },
  "meta": {"units": "SI; lat/lon degrees WGS-84", "notes": [], "version": "1"}
}
```

# `map`

### `map.center` `{lat:number, lon:number}`

Ground point that centers all blast rings (and the crater, if any).

### `map.crater_transient_diameter_m` `number|null`

Transient (initial) crater **diameter** right after excavation.
*Airburst:* `null`. *Impact:* number (meters).

### `map.crater_final_diameter_m` `number|null`

Final crater **diameter** after collapse/modification.
*Airburst:* `null`. *Impact:* number (meters).

### `map.rings` `Array<{id:string, threshold_kpa:number, radius_m:number}>`

Concentric blast circles, ordered from **highest** `threshold_kpa` to **lowest**. Draw each as a circle centered at `map.center` with radius `radius_m` (meters).

* `id` — stable identifier for UI toggles (e.g., `"kpa70"`).
* `threshold_kpa` — peak overpressure threshold this ring represents (e.g., 70, 50, 35, 20, 10, 3).
* `radius_m` — great‑circle radius on the ground from `map.center`.

---

# `panel`

### `panel.energy_released_megatons` `number`

Total energy coupled to air/surface (MT TNT).

### `panel.crater_final` `{formed:boolean, diameter_m:number|null, depth_m:number|null}`

UI summary of crater outcome.

* *Airburst:* `formed=false`, `diameter_m=null`, `depth_m=null`.
* *Impact:* `formed=true`, both metrics set.

### `panel.rings` `Array<…>` (one item per overpressure band)

Detailed data for the side panel, matching `map.rings` but with timing and population.

Per-ring fields:

* `threshold_kpa` — must match the map ring’s threshold.
* `radius_m` — same value as in `map.rings` (keeps panel independent).
* `arrival_time_s` — time from terminal event until the shock reaches `radius_m`.
* `delta_to_next_s` — time gap from this ring’s arrival to the **next** ring’s arrival (outer band). `null` for the last ring.
* `population` — estimated people in the **annulus** between this ring and the next (outer) ring.
* `estimated_deaths` — estimated fatalities within that annulus.
* `blurb` — short tooltip text (e.g., "Severe structural damage", "Most windows shatter").

### `panel.entry` `{…}` — key altitudes (meters) and terminal type

* `h1_breakup_begin_m` — altitude where fragmentation begins (dynamic‑pressure trigger). `null` if no breakup.
* `h2_peak_energy_m` — altitude of maximum energy deposition rate. `null` if not applicable.
* `h3_airburst_or_surface_m` — airburst altitude (>0) **or** 0 for surface impact.
* `terminal_type` — `"airburst" | "impact"`.

### `panel.totals.total_estimated_deaths` `number`

Sum over `panel.rings[].estimated_deaths`.

---

# `meta`

### `meta.units` `string`

Human‑readable units statement (e.g., "SI; lat/lon degrees WGS‑84").

### `meta.notes` `string[]`

Optional free‑text notes for UI/QA (e.g., "Airburst case (no crater)", "Arrival times measured from terminal event time").

### `meta.version` `string`

Schema/version tag (e.g., `"1"`).

---

# Validation hints (frontend)

* If `panel.entry.terminal_type == "airburst"`:

  * `map.crater_transient_diameter_m` and `map.crater_final_diameter_m` **must be `null`**.
  * `panel.crater_final.formed` is **false**.
  * `panel.entry.h3_airburst_or_surface_m` **> 0**.

* If `panel.entry.terminal_type == "impact"`:

  * `map.crater_*_diameter_m` may be numbers; `panel.crater_final.formed` is **true**.
  * `panel.entry.h3_airburst_or_surface_m` **== 0**.
