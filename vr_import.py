# Import JanusVR from URL/filesystem
import os
import urllib.request as urlreq
import bpy
import bs4

def s2v(s):
    return [float(c) for c in s.split(" ")]

def s2p(s):
    v = s2v(s)
    return [v[0], -v[2], v[1]]

def s2lp(s):
    v = s2v(s)
    return [v[0], v[2], v[1]]


def read_html(operator, scene, filepath, path_mode, workingpath):
    #FEATURE import from ipfs://
    if filepath.startswith("http://") or filepath.startswith("https://"):
        splitindex = filepath.rfind("/")
        basepath = filepath[:splitindex+1]
        basename = filepath[splitindex+1:]
    else:
        basepath = "file://" + os.path.dirname(filepath)
        basename = os.path.basename(filepath)
        filepath = "file://" + filepath

    source = urlreq.urlopen(filepath)
    html = source.read()
    soup = bs4.BeautifulSoup(html, "html.parser")

    fireboxrooms = soup.findAll("fireboxroom")

    if fireboxrooms is None:
        operator.report({"ERROR"}, "Could not find the FireBoxRoom tag")
        return

    fireboxroom = fireboxrooms[0]

    rooms = fireboxroom.findAll("room")
    if rooms is None:
        operator.report({"ERROR"}, "Could not find the Room tag")
        return

    room = rooms[0]

    # Reset all changes in case of later error? Undo operator?
    # Prevent having to specify defaults twice? (on external load and addon startup)
    scene.janus_room_gravity = float(room.attrs.get("gravity", 9.8))
    scene.janus_room_walkspeed = float(room.attrs.get("walk_speed", 1.8))
    scene.janus_room_runspeed = float(room.attrs.get("run_speed", 5.4))
    scene.janus_room_jump = float(room.attrs.get("jump_velocity", 5))
    scene.janus_room_clipplane[0] = float(room.attrs.get("near_dist", 0.0025))
    scene.janus_room_clipplane[1] = float(room.attrs.get("far_dist", 500))
    scene.janus_room_teleport[0] = float(room.attrs.get("teleport_min_dist", 5))
    scene.janus_room_teleport[1] = float(room.attrs.get("teleport_min_dist", 100))
    scene.janus_room_defaultsounds = bool(room.attrs.get("default_sounds", True))
    scene.janus_room_cursorvisible = bool(room.attrs.get("cursor_visible", True))
    scene.janus_room_fog = bool(room.attrs.get("fog", False))
    scene.janus_room_fog_density = float(room.attrs.get("fog_density", 500))
    scene.janus_room_fog_start = float(room.attrs.get("fog_start", 500))
    scene.janus_room_fog_end = float(room.attrs.get("fog_end", 500))
    scene.janus_room_fog_col = s2v(room.attrs.get("fog_col", "100 100 100"))
    scene.janus_room_locked = bool(room.attrs.get("locked", False))

    jassets = {}

    assets = fireboxroom.findAll("assets")
    if assets is None:
        operator.report({"INFO"}, "No assets found")
        return

    #reuse and rename exportpath as working directory?
    for asset in assets[0].findAll("assetobject"):
        #make and object class, then obj.import()?
        #dae might be different!
        #assets with same basename will conflict (e.g. from different domains)

        if not asset["src"].endswith(".obj"):
            continue

        print(asset)
        jassets[asset["id"]] = [asset["src"], asset.attrs.get("mtl", None)]
        fobj = open(os.path.join(workingpath, os.path.basename(asset["src"])), "wb")
        fobj.write(urlreq.urlopen(os.path.join(basepath, asset["src"]) if not "/" in asset["src"] else asset["src"]).read())
        fobj.close()
        if asset.attrs.get("mtl", None):
            fmtl = open(os.path.join(workingpath, os.path.basename(asset["mtl"])), "wb")
            fmtl.write(urlreq.urlopen(os.path.join(basepath, asset["mtl"]) if not "/" in asset["mtl"] else asset["mtl"]).read())
            fmtl.close()

    objects = room.findAll("object")
    if objects is None:
        operator.report({"INFO"}, "No objects found")
        return

    for obj in objects:
        srcfile = jassets[obj["id"]][0]
        if srcfile.endswith(".obj"):
            bpy.ops.import_scene.obj(filepath=os.path.join(workingpath, srcfile if not "/" in srcfile else os.path.basename(srcfile)))

def load(operator, context, filepath, path_mode="AUTO", relpath="", workingpath="FireVR/tmp"):
    read_html(operator, context.scene, filepath, path_mode, workingpath)
