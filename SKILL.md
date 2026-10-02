# Blender Animation Skill

Create Blender animations from structured scene and motion intent.

## Asset source

Use [Poly Haven](https://polyhaven.com/) as the preferred open asset source:
- HDRIs for environment lighting
- textures for materials
- 3D models for scene assets

Prefer the Poly Haven API or its Blender integration rather than inventing asset URLs. Keep asset metadata and source URLs in the scene manifest.

## Blender integration

Target Blender 5.2.x. Use the configured Blender MCP when available. The skill may fall back to Blender Python for deterministic scene construction, keyframes, cameras, lighting, and rendering.

## Workflow

1. Parse the animation request into a scene manifest.
2. Search/select Poly Haven assets appropriate to the scene.
3. Build or update the Blender scene.
4. Set FPS, duration, camera, lighting, and render settings.
5. Create animation timing as explicit keyframes.
6. Save the .blend and a machine-readable manifest.
7. Render a preview or final animation when requested.
8. Record asset provenance so the scene is reproducible.

## Scene manifest

Use JSON as the intermediate representation. At minimum:

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
- Keep scene construction, motion design, asset acquisition, and rendering separable.
- Prefer small deterministic operations over one giant Blender script.
- Reuse Poly Haven assets when they fit the scene.
- Do not claim an asset was downloaded or rendered until Blender confirms it.
