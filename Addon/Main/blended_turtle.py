import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import BoolProperty, IntProperty, EnumProperty, FloatVectorProperty

class OBJECT_OT_add_turtle(Operator, AddObjectHelper):
    """Add an empty turtle world"""
    bl_idname = "mesh.primitive_turtle_add"
    bl_label = "Add Turtle"
    bl_options = {'REGISTER', 'UNDO'}

    pendownp: BoolProperty(
        name="Pen State",
        description="Whether the pen is up or down",
        default="True"
    )

    beginpath_vert_index: IntProperty(
        name="Beginpath vert index",
        description="The index of the selected vert when a beginpath command is issued",
        default=0
    )

    # generic transform props
    align_items = (
        ('WORLD', "World", "Align the new object to the world"),
        ('VIEW', "View", "Align the new object to the view"),
        ('CURSOR', "3D Cursor", "Use the 3D cursor orientation for the new object")
    )
    align: EnumProperty(
        name="Align",
        items=align_items,
        default='WORLD',
        update=AddObjectHelper.align_update_callback,
       )

    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )
    rotation: FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
    )

    def execute(self, context):

        # we will use the scene cursor as our turtle
        turtle = bpy.context.scene.cursor

        #zero the turtle rotation
        turtle.rotation_euler = (0, 0, 0)

        return {'FINISHED'}

    def add_object_button(self, context):
        self.layout.operator(
        OBJECT_OT_add_turtle.bl_idname,
        text="Add Turtle",
        icon='PLUGIN')


    # This allows you to right click on a button and link to documentation
    #TODO: put in link to docs
    def add_object_manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping


    