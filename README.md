### Fire: JanusVR Importer and Exporter for Blender 3D

Fire is a Blender addon that exports the current scene to the JanusVR FireBoxHTML-format. It generates the XML description of the room automatically, exports the objects and materials and launches into JanusVR with just one click. It can also import scenes directly from your PC or websites, just give it a URL.

It optionally also supports instant publication over the IPFS network (no server needed!).

#### Requirements

- [JanusVR](http://www.janusvr.com/)

Optional:
- [IPFS](http://ipfs.io/docs/install/) (only required for IPFS publication)
<sup>
To use IPFS, it must be present in the PATH. When not using the IPFS gateway, you need to run the IPFS daemon locally ("ipfs daemon").
</sup>

#### Documentation
https://firevr.readthedocs.io/en/latest/

#### Installation

1. Download this repository as .zip file: https://github.com/void4/FireVR/archive/master.zip
2. Blender -> User Preferences -> Addons -> Install from File -> Select the .zip, enable the addon

More detailed installation instructions can be found here: https://firevr.readthedocs.io/en/latest/installation.html

#### Usage

1. Create your scene
2. Blender -> 3D View -> Tool Shelf -> Misc -> Set your room and object attributes using the panel options
3. Blender -> 3D View -> Tool Shelf -> Misc -> Set the JanusVR and Export target directories 
4. Click on Start JanusVR to export and launch your room in JanusVR

This addon was tested under Ubuntu/Linux and Windows. Your feedback is welcome!
