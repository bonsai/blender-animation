# Blender MCP Connection

How the GUI, the MCP server, the animation manifest, Poly Haven, and the Blender
scene connect. Target: **Blender 5.2.2 LTS (Windows)**.

```
Blender 5.2.2 GUI
  -> MCP (mcp-for-blender)
  -> animation manifest (JSON)
  -> Poly Haven assets
  -> Blender scene (.blend) -> keyframes -> render
```

## 1. MCP source

- Repository: https://github.com/ahujasid/mcp-for-blender
- Legacy repository: https://github.com/ahujasid/blender-mcp (redirects to the above)
- Website: https://mcp-for-blender.com/
- PyPI package: `mcp-for-blender` (legacy name `blender-mcp` still works)
- Author: Siddharth Ahuja — MIT license

The MCP is two parts:

1. **Blender addon** (`addon.py` / installed as `blender_mcp.py`) — opens a socket
   server inside Blender and executes commands.
2. **MCP server** (`mcp-for-blender`) — speaks MCP to the LLM client and connects
   to the addon socket.

## 2. Installed on this machine

Confirmed from the running setup:

| Item | Value |
| --- | --- |
| Addon path | `%APPDATA%\Blender Foundation\Blender\5.2\scripts\addons\blender_mcp.py` |
| Addon name | `MCP for Blender` |
| Addon version | `1.8` |
| Addon protocol | `13` |
| Socket host | `localhost` |
| Socket port | `9876` |
| Blender | `5.2.2 LTS` |
| uv | `0.11.21` |

Verify the port is open after starting the addon server:

```powershell
python3 -c "import socket; s=socket.socket(); s.settimeout(1); print('open' if s.connect_ex(('localhost',9876))==0 else 'closed')"
```

## 3. Setup steps

1. **Install uv** (once). `uv --version` should print a version.
2. **Install the addon**:

   ```powershell
   uvx mcp-for-blender install-addon
   ```

   This writes `blender_mcp.py` into the Blender 5.2 addons folder and keeps a
   `.bak` of any file it replaces.
3. **Enable the addon** in Blender: `Edit -> Preferences -> Add-ons ->
   Interface: MCP for Blender`.
4. **Start the socket server**: in the 3D viewport press `N`, open the
   `MCP for Blender` tab, click `Start MCP Server`. The port `9876` opens.
5. **Point the MCP client at the server** (see section 4).
6. **Verify** with the socket check in section 2, then ask the client to read the
   scene (`get_scene_info`).

Only run one MCP server instance at a time against a given Blender instance.

## 4. Client configuration

opencode (`~/.config/opencode/opencode.json`):

```json
{
  "mcp": {
    "blender": {
      "type": "local",
      "command": ["uvx", "mcp-for-blender"],
      "enabled": true,
      "environment": {
        "BLENDER_HOST": "localhost",
        "BLENDER_PORT": "9876"
      }
    }
  }
}
```

Claude Code / Codex:

```shell
claude mcp add blender uvx mcp-for-blender
codex mcp add blender -- uvx mcp-for-blender
```

Cursor / VS Code / Antigravity use `{"command":"uvx","args":["mcp-for-blender"]}`
with `BLENDER_HOST` / `BLENDER_PORT` env vars.

## 5. Pipeline mapping

| Stage | Where it lives | Notes |
| --- | --- | --- |
| Blender 5.2.2 GUI | Blender desktop app | User enables addon, starts MCP server |
| MCP transport | `mcp-for-blender` + addon socket | `localhost:9876`, protocol 13 |
| Animation manifest | `scene/*.json` in this repo | Deterministic JSON data layer |
| Poly Haven assets | Poly Haven API / Blender integration | CC0 HDRIs, textures, models; record provenance |
| Blender scene | MCP tools or Blender Python | Build objects, materials, camera, lights |
| Keyframes | MCP tools or Blender Python | Compile manifest motion into explicit keyframes |
| Render | Blender render / MCP | Preview or final; only claim success after Blender confirms |

## 6. Principles

- The manifest is the source of truth; Blender is the execution layer.
- Prefer MCP calls for interactive/GUI work and Blender Python for deterministic,
  reproducible batches.
- Keep asset acquisition and scene construction separable; never invent asset URLs.
- Do not claim a download or render succeeded until Blender confirms it.
