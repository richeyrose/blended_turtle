from math import degrees, radians
import bpy
from bpy.props import StringProperty, FloatProperty, FloatVectorProperty, IntProperty
import bmesh
from mathutils import Vector
from .. Utils.utils import select_by_loc


class TURTLE_OT_clear_screen(bpy.types.Operator):
    bl_idname = "turtle.cs"
    bl_label = "Clear Turtle World"
    bl_description = "Deletes mesh in turtle world and homes turtle."

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        bpy.ops.turtle.home()
        bpy.ops.turtle.clean()

        return {'FINISHED'}


class TURTLE_OT_home(bpy.types.Operator):
    bl_idname = "turtle.home"
    bl_label = "Home Turtle"
    bl_description = "Set turtle location and rotation to object origin"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        context.scene.cursor.location = context.object.location
        context.scene.cursor.rotation_euler = context.object.rotation_euler

        return {'FINISHED'}


class TURTLE_OT_clean(bpy.types.Operator):
    bl_idname = "turtle.clean"
    bl_label = "Clean"
    bl_description = "deletes mesh, leaves turtle where it is"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete()
        context.object['beginpath_active_vert'] = 0

        return {'FINISHED'}


class TURTLE_OT_pen_down(bpy.types.Operator):
    bl_idname = "turtle.pd"
    bl_label = "Pend Down"
    bl_description = "Lowers the pen so that the turtle will draw on move"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.mesh.primitive_vert_add()
        bpy.context.object['pendownp'] = True

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TURTLE_OT_pen_up(bpy.types.Operator):
    bl_idname = "turtle.pu"
    bl_label = "Pen Up"
    bl_description = "Raises the pen so that the turtle will NOT draw on move"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.context.object['pendownp'] = False
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TURTLE_OT_forward(bpy.types.Operator):
    bl_idname = "turtle.fd"
    bl_label = "Move Forward"
    bl_description = "Moves the turtle forward. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        # make sure selection is properly updated
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        """ check our object has a "pendownp" property that
         describes the pen state and if not add one"""
        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        # check if pen is down
        if context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            # ensure that we only select the vert that the cursor is on
            turtle_location = bpy.context.scene.cursor.location
            select_by_loc(lbound=turtle_location, ubound=turtle_location)

            # extrude vert along cursor Y
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (0, self.d, 0),
                    "orient_type": 'CURSOR'})

        # move turtle forward
        bpy.ops.transform.translate(
            value=(0, self.d, 0),
            orient_type='CURSOR',
            cursor_transform=True)

        return {'FINISHED'}


class TURTLE_OT_backward(bpy.types.Operator):
    bl_idname = "turtle.bk"
    bl_label = "Move Backward"
    bl_description = "Moves the turtle Backward. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (0, -self.d, 0),
                    "orient_type": 'CURSOR'})

        bpy.ops.transform.translate(
            value=(0, -self.d, 0),
            orient_type='CURSOR',
            cursor_transform=True)

        return {'FINISHED'}


class TURTLE_OT_up(bpy.types.Operator):
    bl_idname = "turtle.up"
    bl_label = "Move Up"
    bl_description = "Moves the turtle Up. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (0, 0, self.d),
                    "orient_type": 'CURSOR'})

        bpy.ops.transform.translate(
            value=(0, 0, self.d),
            orient_type='CURSOR',
            cursor_transform=True)

        return {'FINISHED'}


class TURTLE_OT_down(bpy.types.Operator):
    bl_idname = "turtle.dn"
    bl_label = "Move Down"
    bl_description = "Moves the turtle down. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if context.object['pendownp']:

            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (0, 0, -self.d),
                    "orient_type": 'CURSOR'})

        bpy.ops.transform.translate(
            value=(0, 0, -self.d),
            orient_type='CURSOR',
            cursor_transform=True)

        return {'FINISHED'}


class TURTLE_OT_left(bpy.types.Operator):
    bl_idname = "turtle.lf"
    bl_label = "Move Left"
    bl_description = "Moves the turtle left. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (-self.d, 0, 0),
                    "orient_type": 'CURSOR'})

        bpy.ops.transform.translate(
            value=(-self.d, 0, 0),
            orient_type='CURSOR',
            cursor_transform=True)
        return {'FINISHED'}


class TURTLE_OT_right(bpy.types.Operator):
    bl_idname = "turtle.ri"
    bl_label = "Move Right"
    bl_description = "Moves the turtle right. d = distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (self.d, 0, 0),
                    "orient_type": 'CURSOR'})

        bpy.ops.transform.translate(
            value=(self.d, 0, 0),
            orient_type='CURSOR',
            cursor_transform=True)
        return {'FINISHED'}


class TURTLE_OT_left_turn(bpy.types.Operator):
    bl_idname = "turtle.lt"
    bl_label = "Rotate left"
    bl_description = "Rotate the turtle left. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            turtle.rotation_euler[2] + radians(self.d)]
        return {'FINISHED'}


class TURTLE_OT_right_turn(bpy.types.Operator):
    bl_idname = "turtle.rt"
    bl_label = "Rotate reight"
    bl_description = "Rotate the turtle right. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            turtle.rotation_euler[2] - radians(self.d)]
        return {'FINISHED'}


