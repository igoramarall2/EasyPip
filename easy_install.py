bl_info = {
"name": "Install Python Modules",
"author": "Igor Silva do Amaral",
"version": (0, 1),
"blender": (2, 80, 0),
"location": "TEXT_EDITOR > Side",
"description": "A add-on that simplifies the installation of python modules",
}

import os
import subprocess
import sys

import bpy
from bpy.types import Operator, Panel


def CaixaMensagemPM(message="", title="Message Box", icon="INFO"):
"""
Creates a message box with a specified message, title, and icon.

Parameters:
message (str): The message to display in the message box. Default is an empty string.
title (str): The title of the message box. Default is "Message Box".
icon (str): The icon to display in the message box. Default is "INFO".

Returns:
None
"""

def draw(self, context):
self.layout.label(text=message)

bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class Pip:
"""
The `Pip` class provides methods for managing Python modules using pip within Blender.

Attributes:
python (str): The path to the Python executable used for pip operations.
module_name (str): The name of the Python module to be installed, updated, or uninstalled.

Methods:
Upgrade_PIP(self):
Upgrades the pip tool and ensures pip is installed.

Install_Modules(self):
Installs a specified Python module using pip. Requires setting `self.module_name` first.

Update_Modules(self):
Updates a specified Python module using pip. Requires setting `self.module_name` first.

Uninstall_Modules(self):
Uninstalls a
specified Python module using pip. Requires setting `self.module_name` first.
"""

def __init__(self):
"""
Initializes the Pip instance. It sets the path to the Python executable and the module name.
"""
module_name = bpy.context.scene.modules
python_exe = os.path.join(sys.prefix, "bin", "python.exe")
self.python = python_exe
self.module_name = module_name

def Upgrade_PIP(self):
"""
Upgrades the pip tool and ensures pip is installed.

Returns:
dict: A dictionary with the key "FINISHED" to indicate the operation is completed.
"""
subprocess.call([self.python, "-m", "ensurepip"])
subprocess.call([self.python, "-m", "pip", "install", "--upgrade", "pip"])
CaixaMensagemPM("Pip updated", "DONE", "DOCUMENTS")
return {"FINISHED"}

def Install_Modules(self):
"""
Installs a specified Python module using pip. Requires setting `self.module_name` first.

Returns:
dict: A dictionary with the key "FINISHED" to indicate the operation is completed.
"""
subprocess.call([self.python, "-m", "pip", "install", self.module_name])
CaixaMensagemPM("Module installed. Please restart Blender", "DONE", "DOCUMENTS")
return {"FINISHED"}

def Update_Modules(self):
"""
Updates a specified Python module using pip. Requires setting `self.module_name` first.

Returns:
dict: A dictionary with the key "FINISHED" to indicate the operation is completed.
"""
subprocess.call(
[self.python, "-m", "pip", "install", "--upgrade", self.module_name]
)
CaixaMensagemPM("Module updated. Please restart Blender", "DONE", "DOCUMENTS")
return {"FINISHED"}

def Uninstall_Modules(self):
"""
Uninstalls a specified Python module using pip. Requires setting `self.module_name` first.

Returns:
dict: A dictionary with the key "FINISHED" to indicate the operation is completed.
"""
subprocess.call([self.python, "-m", "pip", "uninstall", self.module_name])
CaixaMensagemPM(
"Module uninstalled. Please restart Blender",
"DONE",
"DOCUMENTS",
)
return {"FINISHED"}


class PIP_OT_tools(Operator):
bl_idname = "pip.toolset"
bl_label = "Ferramentas de Desenvolvedor"
pip: bpy.props.EnumProperty(
items=[
("upgrade_pip", "upgrade_pip", "upgrade_pip"),
("install_modules", "install_modules", "install_modules"),
("upgrade_modules", "upgrade_modules", "upgrade_modules"),
("uninstall_modules", "uninstall_modules", "uninstall_modules"),
]
)

def execute(self, context):
if self.pip == "upgrade_pip":
Pip().Update_Modules()

if self.pip == "install_modules":
Pip().Install_Modules()

if self.pip == "upgrade_modules":
Pip().Update_Modules()

if self.pip == "uninstall_modules":
Pip().Update_Modules()
return {"FINISHED"}


class PIP_PT_tools(Panel):
"""Panel for module installation and PIP updates."""

bl_label = "DEV: Install Modules"
bl_space_type = "TEXT_EDITOR"
bl_region_type = "UI"
bl_category = "Install Modules"

def draw(self, context):
layout = self.layout
box = layout.box()
col = box.column()
row = col.row(align=True)
col.scale_y = 4
col.separator(factor=1)
row.prop(bpy.context.scene, "modules", text="", icon="FILE_SCRIPT")
col.scale_y = 3
row = col.row(align=True)
row.operator(
"pip.toolset", text="Install Module", icon="MODIFIER_ON"
).pip = "install_modules"
row = col.row(align=True)
row.alert = True
row.operator(
"pip.toolset", text="Uninstall Module", icon="TRASH"
).pip = "uninstall_modules"
row = col.row(align=True)
row.operator(
"pip.toolset", text="Update PIP", icon="INDIRECT_ONLY_ON"
).pip = "upgrade_pip"

row.operator(
"pip.toolset", text="Update Module", icon="INDIRECT_ONLY_ON"
).pip = "upgrade_modules"


classes = (PIP_OT_tools, PIP_PT_tools)


def register():
from bpy.utils import register_class

for cls in classes:
register_class(cls)

bpy.types.Scene.modules = bpy.props.StringProperty(name="modulos", default="Modulo")


def unregister():
from bpy.utils import unregister_class

for cls in reversed(classes):
unregister_class(cls)


if __name__ == "__main__":
register()
