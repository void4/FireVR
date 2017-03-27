# Fire: JanusVR Exporter & IPFS Publisher

## Description

Fire is a blender addon that exports the current scene to the JanusVR FireBoxHTML-format.
It generates the XML description of the room automatically, exports the objects and provides instant publication over the IPFS network (no server needed!).  It can also export the room to a local destination (no ipfs required).

## Requirements

- [JanusVR](http://www.janusvr.com/)

Optional:
- [IPFS](http://ipfs.io/docs/install/) (only required for IPFS publication)

To use IPFS:
- IPFS must be present in the PATH.
- When not using the IPFS gateway, you need to run the IPFS daemon locally ("ipfs daemon").

This addon was tested under Ubuntu/Linux and Windows. Your feedback is welcome!

## Documentation
https://firevr.readthedocs.io/en/latest/

## Installation

1. Download this repository as .zip file
2. Blender -> User Preferences -> Addons -> Install from File -> Select the .zip, enable the addon

## Usage

1. Create your scene
2. Blender -> 3D View -> Tool Shelf -> Misc -> Set your room and object attributes using the panel options
3. Blender -> 3D View -> Tool Shelf -> Misc -> Set the JanusVR and Export target directories 
4. Click on Start JanusVR to export and launch your room in JanusVR