class TURTLE_OT_look_up(bpy.types.Operator):
    bl_idname = "turtle.lu"
    bl_label = "Turtle look up"
    bl_description = "Pitch turtle up (look up). d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0] + radians(self.d),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_look_down(bpy.types.Operator):
    bl_idname = "turtle.ld"
    bl_label = "Turtle look down"
    bl_description = "Pitch turtle down (look down). d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0] - radians(self.d),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_roll_left(bpy.types.Operator):
    bl_idname = "turtle.rl"
    bl_label = "Turtle roll left"
    bl_description = "Roll turtle around Y axis. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1] - radians(self.d),
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_roll_right(bpy.types.Operator):
    bl_idname = "turtle.rr"
    bl_label = "Turtle roll right"
    bl_description = "Roll turtle around Y axis. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor
        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1] + radians(self.d),
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_set_pos(bpy.types.Operator):
    bl_idname = "turtle.setp"
    bl_label = "Set turtle posiiton"
    bl_description = "moves the turtle to the specified location. v = location"

    v: FloatVectorProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        if bpy.context.object['pendownp']:
            if len(bpy.context.object.data.vertices) == 0:
                bpy.ops.mesh.primitive_vert_add()

            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate={
                    "value": (self.v),
                    "orient_type": 'CURSOR'})

        bpy.context.scene.cursor.location = (self.v)
        return {'FINISHED'}


class TURTLE_OT_set_rotation(bpy.types.Operator):
    bl_idname = "turtle.setrot"
    bl_label = "Set turtle rotation"
    bl_description = "Set the turtles rotation. v = rotation in degrees (0, 0, 0)"

    v: FloatVectorProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            radians(self.v[0]),
            radians(self.v[1]),
            radians(self.v[2])]
        return {'FINISHED'}


class TURTLE_OT_set_heading(bpy.types.Operator):
    bl_idname = "turtle.seth"
    bl_label = "Set turtle heading"
    bl_description = "Rotate the turtle to face the specified horizontal heading. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            radians(self.d)]
        return {'FINISHED'}


class TURTLE_OT_set_pitch(bpy.types.Operator):
    bl_idname = "turtle.setpitch"
    bl_label = "Set turtle pitch"
    bl_description = "Rotate the turtle to face the specified pitch on the X axis. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            radians(self.d),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_set_roll(bpy.types.Operator):
    bl_idname = "turtle.setr"
    bl_label = "Set turtle roll"
    bl_description = "Rotate the turtle around Y. d = degrees"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[1],
            radians(self.d),
            turtle.rotation_euler[2]]
        return {'FINISHED'}


class TURTLE_OT_quadratic_curve(bpy.types.Operator):
    bl_idname = "turtle.qc"
    bl_label = "Quadratic curve"
    bl_description = "moves the turtle on a path described by a quadratic Bezier curve. \
 Keyword Arguments: cp = coordinates of control point, ep = end point"

    cp: FloatVectorProperty()
    ep: FloatVectorProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        turtle = bpy.context.scene.cursor

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if bpy.context.object['pendownp']:
            world = bpy.context.object
            world_name = world.name
            bpy.ops.curve.primitive_bezier_curve_add(
                radius=1,
                enter_editmode=True)

            bpy.ops.curve.select_all(action='DESELECT')

            # set location of first spline point and control point
            bpy.context.active_object.data.splines[0].bezier_points[0].co = (0, 0, 0)
            bpy.context.active_object.data.splines[0].bezier_points[0].handle_right = self.cp

            # set location of second control point.
            bpy.context.active_object.data.splines[0].bezier_points[1].co = self.ep
            bpy.context.active_object.data.splines[0].bezier_points[1].handle_right = self.ep

            # set turtle location
            turtle.location = turtle.location + Vector(self.ep)

            # set turtle rotation
            direction_vec = Vector(self.ep) - Vector(self.cp)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

            bpy.ops.object.editmode_toggle()

            # convert curve to mesh and join to turtle_world object
            bpy.ops.object.convert(target='MESH')
            bpy.data.objects[world.name].select_set(True)
            bpy.ops.object.join()
            bpy.context.object.name = world_name

            # merge vertices
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()

            bpy.ops.mesh.select_all(action='DESELECT')

            # select last vert of converted curve
            lbound = turtle.location
            ubound = turtle.location
            select_by_loc(
                lbound,
                ubound,
                select_mode='VERT',
                coords='GLOBAL',
                buffer=0.001)
        else:
            # set turtle location without drawing anything
            turtle.location = self.ep

            # set turtle rotation
            direction_vec = Vector(self.ep) - Vector(self.cp)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

        return {'FINISHED'}


