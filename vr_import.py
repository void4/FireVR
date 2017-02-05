# Import JanusVR from URL/filesystem+
# TODO include dependencies directly in addon
from bs4 import BeautifulSoup
import urllib

def read_html(scene, filepath, path_mode):
    source = urllib.urlopen(filepath)
    html = source.read()

    soup = BeautifulSoup(html)

    # Case sensitive!
    room = soup.find_one("fireboxroom")
    assets = room.find_one("assets")

    # Prevent having to specify defaults twice? (on external load and addon startup)
    scene.janus_room_gravity = float(assets.attrs.get("gravity", 9.8))
    scene.janus_walk_speed = float(assets.attrs.get("walk_speed", 1.8))
    scene.janus_run_speed = float(assets.attrs.get("run_speed", 5.4))
    scene.janus_jump_velocity = float(assets.attrs.get("jump_velocity", 5))
    near_dist = float(assets.attrs.get("near_dist", 0.0025))
    far_dist = float(assets.attrs.get("far_dist", 500))
    teleport_min_dist = float(assets.attrs.get("teleport_min_dist", 5))
    teleport_max_dist = float(assets.attrs.get("teleport_min_dist", 100))

    def load(operator, context, filepath, path_mode="AUTO", relpath=""):
        read_html(context.scene, filepath, path_mode)
