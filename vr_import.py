# Import JanusVR from URL/filesystem
import os
import urllib.request as urlreq
import gzip
import bpy
from mathutils import Vector, Matrix
from math import radians
import re
import bs4

def s2v(s):
    return [float(c) for c in s.split(" ")]

def s2p(s):
    v = s2v(s)
    return [v[0], -v[2], v[1]]

def s2lp(s):
    v = s2v(s)
    return [v[0], v[2], v[1]]

def fromFwd(zdir):
    ydir = [0,1,0]
    xdir = Vector(zdir).cross(Vector(ydir))
    mtrx = Matrix([xdir, zdir, ydir])
    return mtrx

def neg(v):
    return [-e for e in v]

def rel2abs(base, path):
    if path.startswith("../"):
        parentdir = base[:-2 if base.endswith("/") else -1].rsplit("/", 1)[0]
        return os.path.join(parentdir, path[3:])

    return path

class AssetObjectObj:

    def __init__(self, basepath, workingpath, tag):
        self.basepath = basepath
        self.workingpath = workingpath
        self.id = tag["id"]
        self.src = tag["src"]
        self.sourcepath = os.path.dirname(self.src)
        self.mtl = tag.attrs.get("mtl", None)
        self.loaded = False
        self.imported = False
        self.objects = []

    def abs_source(self, base, path):
        base = rel2abs(self.basepath, base)
        if path.startswith("/") or path.startswith("http://") or path.startswith("https://"):
            return path
        elif path.startswith("../"):
            return rel2abs(base, path)
        if base.startswith("http://") or base.startswith("https://"):
            return base + "/" + path
        return os.path.join(base, path)

    def abs_target(self, path):
        return os.path.join(self.workingpath, os.path.basename(path))

    # Moves resources to the working directory
    def retrieve(self, path, base=None):
        if base is None:
            base = self.basepath
        source = self.abs_source(base, path)
        print(source)
        target = self.abs_target(path)
        urlreq.urlretrieve(source, target)
        if path.endswith(".gz"):
            with gzip.open(target, 'rb') as infile:
                with open(target[:-3], 'wb') as outfile:
                    outfile.write(infile.read())

            return target[:-3]
        return target

    def load(self):

        if self.loaded:
            return

        self.src = self.retrieve(self.src)
        if self.mtl:
            #mtlpath = os.path.dirname(self.mtl)
            mtlpath = os.path.dirname(self.abs_source(self.basepath,self.mtl))
            self.mtl = self.retrieve(self.mtl)
            print(self.mtl)
            imgfiles = []
            with open(self.mtl, "r") as mtlfile:
                #imgfiles = re.findall(r"\b\w*\.(?:jpg|gif|png)", mtlfile.read())
                imgfiles = re.findall(r"((\S*?)\.(?:jpg|jpeg|gif|png))", mtlfile.read())

            for imgfile in imgfiles:
                self.retrieve(imgfile[0], mtlpath)

            # rewrite mtl to point to local file
            with open(self.abs_target(self.mtl), "r") as mtlfile:
                file = mtlfile.read()
            for imgfile in imgfiles:
                file = file.replace(imgfile[0], os.path.basename(imgfile[0]))
            with open(self.mtl, "w") as mtlfile:
                mtlfile.write(file)
        self.loaded = True

    #An .obj can include multiple objects!
    def instantiate(self, tag):
        print(tag)
        self.load()
        if not self.imported:
            objects = list(bpy.data.objects)
            if self.mtl is not None:
                # rewrite obj to point to correct mtl
                replaced = False
                file = ""
                with open(self.abs_target(self.src), "r") as mtlfile:
                    for line in mtlfile.read().split('\n'):
                        if line[:6] == 'mtllib':
                            file = file + 'mtllib ' + os.path.basename(self.mtl) + '\n'
                            replaced = True
                        else:
                            file = file + line + '\n'
                    if replaced == False:
                        file = 'mtllib ' + os.path.basename(self.mtl) + '\n' + file
                with open(self.abs_target(self.src+"_"+os.path.basename(self.mtl)+".obj"), "w") as mtlfile:
                    mtlfile.write(file)
                bpy.ops.import_scene.obj(filepath=self.src+"_"+os.path.basename(self.mtl)+".obj", axis_up="Y", axis_forward="Z")
            else:
                bpy.ops.import_scene.obj(filepath=self.src, axis_up="Y", axis_forward="Z")
            self.objects = [o for o in list(bpy.data.objects) if o not in objects]
            #obj = bpy.context.selected_objects[0]
            #obj.name = self.id
        else:
            newobj = []
            for obj in self.objects:
                bpy.ops.object.select_pattern(pattern=obj.name)
                bpy.ops.object.duplicate(linked=True)
                newobj.append(bpy.context.selected_objects[0])
            self.objects = newobj

        print(self.objects)
        for obj in self.objects:
            obj.scale = s2v(tag.attrs.get("scale", "1 1 1"))

            if "xdir" in tag.attrs and "zdir" in tag.attrs:
                #Matrix.Rotation(radians(-90.0), 3, 'Y')*
                obj.rotation_euler = (Matrix([s2v(tag["xdir"]), neg(s2v(tag.attrs.get("zdir", "0 0 1"))), s2v(tag.attrs.get("ydir", "0 1 0"))])).to_euler()
            else:
                obj.rotation_euler = fromFwd(neg(s2v(tag.attrs.get("fwd", "0 0 1")))).to_euler()

            obj.location = s2p(tag.attrs.get("pos", "0 0 0"))

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

    for asset in assets[0].findAll("assetobject"):
        #dae might be different!
        #assets with same basename will conflict (e.g. from different domains)
        print(asset)

        if asset["src"].endswith(".obj") or asset["src"].endswith(".obj.gz"):
            jassets[asset["id"]] = AssetObjectObj(basepath, workingpath, asset)
        else:
            continue

    objects = room.findAll("object")
    if objects is None:
        operator.report({"INFO"}, "No objects found")
        return

    for obj in objects:
        asset = jassets.get(obj["id"])
        if asset:
            asset.instantiate(obj)


def load(operator, context, filepath, path_mode="AUTO", relpath="", workingpath="FireVR/tmp"):
    read_html(operator, context.scene, filepath, path_mode, workingpath)
