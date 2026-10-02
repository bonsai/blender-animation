# Examples

## 10sec-polyhaven.json

A minimal 10-second scene manifest.

The example deliberately uses semantic Poly Haven queries rather than hard-coded asset URLs. The runtime resolves:

1. query -> /search
2. selected asset -> /info/{id}
3. Blender-compatible file -> /files/{id}
4. resolved asset -> Blender MCP / Blender Python
5. motion -> Blender keyframes

This keeps the animation description independent from a particular asset revision.
