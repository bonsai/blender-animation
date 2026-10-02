"""Compile a resolved animation manifest into a Blender scene.

Run inside Blender 5.2.x:
  blender --background --python scripts/build_blender_scene.py -- resolved.json

The script intentionally keeps asset resolution outside Blender. Poly Haven
URLs are resolved first by scripts/resolve_polyhaven.py.
"""
from __future__ import annotations

import json
import math
import os
import sys
import urllib.request

import bpy
from mathutils import Vector


def load_manifest():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if not argv:
        raise SystemExit("manifest path required after --")
    with open(argv[0], encoding="utf-8") as f:
        return json.load(f)


def frame(manifest, seconds):
    return round(seconds * manifest["fps"]) + 1


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def import_asset(asset, root):
    url = asset["url"]
    local = os.path.join(root, os.path.basename(url.split("?")[0]))
    if not os.path.exists(local):
        urllib.request.urlretrieve(url, local)

    fmt = asset.get("file_format", "")
    if fmt == "blend":
        with bpy.data.libraries.load(local, link=False) as (data_from, data_to):
            data_to.collections = data_from.collections
        for collection in data_to.collections:
            if collection:
                bpy.context.scene.collection.children.link(collection)
        return bpy.context.scene.objects[-1] if bpy.context.scene.objects else None

    if fmt == "gltf":
        bpy.ops.import_scene.gltf(filepath=local)
    elif fmt == "fbx":
        bpy.ops.import_scene.fbx(filepath=local)
    elif fmt == "usd":
        bpy.ops.wm.usd_import(filepath=local)
    else:
        return None

    return bpy.context.object


def setup_scene(manifest):
    scene = bpy.context.scene
    scene.render.engine = manifest.get("render", {}).get("engine", "BLENDER_EEVEE_NEXT")
    scene.render.resolution_x, scene.render.resolution_y = manifest.get("render", {}).get("resolution", [1920, 1080])
    scene.render.fps = manifest["fps"]
    scene.frame_start = 1
    scene.frame_end = frame(manifest, manifest["duration_seconds"])

    camera_data = bpy.data.cameras.new("AnimationCamera")
    camera = bpy.data.objects.new("AnimationCamera", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.location = manifest.get("camera", {}).get("location", [7, -7, 4])
    look_at(camera, manifest.get("camera", {}).get("look_at", [0, 0, 0]))

    return scene, camera


def add_orbit(obj, start_frame, end_frame, degrees):
    obj.rotation_mode = "XYZ"
    obj.rotation_euler.z = 0
    obj.keyframe_insert("rotation_euler", frame=start_frame, index=2)
    obj.rotation_euler.z = math.radians(degrees)
    obj.keyframe_insert("rotation_euler", frame=end_frame, index=2)


def build(manifest):
    scene, camera = setup_scene(manifest)
    root = os.path.join(os.path.dirname(bpy.data.filepath) or os.getcwd(), "assets")
    os.makedirs(root, exist_ok=True)

    objects = {}
    for asset in manifest.get("assets", []):
        if asset.get("type") == "models":
            objects[asset["id"]] = import_asset(asset, root)

    for motion in manifest.get("motion", []):
        if motion["action"] == "orbit":
            target = objects.get(motion.get("target"))
            if target:
                add_orbit(
                    target,
                    frame(manifest, motion["start"]),
                    frame(manifest, motion["end"]),
                    motion.get("params", {}).get("degrees", 360),
                )

    scene["bonsai_animation_manifest"] = manifest
    output = manifest.get("render", {}).get("blend_output", "animation.blend")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(output))


if __name__ == "__main__":
    build(load_manifest())