class TURTLE_OT_cubic_curve(bpy.types.Operator):
    bl_idname = "turtle.cc"
    bl_label = "Cubic curve"
    bl_description = "moves the turtle on a path described by a cubic Bezier curve.\
Keyword Arguments: cp1 / cp2 = coordinates of control points, ep = end point"

    cp1: FloatVectorProperty()
    cp2: FloatVectorProperty()
    ep: FloatVectorProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        turtle = bpy.context.scene.cursor

        if bpy.context.object.get('pendownp') is None:
            # pen state
            bpy.context.object['pendownp'] = True

        if bpy.context.object['pendownp']:
            canvas = bpy.context.object
            canvas_name = canvas.name
            bpy.ops.curve.primitive_bezier_curve_add(
                radius=1,
                enter_editmode=True)
            bpy.ops.curve.select_all(action='DESELECT')
            p0 = bpy.context.active_object.data.splines[0].bezier_points[0]
            p1 = bpy.context.active_object.data.splines[0].bezier_points[1]

            # set location of first spline point and control point
            p0.co = (0, 0, 0)
            bpy.ops.curve.select_all(action='DESELECT')
            p0.select_right_handle = True
            p0.handle_right = self.cp1

            # set location of second spline point and control point
            p1.co = self.ep
            bpy.ops.curve.select_all(action='DESELECT')
            p1.select_left_handle = True
            p1.handle_left = self.cp2

            # set turtle location
            turtle.location = turtle.location + Vector(self.ep)

            # set turtle rotation
            direction_vec = Vector(self.ep) - Vector(self.cp2)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

            bpy.ops.object.editmode_toggle()

            # convert curve to mesh and join to canvas
            bpy.ops.object.convert(target='MESH')
            bpy.data.objects[canvas.name].select_set(True)
            bpy.ops.object.join()
            bpy.context.object.name = canvas_name

            # merge vertices
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()

            bpy.ops.mesh.select_all(action='DESELECT')

            # select last vert of converted curve
            lbound = turtle.location
            ubound = turtle.location
            select_by_loc(
                lbound,
                ubound,
                select_mode='VERT',
                coords='GLOBAL',
                buffer=0.001)
        else:
            # set turtle location without drawing anything
            turtle.location = self.ep

            # set turtle rotation
            direction_vec = Vector(self.ep) - Vector(self.cp2)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

        return {'FINISHED'}


class TURTLE_OT_begin_path(bpy.types.Operator):
    bl_idname = "turtle.bp"
    bl_label = "Begin path"
    bl_description = "Sets begin_path_vert to index of last vert that has been drawn"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        verts = bpy.context.object.data.vertices
        bpy.context.object['beginpath_active_vert'] = verts.values()[-1].index

        return {'FINISHED'}


class TURTLE_OT_stroke_path(bpy.types.Operator):
    bl_idname = "turtle.sp"
    bl_label = "Stroke path"
    bl_description = "draws an edge between selected vert and vert indexed in beginpath"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        if bpy.context.object.get('beginpath_active_vert') is None:
            return {'PASS_THROUGH'}

        bpy.ops.object.editmode_toggle()

        verts = bpy.context.object.data.vertices

        bpy.context.object.data.vertices[-1].select = True
        bpy.context.object.data.vertices[bpy.context.object['beginpath_active_vert']].select = True

        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.editmode_toggle()

        bpy.context.object.data.vertices[-1].select = True

        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TURTLE_OT_fill_path(bpy.types.Operator):
    bl_idname = "turtle.fp"
    bl_label = "Fill path"
    bl_description = "draws an edge between selected vert and vert indexed in beginpath and then creates a face between all verts created since last beginpath statement"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        if bpy.context.object.get('beginpath_active_vert') is None:
            return {'PASS_THROUGH'}

        bpy.ops.object.editmode_toggle()

        verts = bpy.context.object.data.vertices

        i = bpy.context.object['beginpath_active_vert']

        while i <= verts.values()[-1].index:
            bpy.context.object.data.vertices[i].select = True
            i += 1

        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.edge_face_add()

        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        bpy.context.object.data.vertices[-1].select = True

        return {'FINISHED'}


class TURTLE_OT_select_path(bpy.types.Operator):
    bl_idname = "turtle.selp"
    bl_label = "Select Path"
    bl_description = "Selects all verts drawn since last Begin Path command"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()

        verts = bpy.context.object.data.vertices

        i = bpy.context.object['beginpath_active_vert']
        while i <= verts.values()[-1].index:
            bpy.context.object.data.vertices[i].select = True
            i += 1

        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TURTLE_OT_select_all(bpy.types.Operator):
    bl_idname = "turtle.sa"
    bl_label = "Select All"
    bl_description = "Selects All Vertices"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_all(action='SELECT')

        return {'FINISHED'}


class TURTLE_OT_deselect_all(bpy.types.Operator):
    bl_idname = "turtle.da"
    bl_label = "Select All"
    bl_description = "Selects All Vertices"

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_all(action='DESELECT')

        return {'FINISHED'}


class TURTLE_OT_extrude(bpy.types.Operator):
    bl_idname = "turtle.ex"
    bl_label = "Extrude Selected"
    bl_description = "Extrudes Selected Vertices. d = extrude distance in blender units"

    d: FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'EDIT'

    def execute(self, context):
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, 0, self.d),"orient_type": 'NORMAL'})
        return {'FINISHED'}
