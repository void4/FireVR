#Fire, a JanusVR Exporter
### by void

##Description

Fire is a blender addon that exports the current scene to the JanusVR FireBoxHTML-format.
It generates the XML description of the room automatically and provides instant publication over the IPFS network (no server needed!).

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

##Settings

*IPFS Gateway* Use the IPFS HTTP Gateway (http://gateway.ipfs.io/)
*JanusVR Window Mode* Starts JanusVR in window mode
*Room* Sets the room model (see the [FireBox docs](http://www.dgp.toronto.edu/~mccrae/projects/firebox/notes.html) for further details.
*Room visible* If checked, makes the room visible

##FAQ

###The objects are loading slowly
Consider running IPFS locally.

###The objects are not rotated correctly
CTRL+A -> Apply Rotation
