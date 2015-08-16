import os
import io
import shutil
from contextlib import redirect_stdout

import bpy
from mathutils import Vector

from .html import Tag
from . import ipfs

# boolean to string
def b2s(b):
	return str(b).lower()

# float to string
def f2s(f):
	return "{0:.6f}".format(f)

# vector to string
def v2s(v):
	return " ".join("{0:.6f}".format(c) for c in v)
	
# position to string
def p2s(v):
	v = [v[0],v[2],-v[1]]
	return v2s(v)

# rotation to string
def r2s(m):
	return v2s(list(m*Vector([-1,0,0,0]))[:3])

def write_html(scene, filepath, path_mode):

	stdout = io.StringIO()
	
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
		("near_dist", f2s(scene.janus_room_clipplane[0])),
		("far_dist", f2s(scene.janus_room_clipplane[1])),
		("teleport_min_dist", f2s(scene.janus_room_teleport[0])),
		("teleport_max_dist", f2s(scene.janus_room_teleport[1])),
		("default_sounds", b2s(scene.janus_room_defaultsounds)),
		("cursor_visible", b2s(scene.janus_room_cursorvisible)),
		("fog", b2s(scene.janus_room_fog)),
		("fog_mode", scene.janus_room_fog_mode),
		("fog_density", f2s(scene.janus_room_fog_density)),
		("fog_start", f2s(scene.janus_room_fog_start)),
		("fog_end", f2s(scene.janus_room_fog_end)),
		("fog_col", v2s(scene.janus_room_fog_col)),
		("locked", b2s(scene.janus_room_locked)),
		]
	
	if scene.janus_server_default!=True:
		attr += [
		("server",scene.janus_server),
		("port",scene.janus_server_port),
		]
	
	if scene.camera:
		attr += [
		("pos", p2s(scene.camera.location)),
		("fwd", r2s(scene.camera.matrix_local)),
		]

	if scene.janus_room!="None":
		attr += [
		("use_local_asset",scene.janus_room),
		("visible",b2s(scene.janus_room_visible)),
		("col",v2s(scene.janus_room_color)),
		]
		
	if scene.janus_room_skybox_active:
		attr += [
		("skybox_left_id","sky_left"),
		("skybox_right_id","sky_right"),
		("skybox_front_id","sky_front"),
		("skybox_back_id","sky_back"),
		("skybox_up_id","sky_up"),
		("skybox_down_id","sky_down"),
		]
		
		sky_image = [(scene.janus_room_skybox_left,"sky_left"),(scene.janus_room_skybox_right,"sky_right"),(scene.janus_room_skybox_front,"sky_front"),(scene.janus_room_skybox_back,"sky_back"),(scene.janus_room_skybox_up,"sky_up"),(scene.janus_room_skybox_down,"sky_down")]
		
		for sky in sky_image:
			skyname = os.path.basename(sky[0])
			assetimage = Tag("AssetImage", attr=[("id",sky[1]), ("src",skyname)])
			if not assetimage in assets:
				assets(assetimage)
				shutil.copyfile(src=sky[0], dst=os.path.join(filepath, skyname))	

	if scene.janus_room_script_active:	
		script_list = [scene.janus_room_script1,scene.janus_room_script2,scene.janus_room_script3,scene.janus_room_script4]
		for script_entry in script_list:
			if script_entry != "":
				scriptname = os.path.basename(script_entry)
				assetscript = Tag("AssetScript", attr=[("src",scriptname)])
				if not assetscript in assets:
					assets(assetscript)
					shutil.copyfile(src=script_entry, dst=os.path.join(filepath, scriptname))

	if scene.janus_room_shader_active:		
		if scene.janus_room_shader_frag != "":
			fragname = os.path.basename(scene.janus_room_shader_frag)
		if scene.janus_room_shader_vert != "":
			vertname = os.path.basename(scene.janus_room_shader_vert)
		else:
			vertname = ""
		if fragname:
			attr += [("shader_id", fragname)]
		assetshader = Tag("AssetShader", attr=[("id",fragname),("src",fragname),("vertex_src",vertname)])
		if not assetshader in assets:
			assets(assetshader)
			if fragname:
				shutil.copyfile(src=scene.janus_room_shader_frag, dst=os.path.join(filepath, fragname))
			if vertname:
				shutil.copyfile(src=scene.janus_room_shader_vert, dst=os.path.join(filepath, vertname))						
				
	room = Tag("Room", attr)
	
	useractive = scene.objects.active
	
	exportedmeshes = []
	exportedsurfaces = []

	if  scene.janus_unpack:
		bpy.ops.file.unpack_all(method='USE_LOCAL')
		bpy.ops.file.make_paths_absolute()
	
	for o in bpy.data.objects:
		if o.type=="MESH":
			scene.objects.active = o

			if scene.janus_apply_rot:
				try:
					with redirect_stdout(stdout):
						bpy.ops.object.transform_apply(rotation=True)
				except:
					pass
			if scene.janus_apply_scale:
				try:
					with redirect_stdout(stdout):
						bpy.ops.object.transform_apply(scale=True)
				except:
					pass
			if scene.janus_apply_pos:
				try:
					with redirect_stdout(stdout):
						bpy.ops.object.transform_apply(position=True)
				except:
					pass
			loc = o.location.copy()
			o.location = [0, 0, 0]
			bpy.ops.object.select_pattern(pattern=o.name, extend=False)
			if not o.data.name in exportedmeshes:
				epath = os.path.join(filepath, o.data.name+scene.janus_object_export)
				if scene.janus_object_export==".obj":
					with redirect_stdout(stdout):
						bpy.ops.export_scene.obj(filepath=epath, use_selection=True, use_smooth_groups_bitflags=True, use_uvs=True, use_materials=True, use_mesh_modifiers=True,use_triangles=True, check_existing=False, use_normals=True, path_mode="COPY")
				else:
					with redirect_stdout(stdout):
						bpy.ops.wm.collada_export(filepath=epath, selected=True, check_existing=False)
						# TODO differentiate between per-object and per-mesh properties
				ob = Tag("AssetObject", attr=[("id", o.data.name), ("src",o.data.name+scene.janus_object_export), ("mtl",o.data.name+".mtl")])
				exportedmeshes.append(o.data.name)
				assets(ob)
			rot = [" ".join([str(f) for f in list(v.xyz)]) for v in o.matrix_local.normalized()]
			attr = [("id", o.data.name), ("locked", b2s(o.janus_object_locked)), ("cull_face", o.janus_object_cullface), ("visible", str(o.janus_object_visible).lower()),("col",v2s(o.janus_object_color) if o.janus_object_color_active else "1 1 1"), ("lighting", b2s(o.janus_object_lighting)),("collision_id", o.data.name if o.janus_object_collision else ""), ("pos", p2s(loc)), ("scale", v2s(o.scale)), ("xdir", rot[0]), ("ydir", rot[1]), ("zdir", rot[2])]
			
			if o.janus_object_jsid:
				attr += [("js_id",o.janus_object_jsid)]
			
			if o.janus_object_websurface and o.janus_object_websurface_url:
					if not o.janus_object_websurface_url in exportedsurfaces:
							assets(Tag("AssetWebSurface", attr=[("id", o.janus_object_websurface_url), ("src", o.janus_object_websurface_url), ("width", o.janus_object_websurface_size[0]), ("height", o.janus_object_websurface_size[1])]))
							exportedsurfaces.append(o.janus_object_websurface_url)
					attr += [("websurface_id", o.janus_object_websurface_url)]
			
			if o.janus_object_shader_active:
				if o.janus_object_shader_frag != "":
					fragname = os.path.basename(o.janus_object_shader_frag)
				if o.janus_object_shader_vert != "":
					vertname = os.path.basename(o.janus_object_shader_vert)
				else:
					vertname = ""
				if fragname:
					assetshader = Tag("AssetShader", attr=[("id",fragname),("src",fragname),("vertex_src",vertname)])
					if not assetshader in assets:
							assets(assetshader)
							shutil.copyfile(src=o.janus_object_shader_frag, dst=os.path.join(filepath, fragname))
							if vertname != "":
								shutil.copyfile(src=o.janus_object_shader_vert, dst=os.path.join(filepath, vertname))
					attr += [("shader_id", fragname)]
			
			room(Tag("Object", single=False, attr=attr))
			o.location = loc
		
		elif o.type=="FONT":
		
			if o.data.body.startswith("http://") or o.data.body.startswith("https://"):
				room(Tag("Link", attr=[("pos",v2s(o.location)), ("scale","1.8 3.2 1"), ("url",o.data.body), ("title",o.name), ("col", v2s(o.color[:3]))]))
			else:
				text = Tag("Text", attr=[("pos",v2s(o.location)), ("scale","1.8 3.2 1"), ("title",o.name)])
				text.sub.append(o.data.body)
				room(text)

		elif o.type=="SPEAKER":

			if o.janus_object_sound:
				name = os.path.basename(o.janus_object_sound)
				assetsound = Tag("AssetSound", attr=[("id", name), ("src",name)])
				if not assetsound in assets:
					assets(assetsound)
					shutil.copyfile(src=o.janus_object_sound, dst=os.path.join(filepath, name))
				sound = Tag("Sound", attr=[("id", name), ("js_id", o.janus_object_jsid), ("pos", p2s(o.location)), ("dist", f2s(o.janus_object_sound_dist)), ("rect", v2s(list(o.janus_object_sound_xy1)+list(o.janus_object_sound_xy2))), ("loop", b2s(o.janus_object_sound_loop)), ("play_once", b2s(o.janus_object_sound_once))])
				room(sound)
				
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
