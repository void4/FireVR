bl_info = {
	"name" : "FireVR",
	"author" : "void",
	"version" : (0, 1),
	"blender" : (2, 75, 0),
	"location" : "View3D > Add > Mesh",
	"description": "Converts the scene into FireBox HTML and publishes it to IPFS",
	"wiki_url" : "",
	"category" : "Import-Export"
}

import importlib

if "bpy" in locals():
	if "ipfsvr_export" in locals():
		importlib.reload(ipfsvr_export)

import os
import time
import subprocess

from bpy.types import (
	Operator,
	Panel,
	AddonPreferences
	)

from bpy.props import (
	StringProperty,
	BoolProperty,
	EnumProperty,
	FloatProperty,
	FloatVectorProperty,
	IntProperty
	)

from bpy_extras.io_utils import (
	ExportHelper
	)

import bpy

import bpy.utils.previews

from . import vr_export

bpy.types.Scene.roomhash = StringProperty(name="", default="")

class ToolPanel(Panel):
	bl_label = "Firebox"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	
	def draw(self, context):
		self.layout.operator("fire.html", icon_value=custom_icons["custom_icon"].icon_id)
		if context.scene.roomhash:
			self.layout.prop(context.scene, "roomhash")
		self.layout.operator("export_scene.html")

bpy.types.Scene.usegateway = BoolProperty(name="IPFS Gateway", default=True)
bpy.types.Scene.usefullscreen = BoolProperty(name="JanusVR Fullscreen", default=True)

bpy.types.Scene.useipns = BoolProperty(name="IPNS", default=False)
bpy.types.Scene.useipnsname = StringProperty(name="", default="myroom")

class SettingsPanel(Panel):
	bl_label = "Settings"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	
	def draw(self, context):
		self.layout.operator("export_path.html")
		self.layout.operator("set_path.janus")
		self.layout.prop(context.scene, "usegateway")
		self.layout.prop(context.scene, "usefullscreen")
		self.layout.prop(context.scene, "useipns")
		if context.scene.useipns:
			self.layout.prop(context.scene, "useipnsname")


rooms = ["room_plane", "None", "room1", "room2", "room3", "room4", "room5", "room6", "room_1pedestal", "room_2pedestal", "room_3_narrow", "room_3_wide", "room_4_narrow", "room_4_wide", "room_box_small", "room_box_medium", "room1_new"]
roomlist = tuple(tuple([room, room, room]) for room in rooms)
bpy.types.Scene.useroom = EnumProperty(name="", default="room_plane", items=roomlist)
bpy.types.Scene.useroomvisible = BoolProperty(name="Visible", default=True)
bpy.types.Scene.useroomcolor = FloatVectorProperty(name="Color", default=(1.0,1.0,1.0), subtype="COLOR", size=3, min=0.0, max=1.0)

bpy.types.Scene.useroomgravity = FloatProperty(name="Gravity", default=9.8, min=-100, max=100)
bpy.types.Scene.useroomwalkspeed = FloatProperty(name="Walk Speed", default=1.8, min=-100, max=100)
bpy.types.Scene.useroomrunspeed = FloatProperty(name="Run Speed", default=5.4, min=-100, max=100)

class RoomPanel(Panel):
	bl_label = "Room"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	
	def draw(self, context):
		self.layout.prop(context.scene, "useroom")
		
		if context.scene.useroom!="None":
			self.layout.prop(context.scene, "useroomvisible")
			self.layout.prop(context.scene, "useroomcolor")
			
		self.layout.prop(context.scene, "useroomgravity")
		self.layout.prop(context.scene, "useroomwalkspeed")
		self.layout.prop(context.scene, "useroomrunspeed")

bpy.types.Scene.useserver = StringProperty(name="", default="babylon.vrsites.com")
bpy.types.Scene.useserverport = IntProperty(name="Port", default=5567, min=0, max=2**16-1)

class ServerPanel(Panel):
	bl_label = "Multiplayer Server"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	
	def draw(self, context):
		self.layout.prop(context.scene, "useserver")
		self.layout.prop(context.scene, "useserverport")

class ipfsvr(AddonPreferences):
	bl_idname = __package__
		
	from os.path import expanduser
	home = expanduser("~")
	filename_ext = ""
	
	exportpath = StringProperty(name="", subtype="FILE_PATH", default="")
	januspath = StringProperty(name="januspath", subtype="FILE_PATH", default=os.path.join(home,"JanusVRBin/janusvr"))

	def draw(self, context):
		layout = self.layout
		layout.label("VR Preferences")
		#layout.prop(self, exportpath)

