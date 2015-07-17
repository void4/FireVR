#Fire: JanusVR Exporter & IPFS Publisher
#### by void

##Description

Fire is a blender addon that exports the current scene to the JanusVR FireBoxHTML-format.
It generates the XML description of the room automatically, exports the objects and provides instant publication over the IPFS network (no server needed!).

##Requirements

- [JanusVR](http://www.janusvr.com/)
- [IPFS](http://ipfs.io/docs/install/)

IPFS has to be present in the PATH.

When not using the IPFS gateway, you need to run the IPFS daemon locally ("ipfs daemon").

This addon was tested under Ubuntu/Linux. Your feedback is welcome!

##Installation

1. Download this repository as .zip file
2. Blender -> User Preferences -> Addons -> Install from File -> Select the .zip, enable the addon
3. Blender -> 3D View -> Tool Shelf -> Misc -> Set the JanusVR and Export target directories

##Usage

1. Create your scene
2. Click on Start JanusVR

##Configuration

###Firebox

**Start JanusVR** All-in-one button

**Hash** The address of the room is displayed here

**Export FireBox** Only exports the objects and generates the room

###Settings

**Export path** The place where the rooms are exported to

**Janus VR path** The path to the JanusVR application

**IPFS Gateway** Use the IPFS HTTP Gateway (http://gateway.ipfs.io/)

**JanusVR Window Mode** Starts JanusVR in window mode

###Room

**Room** Sets the room model (see the [FireBox docs](http://www.dgp.toronto.edu/~mccrae/projects/firebox/notes.html) for further details.

**Visible** If checked, makes the room visible

**Color** Sets the rooms color

**Gravity** Sets the rooms gravity

**Walk Speed** Sets the players walk speed

**Run Speed** Sets the players run speed

###Multiplayer Server

**Server** URL to the server

**Port** Port of the server

##FAQ

###The objects are loading slowly
Consider running IPFS locally.

###The objects are rotated incorrectly
CTRL+A -> Apply Rotation
