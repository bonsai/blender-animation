# Runtime

## Resolve assets

Run outside Blender:

    python scripts/resolve_polyhaven.py examples/10sec-polyhaven.json

This produces:

    examples/10sec-polyhaven.resolved.json

The resolver uses the official Poly Haven API and records the selected asset,
file URL, checksum, and API provenance.

## Build the Blender scene

Run with Blender 5.2.x:

    blender --background --python scripts/build_blender_scene.py -- examples/10sec-polyhaven.resolved.json

Asset acquisition is deliberately outside the animation manifest authoring step.
That keeps the manifest stable while allowing Poly Haven's catalog to change.
