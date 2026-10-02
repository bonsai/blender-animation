# Poly Haven API adapter

bonsai/blender-animation uses the official public API maintained by Poly Haven.

Official API:
- Base: https://api.polyhaven.com
- Source: https://github.com/Poly-Haven/Public-API
- OpenAPI: https://api.polyhaven.com/api-docs/swagger.json

## Useful endpoints

### Search

GET /search?q=<query>&t=<type>&limit=<n>

Use semantic + keyword search to turn animation intent into asset candidates.

Supported types:
- hdris
- textures
- models
- all

### Asset metadata

GET /info/<id>

Use the returned metadata as the canonical asset record.

### File inventory

GET /files/<id>

Use this to choose an actual Blender-compatible file. Prefer:
- models: blend or gltf
- textures: blend or gltf when a packaged material is useful
- HDRIs: the hdri file at the required resolution

## Adapter contract

The animation skill should produce an asset record like:

    {
      "id": "prop",
      "type": "models",
      "query": "decorative object",
      "source": "polyhaven",
      "polyhaven_id": "resolved-by-search",
      "file_format": "blend",
      "resolution": "2k",
      "url": "resolved-from-files"
    }

Do not invent a download URL. Resolve it from /files/<id>.

The API is free to use for personal and commercial purposes. When building on the live API, follow Poly Haven's current Terms of Service, including the required "Powered by Poly Haven" credit for API-powered applications.
