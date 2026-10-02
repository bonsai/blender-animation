# blender-animation

A skill for creating Blender animations from structured scene and motion data.

## Stack

- Blender 5.2.x
- Blender MCP: [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender)
- Blender Python
- Poly Haven
- Poly-Haven Public API

## Connection

GUI + MCP setup (Blender 5.2.2 GUI -> MCP -> animation manifest -> Poly Haven ->
Blender scene) is documented in [CONNECTION.md](CONNECTION.md).

## Concept

```
request
  -> animation manifest
  -> Poly Haven semantic search
  -> asset metadata
  -> Blender-compatible file
  -> Blender MCP / Python
  -> keyframes
  -> render
```

The repository keeps animation intent, asset discovery, and Blender execution separate so the same animation description can be inspected, generated, and reproduced.

## Poly Haven

Use the official Poly Haven API for asset discovery:

- API: https://api.polyhaven.com
- Source: https://github.com/Poly-Haven/Public-API
- Adapter contract: [polyhaven/API.md](polyhaven/API.md)

The runtime should resolve `query -> search -> asset info -> file inventory` rather than embedding guessed asset URLs.

## Example

See [examples/10sec-polyhaven.json](examples/10sec-polyhaven.json) for a minimal 10-second animation manifest.

## Skill

See [SKILL.md](SKILL.md).
