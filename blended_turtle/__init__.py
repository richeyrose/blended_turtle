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

import os
import bpy
from . Operators.blended_turtle import OBJECT_OT_add_turtle
from . Operators.commands import *

bl_info = {
    "name": "BlendedTurtle",
    "author": "Richard Rose",
    "description": "Turtle graphics in blender",
    "blender": (2, 80, 0),
    "version": (0, 0, 2),
    "location": "View3d > Add > Mesh > New Object",
    "warning": "",
    "category": "Add Mesh"
}

classes = (
    OBJECT_OT_add_turtle,
    TURTLE_OT_clear_screen,
    TURTLE_OT_clean,
    TURTLE_OT_home,
    TURTLE_OT_pen_down,
    TURTLE_OT_pen_up,
    TURTLE_OT_forward,
    TURTLE_OT_backward,
    TURTLE_OT_up,
    TURTLE_OT_down,
    TURTLE_OT_left,
    TURTLE_OT_right,
    TURTLE_OT_left_turn,
    TURTLE_OT_right_turn,
    TURTLE_OT_look_up,
    TURTLE_OT_look_down,
    TURTLE_OT_roll_left,
    TURTLE_OT_roll_right,
    TURTLE_OT_set_pos,
    TURTLE_OT_set_rotation,
    TURTLE_OT_set_heading,
    TURTLE_OT_set_pitch,
    TURTLE_OT_set_roll,
    TURTLE_OT_quadratic_curve,
    TURTLE_OT_cubic_curve,
    TURTLE_OT_begin_path,
    TURTLE_OT_stroke_path,
    TURTLE_OT_fill_path,
    TURTLE_OT_select_all,
    TURTLE_OT_extrude,
    TURTLE_OT_select_path)


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
