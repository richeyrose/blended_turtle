import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper
from bpy.props import BoolProperty, IntProperty, EnumProperty, FloatVectorProperty
from .. Utils.utils import select, activate

class OBJECT_OT_add_turtle(Operator, AddObjectHelper):
    """Adds an empty turtle world"""
    bl_idname = "mesh.primitive_turtle_add"
    bl_label = "Add Turtle"
    bl_options = {'REGISTER', 'UNDO'}

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
        
        obj = bpy.context.active_object

        object_mode = 'OBJECT' if obj is None else obj.mode
        if object_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        #create new empty turtle world
        world_mesh = bpy.data.meshes.new("world_mesh")
        new_world = bpy.data.objects.new("turtle_world", world_mesh)

        #index of active vert when beginpath is called
        new_world['beginpath_active_vert'] = 0

        #link object to active collection
        bpy.context.layer_collection.collection.objects.link(new_world)

        # we will use the scene cursor as our turtle
        turtle = bpy.context.scene.cursor

        #zero the turtle rotation relative to turtle world
        turtle.rotation_euler = self.rotation

        select(new_world.name)
        activate(new_world.name)
        
        bpy.ops.object.mode_set(mode='EDIT')
                
        #add vert
        bpy.ops.mesh.primitive_vert_add()
        
        #pen state
        new_world['pendownp'] = True
        
        return {'FINISHED'}

    #TODO: find suitable icon or make one
    def add_object_button(self, context):
        """"Adds an add turtle to the add mesh menu"""
        self.layout.operator(
        OBJECT_OT_add_turtle.bl_idname,
        text="Add Turtle",
        icon='PLUGIN')

    
    #TODO: put in link to docs
    def add_object_manual_map():
        """ This allows you to right click on a button and link to documentation"""
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping


    