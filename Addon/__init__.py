# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "BlendedTurtle",
    "author" : "Richard Rose",
    "description" : "Turtle graphics in blender",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3d > Add > Mesh > New Object",
    "warning" : "",
    "category" : "Add Mesh"
}
import os
import bpy
from . Operators.blended_turtle import OBJECT_OT_add_turtle
from . Commands import*

classes = (OBJECT_OT_add_turtle, pen_down, pen_up)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_manual_map(OBJECT_OT_add_turtle.add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(OBJECT_OT_add_turtle.add_object_button)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(OBJECT_OT_add_turtle.add_object_button)
    bpy.utils.unregister_manual_map(OBJECT_OT_add_turtle.add_object_manual_map)
