import bpy


class TURTLE_OT_clear_screen_alias(bpy.types.Operator):
    bl_idname = "turtle.clear_screen"
    bl_label = "Clear Turtle World"
    bl_description = "Deletes mesh in turtle world and homes turtle."

    def execute(self, context):
        bpy.ops.turtle.cs()

        return {'FINISHED'}
