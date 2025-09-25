# Official statement (condensed)
Develop an interactive visualization and simulation tool that uses real data from NASA APIs to model asteroid impact scenarios, predict consequences, and evaluate potential mitigation strategies. Model environmental and geological impacts (e.g., tsunami zones, seismic activity, topography).

# API Endpoints

| API Endpoint             | Method | Description                                                                 | Request Body (example)                                                                                     | Response (example)                                                                                          | Status Codes |
|--------------------------|--------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|--------------|
| `/api/simulations`       | POST   | Normalize inputs → compute unique ID → check DB → create or reuse simulation. | `{ "lat": 52.1, "lon": 21.0, "size_m": 500, "speed_kms": 20.0, "impact_angle_deg": 90 }`                   | **If exists:** `{"id":"sim_xxx"}` + `Location: /api/simulations/sim_xxx`<br>**If new:** `{"id":"sim_xxx","inputs":{...},"outputs":{...}}` | 303 See Other (exists)<br>201 Created (new)<br>400/422 (invalid input) |
| `/api/simulations/<id>`  | GET    | Fetch a simulation by ID. Returns inputs + outputs stored in DB.            | N/A                                                                                                        | `{"id":"sim_xxx","inputs":{...},"outputs":{...}}`                                                            | 200 OK<br>304 Not Modified (with ETag)<br>404 Not Found |

# Example front end routes (up to front end devs to decide what to actually use in reality)
| Frontend Route        | Method | Description                                             | Returns  | Status Codes     |
|-----------------------|--------|---------------------------------------------------------|----------|------------------|
| `/`                   | GET    | Landing page with form to collect parameters & location | HTML/JS  | 200 OK           |
| `/simulations/<id>`   | GET    | Viewer page; calls `GET /api/simulations/<id>` to render| HTML/JS  | 200 OK<br>404 Not Found |


1. `/` gets location, asteroid characteristics from user input,then does `POST /api/simulations`
2. `/api/simulations` normalizes input (defaults, rounding, sorted keys, normalized units) -> computes unique id by hashing the normalized JSON -> looks for that id in db:
	1. if id exists in db -> return `303 See other` with `Location: /api/simulations/<id>`
	2. if id doesn't exist in db -> run simulation, store the parameters and simulation calculations as a record keyed by id inside the db, return `201 Created` with `Location: /api/simulations/<id>`
3. Client: upon 303/201/200 -> redirect to `/simulations/<id>` which fetches `GET /api/simulations/<id>`

# Parameters
Parameters depend on what we want to compute, so let's decide that first.\
METRICS:
- estimated deaths
- energy released upon impact (compare with bombs in the past)
- deflection expenses and evaluation if its worth it (maybe if it costs 9 gorillion dollars and the asteroid isnt that big and hits the atlantic ocean then nobody will care)

GEOJSON:
- crater
- blast rings
- evacuation zones
- earthquake zones with probability
- forest fires with probability
- tsunami zones


>[!NOTE] ^ cia tsg sarasas dalyku kuriuos galim idet, parasyk savo idejas ir td reiks nusprest kurie is sito saraso mvp, kurie additional features, ir tada bus galima nusprest kokiu inputu prasysim is userio

# Backend parts
`handle_simulation()` is a view that implements server side workflow of the "simulate" button. It's urlconf'ed to `/api/simulations` here's a high level overview:
```python
@api_view (["POST"])
def handle_simulation(request):
	raw_params = request.data
	normalized_params = normalize_params(raw_params)
	id = compute_id(normalized_params)
	
	if (simulation_exists(id)):
		return Response(
			{"id": id},
			status=303,
			headers={"Location": f"/api/simulations/{id}"}
		)
	else:
		outputs = run_simulation(normalized_params)
		write_simulation_to_db(id, normalized_params, outputs)
		return Response(
			{"id": id, "inputs": normalized_params, "outputs": outputs},
			status=201,
			headers={"Location": f"/api/simulations/{id}"}
		)
```
## `normalize_params()`
a function that takes all parameters relevant to the simulation (JSON or already parsed dict) and returns a normalized JSON, so that we can create a unique id for that unique set of parameters.

