# blender-animation

A skill for creating Blender animations from structured scene and motion data.

## Stack

- Blender 5.2.x
- Blender MCP
- Blender Python
- Poly Haven for CC0 environment, texture, and 3D assets

## Concept

```
request
  -> animation manifest
  -> Poly Haven assets
  -> Blender scene
  -> keyframes
  -> render
```

The repository keeps the animation logic separate from Blender execution so the same animation description can be inspected, generated, and reproduced.

## Asset source

Poly Haven: https://polyhaven.com/

The skill prefers Poly Haven assets and records their provenance in the animation manifest.

## Skill

See [SKILL.md](SKILL.md).
