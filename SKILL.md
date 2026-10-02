# Blender Animation Skill

Create Blender animations from structured scene and motion intent.

## Asset source

Use [Poly Haven](https://polyhaven.com/) as the preferred open asset source:
- HDRIs for environment lighting
- textures for materials
- 3D models for scene assets

Use the official [Poly-Haven/Public-API](https://github.com/Poly-Haven/Public-API) as the asset discovery boundary. The live API is at https://api.polyhaven.com.

### Asset resolution pipeline

Resolve semantic animation intent into real assets in this order:

1. `GET /search?q=<query>&t=<type>&limit=<n>` — find candidates.
2. `GET /info/<id>` — obtain canonical asset metadata.
3. `GET /files/<id>` — select an actual downloadable Blender-compatible file.
4. Store the resolved asset ID, file format, resolution, URL, and provenance in the animation manifest.
5. Hand the resolved asset to Blender MCP or Blender Python.

Never invent a Poly Haven download URL. Prefer the file URL returned by `/files/{id}`.

See [polyhaven/API.md](polyhaven/API.md) for the adapter contract.

## Blender integration

Target Blender 5.2.x. Use the configured Blender MCP when available. The skill may fall back to Blender Python for deterministic scene construction, keyframes, cameras, lighting, and rendering.

## Workflow

1. Parse the animation request into a scene manifest.
2. Convert asset intent into Poly Haven search queries.
3. Search Poly Haven and select candidate assets.
4. Resolve metadata and file inventory for selected assets.
5. Build or update the Blender scene.
6. Set FPS, duration, camera, lighting, and render settings.
7. Create animation timing as explicit keyframes.
8. Save the .blend and a machine-readable manifest.
9. Render a preview or final animation when requested.
10. Record asset provenance so the scene is reproducible.

## Scene manifest

Use JSON as the intermediate representation. Validate against [schema/animation-manifest.schema.json](schema/animation-manifest.schema.json).

At minimum:

```json
{
  "fps": 24,
  "duration_seconds": 10,
  "scene": {},
  "assets": [],
  "characters": [],
  "camera": {},
  "lighting": {},
  "motion": [],
  "render": {}
}
```

Motion should be expressed as semantic actions plus frame/time boundaries, then compiled into Blender keyframes.

## Principles

- JSON is the animation data layer; Blender is the execution/rendering layer.
- Poly Haven API is the asset discovery and provenance layer.
- Keep scene construction, motion design, asset acquisition, and rendering separable.
- Prefer small deterministic operations over one giant Blender script.
- Reuse Poly Haven assets when they fit the scene.
- Do not claim an asset was downloaded or rendered until Blender confirms it.


## Runtime

The reference runtime is split into two deterministic stages:

### 1. Resolve Poly Haven assets

```bash
python scripts/resolve_polyhaven.py examples/10sec-polyhaven.json
```

This produces a resolved manifest containing the selected Poly Haven asset IDs,
metadata, file URL, checksum, and API provenance.

### 2. Compile the scene in Blender

```bash
blender --background --python scripts/build_blender_scene.py -- examples/10sec-polyhaven.resolved.json
```

The Blender compiler imports resolved model assets and converts semantic motion
actions into keyframes. Blender MCP can use the same resolved manifest as its
machine-readable input when operating interactively.

The runtime deliberately does not guess asset URLs and does not make Poly Haven
API calls from Blender scene-building logic.