normalization should:
- fill in defaults where user didn't provide something
- validate types
- normalize units to SI (maybe not needed depending on frontend)
- round floats to some agreed upon precision so that we can get away without recomputing same simulations with just tiny differences in float (though will need to put approximation error percentage in the docs - physicist's job)
- anything else?

## `compute_id()`
 a function that takes in a json and hashes it using sha256 (deterministic, collision resistant, fast) to return a hash which we will use as an id.

## `simulation_exists(id)`
a function that returns true if an id is in the database, false if not

## `run_simulation(normalized_params)`
a function that takes in the normalized JSON and returns JSON (metrics, trajectory), GEOJSON (craters, etc.)

## `write_simulation_to_db()` or `persist_data()`
a function that takes in `id, normalized_params, outputs` and writes them to the database

# TODO
split `run_simulation()` into more parts (like trajectory computation, metrics computation, geojson computation, etc.?) and document what we might need to begin creating them

# Data
NASA NEO API provides asteroid characteristics (e.g. size, velocity, orbit)
The U.S. Geological Survey (USGS) offers environmental and geological datasets (e.g., topography, seismic activity, tsunami zones) critical for modeling impact effects.

# Questions
## What are the judges actually looking for?
I think they're looking for an idea that:
- is feasible, can actually be executed and extended
- scientific correctness (use of reserach papers, lots of quantitative figures, for example detailing the estimations made when creating the app and the resulting approximation errors, etc.)
- appeal to a wide audience (at the end of the day they probably just want to familiarize as many people with the problem as possible to generate funding for their departament, so how marketable our app is also might play a role)
- robustness and error handling - how reliable is the app really?
- story telling and the pitch are probably as important as the app itself

### Does "Impactor-2025" even exist?
I didn't manage to find the neo_id for an asteroid called "Impactor-2025" in either of the APIS (NEO or JPL Horizons). From the information I gathered, it's likely that "Impactor-2025" is a made up asteroid purely for hackathon purposes. Since there is no information on its orbital data - there is no way to simulate it realistically - we will need to model characteristics of an asteroid that crashes into the earth ourselves.

### What do we actually need to simulate in 3D?
Since we're aiming to build a collision simulator we only need to simulate asteroids that are going to crash into the earth, which means we won't be using NEO API for asteroid inputs. **We just need an interface where the user can enter params which are used simulate a guaranteed crash into the earth (on a predetermined path from what I imagine) and provide the consequences**. We will also need to simulate deflection, but it really depends on how we want to go about it.

##### Why?
No asteroids from the NEO database are on track to hitting the earth, meaning the problem-setters probably aren't expecting us to simulate 3D trajectories for any given asteroid (further clarified by the fact that it's not possible to reconstruct an asteroid's full state (initial and velocity vectors) from the data available in NEO database, although there is JPL Horizons API if we ever wanted to do that). It would be a really nice twist though since I think most teams will just do 2D maps, but we need to ensure we get the expected part right too.

### Which asteroids to include?
what are the minimum charactersistics for an asteroid to be considered dangerous (before entering earth's atmosphere)? compare costs of deflection and when its worth to actually deflect it.

### When should simulation stop?
I think simulation should stop either when the asteroid crashes into the Earth (after crash animation, zoom) or when the asteroid comes to the closest point with the Earth (zoom also, red/yellow line marking the distance and the distance written in km on top of the line (relevant for deflection).

### Difference between `neo_id` and `asteroid_id` in the NEO API
Use `neo_id` when focusing on objects that can potentially enter Earth's neighborhood (neo - near earth object).
Use `asteroid_id` when referring to an asteroid within the solar system (more general)
Since in our usecase we're only worried about potential treats to Earth, use `neo_id`.

### How to implement deflection?
_Some definitions before reading this:_
**Geocentric** - measured with relation to the Earth (Earth is the centre (0, 0, 0)).

**Geocentric state vector** - a vector that represents the complete physical state of an object (typically a satellite or a spacecraft), by specifying its position and velocity relative to the Earth's center at a given time, usually within a non-rotating geocentric equatorial coordinate system. It is defined by a position vector (r) and a velocity vector (v), often expressed as a six-element column matrix, that fully describes the object's orbital dynamics.

idea: we only know the last **geocentric state vector** of the asteroid before impact since thats the info we get from input, so we could probably reconstruct the trajectory backwards in time and try to calculate when we would need to crash into the asteroid with a spacecraft to make a change in velocity big enough to offset the asteroids path from hitting the earth. this sounds really computationally expensive, and I'm really not sure if it's feasible, but if we managed to do this then it would be pretty impressive and would justify the long load time IMO.

any other ideas for anything welcome
