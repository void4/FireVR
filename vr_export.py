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
		("gravity", f2s(scene.janus_room_gravity)),
		("walk_speed", f2s(scene.janus_room_walkspeed)),
		("run_speed", f2s(scene.janus_room_runspeed)),
		("jump_velocity", f2s(scene.janus_room_jump)),
		("near_dist", f2s(scene.janus_room_neardist)),
		("far_dist", f2s(scene.janus_room_fardist)),
		("teleport_min_dist", f2s(scene.janus_room_telemindist)),
		("teleport_max_dist", f2s(scene.janus_room_telemaxdist)),
		("fog",str(scene.janus_room_fog).lower()),
		("fog_col",v2s(scene.janus_room_fogcolor)),
		("fog_mode",scene.janus_room_fogmode),
		("fog_density", f2s(scene.janus_room_fogdensity)),
		("fog_start", f2s(scene.janus_room_fogstart)),
		("fog_end", f2s(scene.janus_room_fogend)),
		("default_sounds",str(scene.janus_room_defaultsounds).lower()),
		("cursor_visible",str(scene.janus_room_showcursor).lower()),
		("server",scene.janus_server),
		("port",scene.janus_server_port),
		]
	
	if scene.janus_room!="None":
		attr += [
		("use_local_asset",scene.janus_room),
		("visible",str(scene.janus_room_visible).lower()),
		("col",v2s(scene.janus_room_color)),
		]
		
	room = Tag("Room", attr)
	
	useractive = scene.objects.active
	
	exportedmeshes = []
	
	bpy.ops.file.unpack_all(method='USE_LOCAL')
	bpy.ops.file.make_paths_absolute()
	
	for o in bpy.data.objects:
		if o.type=="MESH":
			scene.objects.active = o
			try:
				bpy.ops.object.transform_apply(rotation=True)
			except:
				pass
			try:
				bpy.ops.object.transform_apply(scale=True)
			except:	
				pass
			loc = o.location.copy()
			o.location = [0, 0, 0]
			bpy.ops.object.select_pattern(pattern=o.name, extend=False)
			if not o.data.name in exportedmeshes:
				epath = os.path.join(filepath, o.data.name+scene.janus_object_export)
				if scene.janus_object_export==".obj":
					bpy.ops.export_scene.obj(filepath=epath, use_selection=True, use_smooth_groups_bitflags=False, use_uvs=True, use_materials=True, use_mesh_modifiers=True, use_triangles=True, check_existing=False, axis_forward='-Z', axis_up='Y', use_normals=True, path_mode="COPY")
				else:
					bpy.ops.wm.collada_export(filepath=epath, selected=True, check_existing=False)
				ob = Tag("AssetObject", attr=[("id", o.data.name), ("src",o.data.name+scene.janus_object_export), ("mtl",o.data.name+".mtl")])
				exportedmeshes.append(o.data.name)
				assets(ob)
			rot = [" ".join([str(f) for f in list(v.xyz)]) for v in o.matrix_local.normalized()]
			room(Tag("Object", single=False, attr=[
			("id", o.data.name), 
			("js_id", o.data.name), 
			("locked", str(o.janus_object_locked).lower()), 
			("lighting", str(o.janus_object_lighting).lower()),
			("visible", str(o.janus_object_visible).lower()),
			("col",v2s(o.janus_object_color)),
			("collision_id", o.data.name if o.janus_object_collision else ""), 
			("pos", p2s(loc)), 
			("scale", v2s(o.scale)), 
			("xdir", rot[0]), 
			("ydir", rot[1]), 
			("zdir", rot[2]),
			("websurface_id", str(o.janus_object_websurfaceid) if o.janus_object_websurfaceid != ("" or "http://") else ""),
			]))
			if o.janus_object_websurfaceid != ("" or "http://"):
				websurf = Tag("AssetWebsurface", attr=[("id", o.janus_object_websurfaceid), ("src", o.janus_object_websurfaceid)])
				assets(websurf)
			o.location = loc
		elif o.type=="FONT":
			if o.data.body.startswith("http://") or o.data.body.startswith("https://"):
				room(Tag("Link", attr=[("pos",v2s(o.location)), ("scale","1.8 3.2 1"), ("url",o.data.body), ("title",o.name), ("col", v2s(o.color[:3]))]))
			else:
				text = Tag("Text", attr=[("pos",v2s(o.location)), ("scale","3 3 3"), ("title",o.name)])
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
