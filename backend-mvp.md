# Official statement (condensed)
Develop an interactive visualization and simulation tool that uses real data from NASA APIs to model asteroid impact scenarios, predict consequences, and evaluate potential mitigation strategies. Model environmental and geological impacts (e.g., tsunami zones, seismic activity, topography).

## API Endpoints
| Method | Endpoint                | Params | Description                                                                 | Status Codes                              |
|--------|--------------------------|--------|-----------------------------------------------------------------------------|-------------------------------------------|
| POST   | `/api/simulations`         | check inputs    | Compute simulation params (hash normalized inputs to get id, check DB if id already exists, if it doesn't - compute params for that id) and return id, input params, computed params. | 200 OK; 400 Bad Request; 422 Unprocessable Entity |
| GET    | `/api/simulations/{id}`    | id (path) | Fetch simulation params by ID. Returns stored input params + computed params. | 200 OK; 304 Not Modified; 404 Not Found    |

# Input

The backend receives these params:
- asteroid diameter
- asteroid material density (frontend can add basic presets to make it easier to use e.g. rock, crystal, iron, etc.)
- asteroid velocity before entering Earth's atmosphere
- entry angle (from horizontal)
- azimuth
- aim point (lat, lon) - surface reference used to place the spawn point directly above at 120 km and to build the local ENU frame; physics then decides the actual airburst/impact location (if entry angle is set to 90 then the impact/airburst will occur at aim point)
- target surface (water or land for simplicity, can use cesium `sampleTerrain`)

# Output
- energy released (megatons TNT) 
- crater diameter (transient) (m)
- crater diameter & depth (final) (m)
- radius for each blast ring:
  - severe structural damage (>=70kPa) (m)
  - heavy damage (35-70kPa) (m)
  - moderate damage (20-35kPa) (m)
  - light damage (10-20kPa) (m)
  - minor damage (3-10kPa) (m)
- atmospheric entry: 
  - the asteroid begins to break up at an altitude of h1 (m)
  - the asteroid reaches peak energy at h2 (m)
  - the asteroid airbursts at h3 (or surface impact) (m)
- trajectory forward (into the earth)
- trajectory backward (for deflection computation)

example jsons in `examples/`.

need physicists help for trajectory/deflection








