import os

import bpy

from .html import Tag
from . import ipfs

def f2s(f):
	return "{0:.6f}".format(f).replace("-0","0")

def v2s(v):
	return " ".join("{0:.6f}".format(c).replace("-0","0") for c in v)
	
def p2s(v):
	v = [v[0],v[2],-v[1]]
	return v2s(v)

def write_html(scene, filepath, path_mode):

	world = scene.world

	doc = Tag("!DOCTYPE html", single=True)

	html = Tag("html")
	doc(html)

	head = Tag("head")
	head(Tag("meta", attr=[("charset","utf-8")], single=True))
	html(head)

	body = Tag("body")
	html(body)
	
	fire = Tag("FireBoxRoom")
	assets = Tag("Assets")
	
	attr=[
		("fwd","0 0 1"),
		("gravity", f2s(scene.useroomgravity)),
		("walk_speed", f2s(scene.useroomwalkspeed)),
		("run_speed", f2s(scene.useroomrunspeed)),
		]
	
	if scene.useroom!="None":
		attr += [
		("use_local_asset",scene.useroom),
		("visible",str(scene.useroomvisible).lower()),
		("col",v2s(scene.useroomcolor)),
		("server",scene.useserver),
		("port",scene.useserverport),
		]
		
	room = Tag("Room", attr)
	
	useractive = scene.objects.active
	
	exportedmeshes = []
	
	for o in bpy.data.objects:
		if o.type=="MESH":
			scene.objects.active = o
			try:
				bpy.ops.object.transform_apply(rotation=True)
			except:
				pass
			loc = o.location.copy()
			o.location = [0, 0, 0]
			bpy.ops.object.select_pattern(pattern=o.name, extend=False)
			if not o.data.name in exportedmeshes:
				epath = os.path.join(filepath, o.data.name+scene.useobjectexport)
				if scene.useobjectexport==".obj":
					bpy.ops.export_scene.obj(filepath=epath, use_selection=True, use_triangles=True, check_existing=False, use_normals=True)
				else:
					bpy.ops.wm.collada_export(filepath=epath, selected=True, check_existing=False)
				ob = Tag("AssetObject", attr=[("id", o.data.name), ("src",o.data.name+scene.useobjectexport), ("mtl",o.data.name+".mtl")])
				exportedmeshes.append(o.data.name)
				assets(ob)
			rot = [" ".join([str(f) for f in list(v.xyz)]) for v in o.matrix_local.normalized()]
			room(Tag("Object", single=False, attr=[("id", o.data.name), ("collision_id", o.data.name), ("pos", p2s(loc)), ("scale", v2s(o.scale)), ("xdir", rot[0]), ("ydir", rot[1]), ("zdir", rot[2])]))
			o.location = loc
		elif o.type=="FONT":
			if o.data.body.startswith("http://") or o.data.body.startswith("https://"):
				room(Tag("Link", attr=[("pos",v2s(o.location)), ("scale","1.8 3.2 1"), ("url",o.data.body), ("title",o.name)]))
			else:
				text = Tag("Text", attr=[("pos",v2s(o.location)), ("scale","1.8 3.2 1"), ("title",o.name)])
				text.sub.append(o.data.body)
				room(text)
				
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