def setv(context, name, value):
	context.user_preferences.addons[__name__].preferences[name] = value

def getv(context, name):
	return context.user_preferences.addons[__name__].preferences[name]

def hasv(context, name):
	try:
		return getv(context, name)
	except KeyError:
		pass

class VRExportPath(Operator, ExportHelper):
	bl_idname = "export_path.html"
	bl_label = "Export path"
	bl_options = {"PRESET", "UNDO"}
	
	use_filter_folder = True
	filename_ext = ""
	filter_glob = ""
	
	def execute(self, context):
		keywords = self.as_keywords(ignore=("filter_glob","check_existing"))

		if bpy.data.is_saved and context.user_preferences.filepaths.use_relative_paths:
			keywords["relpath"] = os.path.dirname((bpy.data.path_resolve("filepath", False).as_bytes()))

		if os.path.isdir(os.path.dirname(keywords["filepath"])):
			setv(context,"exportpath",os.path.dirname(keywords["filepath"]))
		else:
			self.report({"ERROR"}, "Please select a directory, not a file")
			
		return {"FINISHED"}

class VRJanusPath(Operator, ExportHelper):
	bl_idname = "set_path.janus"
	bl_label = "JanusVR path"
	bl_options = {"PRESET", "UNDO"}

	use_filter = False
	filename_ext = ""
	filter_glob = ""
	
	def execute(self, context):
		keywords = self.as_keywords(ignore=("filter_glob","check_existing"))

		if bpy.data.is_saved and context.user_preferences.filepaths.use_relative_paths:
			keywords["relpath"] = bpy.data.path_resolve("filepath", False).as_bytes()

		if os.path.isfile(keywords["filepath"]):
			setv(context,"januspath", keywords["filepath"])
		else:
			self.report({"ERROR"}, "Please select the JanusVR executable")
			
		return {"FINISHED"}

class VRExport(Operator):
	bl_idname = "export_scene.html"
	bl_label = "Export FireBoxHTML"
	bl_options = {"PRESET", "UNDO"}
	
	def execute(self, context):
		exportpath = getv(context, "exportpath")
		if exportpath:
			filepath = os.path.join(exportpath, time.strftime("%Y%m%d%H%M%S"))
			os.makedirs(filepath, exist_ok=True)
			vr_export.save(self, context, filepath=filepath)
			setv(context, "filepath", filepath)
			self.report({"INFO"}, "Exported files to %s" % filepath)
		else:
			self.report({"ERROR"}, "Invalid export path")
		return {"FINISHED"}

def getURL(context, hashes):
	if context.scene.usegateway:
		return "http://gateway.ipfs.io/ipfs/"+hashes[-1]+"/index.html"
	else:
		return "localhost:8080/ipfs/"+hashes[-1]+"/index.html"

class VRJanus(Operator):
	bl_idname = "export_scene.vrjanus"
	bl_label = "Start JanusVR"
	bl_options = {"PRESET", "UNDO"}
	
	def execute(self, context):
	
		filepath = hasv(context, "filepath")

		if not filepath:
			self.report({"ERROR"}, "Did not export scene.")
			return {"FINISHED"}			
	
		ipfs.start()
		
		hashes = ipfs.addRecursive(filepath)
	
		if not hashes:
			self.report({"ERROR"}, "IPFS Error")
			return {"FINISHED"}
			
		gateway = getURL(context, hashes)
		
		context.scene.roomhash = gateway
			
		self.report({"INFO"}, "Starting JanusVR on %s" % gateway)
		
		args = []
		if not context.scene.usefullscreen:
			args.append("-window")
			
		januspath = hasv(context, "januspath")
		if januspath:
			subprocess.Popen([januspath, gateway]+args, close_fds=True)
		else:
			self.report({"ERROR"}, "JanusVR path not set")
		return {"FINISHED"}
		
class VRFire(Operator):
	bl_idname = "fire.html"
	bl_label = "Start JanusVR"
	bl_options = {"PRESET", "UNDO"}
	
	def execute(self, context):
		bpy.ops.export_scene.html()
		bpy.ops.export_scene.vrjanus()
		return {"FINISHED"}

custom_icons = None

def register():
	global custom_icons
	custom_icons = bpy.utils.previews.new()
	script_path = os.path.realpath(__file__)
	icon_path = os.path.join(os.path.dirname(script_path), "icon.png")
	custom_icons.load("custom_icon", icon_path, "IMAGE")
	bpy.utils.register_module(__name__)
	
def unregister():
	global custom_icons
	bpy.utils.previews.remove(custom_icons)
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()
