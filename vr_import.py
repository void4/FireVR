# Import JanusVR from URL/filesystem+
# TODO include dependencies directly in addon
from bs4 import BeautifulSoup
import urllib

def s2v(s):
    return [float(c) for c in s.split(" ")]

def s2p(s):
    v = s2v(s)
    return [v[0], -v[2], v[1]]

def s2lp(s):
    v = s2v(s)
    return [v[0], v[2], v[1]]

def read_html(scene, filepath, path_mode):
    source = urllib.urlopen(filepath)
    html = source.read()

    soup = BeautifulSoup(html)

    # Case sensitive!
    room = soup.find_one("fireboxroom")
    assets = room.find_one("assets")

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
    scene.janus_room_fog_col = s2v(room.attrs.get("fog_col", 500))
    scene.janus_room_locked = bool(room.attrs.get("locked", False))


def load(operator, context, filepath, path_mode="AUTO", relpath=""):
    read_html(context.scene, filepath, path_mode)
