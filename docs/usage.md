# Usage

Check the JanusVR docs for more details:

[http://www.janusvr.com/guide/markuplanguage/index.html
](http://www.janusvr.com/guide/markuplanguage/index.html)
### Firebox

- **Start JanusVR** All-in-one button, exports room and launches Janus
- **Export FireBox** Only exports the objects and generates the room

### Export Settings

- **Export path** The local directory where the rooms are exported to
- **Use IPFS** Check this to enable IPFS (requires IPFS installed and present in PATH)
  - **IPFS Gateway** Use the IPFS HTTP Gateway (http://gateway.ipfs.io/)
  - **IPNS** Use the IPNS nameserver / set name
- **Apply Rotation** Apply Current Scene Rotation to Objects
- **Apply Scale** Apply Current Scene Scale to Objects
- **Apply Position** Apply Current Scene Position to Objects
- **Unpack Textures** Unpack all textures when exporting

### Run Settings

- **Janus VR path** The path to the JanusVR application
- **Display Mode** Select 2D, Rift, SBS, SBSR mode
- **Rate** Server update rate
- **JanusVR FullScreen** Starts JanusVR in fullscreen mode
- **Window Size** Launch JanusVR with the specified window dimensions

### Objects

__*These attributes are all set on a per object basis__

_**Mesh Objects/Common**_

- **Object Type** For the most part, should be "Object (model)". However, it can be used to allow making placeholder objects with meshes.
- **js\_id** Specify js\_id for object here, blank will give a default numeric id

_**Mesh Objects/Link**_

When making one of these, start off with a newly created Plane.

Don't go into edit mode to resize it - just use the transform
 (the exporter won't pick up on mesh resizing, the plane itself is just a placeholder)

With this, you should be able to semi-accurately place portals.

To check the orientation:
Local Y should be up, Z should be facing outwards.

I'm not quite sure it works completely accurately, and if not what's responsible, but it's a start.

- **Link Name** The name displayed on the portal.
- **Link URL** Since (unlike the old "text as portal" system) link objects don't directly hold text, the URL is put here.
- **Active** If false, ``active="false"`` is set.

_**Mesh Objects/Mesh**_

- **Export Format** Select Wavefront (.obj) or Collada (.dae) export format
- **Collision** Enable collision for this object
- **Locked** Lock this object
- **Visible** Draw this item in the Janus room (setting to false with collision set to true is useful for proxy collision geometry)
- **Set Color** Enable a Janus color value for this object
  - **Color** Select color value for this object
- **Websurface** Texture the current object with a Janus Websurface
  - **URL** Set URL for websurface
  - **Width&Height** Set pixel dimensions for websurface
- **Cull Face** Set desired face culling (back, front, none)
- **GLSL Shader** Set a custom GLSL Shader for this object
  - **Frag Shader** Set path to Fragment Shader (use absolute paths)
  - **Vertex Shader** Set path to Vertex Shader (use absolute paths)

_**Sound Objects (use speaker in Blender)**_

- **Sound** Set path to sound file (use absolute paths)
- **js\_id** js\_id for sound object
- **Distance** Distance at which sound plays at full volume
- **XY1** X and Z positions for first corner of trigger rectangle
- **XY2** X and Z positions for second corner of trigger rectangle
- **Loop** loop sound
- **Place once** play the sound only the first time triggered per user session

_**Text Objects**_

Text objects don't have any properties as such, but there are the following things to note:

1. Text is created for single-line, Paragraph for multi-line.
2. It seems JanusVR ignores the lines anyway, so this is fine.
3. The old "beginning with http creates link" behavior still exists - not exactly sublime.

### Room

- **Room** Sets the room model (see the [FireBox docs](http://www.dgp.toronto.edu/~mccrae/projects/firebox/notes.html) for further details.
- **Visible** If checked, makes the room visible
  - **Color** Sets the rooms color
- **Select Skybox Images** Sets custom skybox images for this room
  - **Skybox Left** Set path to Left Skybox Image (use absolute paths)
  - **Skybox Right** Set path to Right Skybox Image (use absolute paths)
  - **Skybox Front** Set path to Front Skybox Image (use absolute paths)
  - **Skybox Back** Set path to Back Skybox Image (use absolute paths)
  - **Skybox Up** Set path to Up Skybox Image (use absolute paths)
  - **Skybox Down** Set path to Down Skybox Image (use absolute paths)
- **Gravity** Sets the rooms gravity
- **Walk Speed** Sets the players walk speed
- **Run Speed** Sets the players run speed
- **Jump Velocity** Sets the players jump velocity
- **Clip Plane** Sets the near and far clip distances
- **Teleport Range** Sets the min and max teleport distances
- **Default Sounds** Use default sounds in room
- **Show Cursor** Show Cursor in room
- **Fog** Enable Fog effects
  - **Color** Set fog color
  - **Fog Mode** Set fog mode (exp, exp2, linear)
    - **Density** Set fog density (exp and exp2 modes)
    - **Start & End** Set fog start and end dist (linear mode)
- **Asset Scripts** Enable JS scripts for room
  - **Script 1-4** Set path to Asset Scripts (use absolute paths, up to 4 scripts supported)
- **Global GLSL Shader** Set a global GLSL shader for the room
  - **Frag Shader** Set path to Fragment Shader (use absolute paths)
  - **Vertex Shader** Set path to Vertex Shader (use absolute paths)
- **Lock Room** Lock room from edits

### Multiplayer Server
- **Default Server** Use the default server specified in Janus
- **Server** URL to the server
- **Port** Port of the server

### Debug
- **JanusVR** enable debug mode
