import os

import bpy

from .html import Tag
from . import ipfs

def v2s(v):
	return " ".join("{0:.4f}".format(c).replace("-0","0") for c in v)
	
def p2s(v):
	v = [v[0],v[2],-v[1]]
	return v2s(v)

def write_html(scene, filepath, path_mode):

	world = scene.world

	doc = Tag("!DOCTYPE html", single=True)

	html = Tag("html")
	doc(html)

	head = Tag("head")
	head(Tag("meta", charset="utf-8", single=True))
	html(head)

	body = Tag("body")
	html(body)
	
	fire = Tag("FireBoxRoom")
	assets = Tag("Assets")
	
	if scene.useroom!="None":
		room = Tag("Room", use_local_asset=scene.useroom, visible=str(scene.useroomvisible).lower(), fwd="0 0 1")
	else:
		room = Tag("Room", fwd="0 0 1")
	
	useractive = scene.objects.active
	
	for o in bpy.data.objects:
		if o.type=="MESH":
			scene.objects.active = o
			bpy.ops.object.transform_apply(rotation=True)
			loc = o.location.copy()
			o.location = [0, 0, 0]
			bpy.ops.object.select_pattern(pattern=o.name, extend=False)
			bpy.ops.export_scene.obj(filepath=os.path.join(filepath, o.name+".obj"), use_selection=True, use_triangles=True, check_existing=False, use_normals=True)
			ob = Tag("AssetObject", id=o.name, src=o.name+".obj", mtl=o.name+".mtl")
			assets(ob)
			rot = [" ".join([str(f) for f in list(v.xyz)]) for v in o.matrix_local.normalized()]
			room(Tag("Object", single=False, id=o.name, collision_id=o.name, pos=p2s(loc), scale=v2s(o.scale), xdir=rot[0], ydir=rot[1], zdir=rot[2]))
			o.location = loc
		elif o.type=="FONT":
			if o.data.body.startswith("http://") or o.data.body.startswith("https://"):
				room(Tag("Link", pos=v2s(o.location), scale="1.8 3.2 1", url=o.data.body, title=o.name))
	
	scene.objects.active = useractive
	
	fire(assets)
	fire(room)
	body(fire)

	file = open(os.path.join(filepath,"index.html"), mode="w", encoding="utf8", newline="\n")
	fw = file.write
	doc.write(fw, indent="")
	file.close()

def save(operator, context, filepath="", path_mode="AUTO", relpath=""):
	write_html(context.scene, filepath, path_mode)
