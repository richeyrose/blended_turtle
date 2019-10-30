from math import degrees, radians
import bpy
import bmesh
from mathutils import Vector
from . Utils.utils import *

class turtle_commands(bpy.types.Operator):
    bl_idname = "turtle.turtle"
    bl_label = "move turtle"

    pd = bpy.props.BoolProperty()
    pu = bpy.props.BoolProperty()
    fd = bpy.props.FloatProperty()
    bk = bpy.props.FloatProperty()
    lt = bpy.props.FloatProperty()
    rt = bpy.props.FloatProperty()
    
    def execute(self, context):
        if self.pd:
            pen_down()
        if self.pu:
            pen_up()
        if self.fd:
            forward(self.fd)
        if self.lt:
            left_turn(self.lt)
        return {'FINISHED'}


def forward(distance):
        """move turtle forward"""
        bpy.ops.transform.translate(
            value=(0, distance, 0),
            orient_type='CURSOR',
            cursor_transform=True)

        if bpy.context.object['pendownp']:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(0, distance, 0),
                    "orient_type":'CURSOR'})
        return{'FINISHED'}

def left_turn(degrees):
    """rotate turtle left"""
    turtle = bpy.context.scene.cursor
    turtle.rotation_euler = [
    turtle.rotation_euler[0],
    turtle.rotation_euler[1],
    turtle.rotation_euler[2] + radians(degrees)]
    return{'FINISHED'}

def pen_down():
    """pen down"""
    bpy.ops.mesh.primitive_vert_add()
    bpy.context.object['pendownp'] = True

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    return{'FINISHED'}

def pen_up():
    """pen up"""
    bpy.context.object['pendownp'] = False
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    return{'FINISHED'}
class position(bpy.types.Operator):
    bl_idname = "turtle.pos"
    bl_label = "get position"

    def execute(self, context):
        """returns the turtle's position"""
        return bpy.context.scene.cursor.location

class heading(bpy.types.Operator):
    bl_idname = "turtle.heading"
    bl_label = "get heading"

    def execute(self, context):
        """returns the turtle's heading in degrees"""
        rot = bpy.context.scene.cursor.rotation_euler
        return Vector((degrees(rot[0]), degrees(rot[1]), degrees(rot[2])))

'''

    def cs():
        """homes the turtle and deletes all vertices"""
        home()
        delete_all()
        bpy.ops.mesh.primitive_vert_add()
        return {'FINISHED'}

    def home():
        """Moves the turtle to the centre of the canvas and zeros its heading"""
        bpy.context.scene.cursor.location = C.object.location
        bpy.context.scene.cursor.rotation_euler = (0, 0, 0)


    def bk(distance):
        """move turtle backward"""
        bpy.ops.transform.translate(
            value=(0, -distance, 0),
            orient_type='CURSOR',
            cursor_transform=True)

        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(0, -distance, 0),
                    "orient_type":'CURSOR'})

    def up(distance):
        """move turtle up"""
        bpy.ops.transform.translate(
            value=(0, 0, distance),
            orient_type='CURSOR',
            cursor_transform=True)

        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(0, 0, distance),
                    "orient_type":'CURSOR'})

    def dn(distance):
        """move turtle down"""
        bpy.ops.transform.translate(
            value=(0, 0, -distance),
            orient_type='CURSOR',
            cursor_transform=True)

        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(0, 0, -distance),
                "orient_type":'CURSOR'})

    def lf(distance):
        """move turtle left"""
        bpy.ops.transform.translate(
            value = (-distance, 0, 0),
            orient_type ='CURSOR',
            cursor_transform = True)
                
        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(-distance, 0, 0),
                "orient_type":'CURSOR'})
                
    def ri(distance):
        """move turtle right"""
        bpy.ops.transform.translate(
            value = (distance, 0, 0),
            orient_type ='CURSOR',
            cursor_transform = True)
                
        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(distance, 0, 0),
                "orient_type":'CURSOR'})
        
    def lt(degrees):
        """rotate turtle counter-clockwise"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            turtle.rotation_euler[2] - radians(degrees)]

    def rt(degrees):
        """rotate turtle clockwise"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            turtle.rotation_euler[2] + radians(degrees)]

    def lu(degrees):
        """turtle pitch (look) up"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0] + radians(degrees),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]
            
    def ld(degrees):
        """turtle pitch (look) down"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0] + radians(degrees),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]

    def setpos(vector):
        """move turtle to specified location"""
        bpy.context.scene.cursor.location = (vector)

        #if pen is down draw a line to the specified location
        if bpy.context.object:
            bpy.ops.mesh.extrude_vertices_move(
                TRANSFORM_OT_translate=
                {"value":(vector),
                "orient_type":'CURSOR'})
            me = bpy.context.edit_object.data
            bm = bmesh.from_edit_mesh(me)
            
            for v in bm.verts:
                if v.select:
                    v.co = vector
                    
            bmesh.update_edit_mesh(me, True)

    def seth(degrees):
        """rotate the turtle to the specified horizontal heading (yaw / rotate around z)"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            turtle.rotation_euler[0],
            turtle.rotation_euler[1],
            radians(degrees)]

    def setp(degrees):
        """rotate the turtle to the specified vertical heading (pitch aroun x)"""
        turtle = bpy.context.scene.cursor

        turtle.rotation_euler = [
            radians(degrees),
            turtle.rotation_euler[1],
            turtle.rotation_euler[2]]

    def arc(angle, radius, steps):
        """Without moving the turtle, draw an arc centered on the turtle, 
        starting at the turtle's heading"""

        turtle = bpy.context.scene.cursor

        if bpy.context.object:
            #we need to switch back to object mode to get selected verts
            mode('OBJECT')
            selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]
            for v in selected_verts:
                original_vert = v.index
            mode('EDIT')

        deselect_all()

        #add a new vert
        bpy.ops.mesh.primitive_vert_add()

        #transform vert along cursor axis
        bpy.ops.transform.translate(
            value = (0, radius, 0),
            orient_type='CURSOR')

        bpy.ops.mesh.spin(
            steps=steps,
            angle=radians(angle),
            center=turtle.location,
            axis=turtle.rotation_euler)

        deselect_all()

        if bpy.context.object:
            me = bpy.context.edit_object.data
            bm = bmesh.from_edit_mesh(me)
            bm.verts.ensure_lookup_table()
            bm.verts[original_vert].select_set(True)
            bmesh.update_edit_mesh(me, True)

    def clean():
        """deletes mesh, leaves turtle where it is"""
        delete_all()
        if bpy.context.object:
            bpy.ops.mesh.primitive_vert_add()
            
    def qc(cp, ep):
        """moves the turtle on a path described by a quadratic Bezier curve.
        
        Keyword Arguments:
        cp -- coordinates of control point
        ep -- coordinate of end point

        """
        turtle = bpy.context.scene.cursor

        if bpy.context.object:
            world = bpy.context.object
            world_name = world.name
            bpy.ops.curve.primitive_bezier_curve_add(
                radius=1,
                enter_editmode=True)
            
            bpy.ops.curve.select_all(action='DESELECT')
            
            #set location of first spline point and control point
            bpy.context.active_object.data.splines[0].bezier_points[0].co = (0,0,0) 
            bpy.context.active_object.data.splines[0].bezier_points[0].handle_right = cp
            
            #set location of second control point. 
            bpy.context.active_object.data.splines[0].bezier_points[1].co = ep
            bpy.context.active_object.data.splines[0].bezier_points[1].handle_right = ep
            
            #set turtle location
            turtle.location = turtle.location + Vector(ep)
            
            #set turtle rotation
            direction_vec = Vector(ep) - Vector(cp)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'
            
            mode('OBJECT')
            
            #convert curve to mesh and join to canvas
            bpy.ops.object.convert(target='MESH')
            bpy.data.objects[world.name].select_set(True)
            bpy.ops.object.join()
            bpy.context.object.name = world_name
            
            #merge vertices
            mode('EDIT')
            select_all()
            bpy.ops.mesh.remove_doubles()
                
            deselect_all()
            
            #select last vert of converted curve
            lbound = turtle.location
            ubound = turtle.location
            select_by_loc(
                lbound,
                ubound,
                select_mode='VERT',
                coords='GLOBAL',
                buffer = 0.001
                )
        else:
            #set turtle location without drawing anything
            turtle.location = ep
            
            #set turtle rotation
            direction_vec = Vector(ep) - Vector(cp)
            rot_quat = direction_vec.to_track_quat('Y', 'Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

    def cc(cp1, cp2, ep):
        """moves the turtle on a path described by a cubic Bezier curve.

        Keyword Arguments:
        cp1 -- coordinates of control point1
        cp2 -- coordinates of control point2
        ep -- coordinate of end point
        """
        turtle = bpy.context.scene.cursor

        if bpy.context.object:
            canvas = bpy.context.object
            canvas_name = canvas.name
            bpy.ops.curve.primitive_bezier_curve_add(
                radius=1,
                enter_editmode=True)
            bpy.ops.curve.select_all(action='DESELECT')        
            p0 = bpy.context.active_object.data.splines[0].bezier_points[0]
            p1 = bpy.context.active_object.data.splines[0].bezier_points[1]

            #set location of first spline point and control point
            p0.co = (0, 0, 0)
            bpy.ops.curve.select_all(action='DESELECT')
            p0.select_right_handle = True
            p0.handle_right = cp1

            #set location of second spline point and control point
            p1.co = ep
            bpy.ops.curve.select_all(action='DESELECT')
            p1.select_left_handle = True
            p1.handle_left = cp2
            
            #set turtle location
            turtle.location = turtle.location + Vector(ep)
            
            #set turtle rotation
            direction_vec = Vector(ep) - Vector(cp2)
            rot_quat = direction_vec.to_track_quat('Y','Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'
            
            mode('OBJECT')
            
            #convert curve to mesh and join to canvas
            bpy.ops.object.convert(target='MESH')
            bpy.data.objects[canvas.name].select_set(True)
            bpy.ops.object.join()
            bpy.context.object.name = canvas_name
            
            #merge vertices
            mode('EDIT')
            select_all()
            bpy.ops.mesh.remove_doubles()
                
            deselect_all()
            
            #select last vert of converted curve
            lbound = turtle.location
            ubound = turtle.location
            select_by_loc(
                lbound,
                ubound,
                select_mode='VERT',
                coords='GLOBAL',
                buffer = 0.001
                )
        else:
            #set turtle location without drawing anything
            turtle.location = ep
            
            #set turtle rotation
            direction_vec = Vector(ep) - Vector(cp2)
            rot_quat = direction_vec.to_track_quat('Y','Z')
            turtle.rotation_mode = 'QUATERNION'
            turtle.rotation_quaternion = rot_quat
            turtle.rotation_mode = 'XYZ'

    def beginpath():
        """Sets begin_path_vert to index of selected vert
        """
        #TODO: find a better way of updating whether vert is selected!
        
        if bpy.context.object:
            bpy.ops.object.mode_set(mode='OBJECT')    
            verts = bpy.context.object.data.vertices
            i = 0
            for v in verts:
                if v.select:
                    bpy.context.object['beginpath_active_vert'] = i
                i += 1
            bpy.ops.object.mode_set(mode='EDIT')
        
    def strokepath():
        """draws an edge between selected vert and vert indexed in beginpath"""
        if bpy.context.object:
            bpy.ops.object.mode_set(mode='OBJECT')
            verts = bpy.context.object.data.vertices
            endpath_vert_index = 0
            
            i = 0
            for v in verts:
                if v.select:
                    endpath_vert_index = i
                i += 1

            bpy.context.object.data.vertices[bpy.context.object['beginpath_active_vert']].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.edge_face_add()
            deselect_all()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.object.data.vertices[endpath_vert_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            
    def fillpath():
        """draws an edge between selected vert and vert indexed in beginpath
        and then creates a face between all verts created since last beginpath statement"""    
        if bpy.context.object:
            bpy.ops.object.mode_set(mode='OBJECT')
            verts = bpy.context.object.data.vertices

            endpath_vert_index = 0
            
            i = 0
            for v in verts:
                if v.select:
                    endpath_vert_index = i
                i += 1
            
            i = bpy.context.object['beginpath_active_vert']
            while i < endpath_vert_index:
                bpy.context.object.data.vertices[i].select = True
                i+= 1
                
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.edge_face_add()
            bpy.ops.mesh.edge_face_add()
            deselect_all()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.object.data.vertices[endpath_vert_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')

    def extrudepath(distance):
        """Extrudes the path along its normal"""
        if bpy.context.object:
            bpy.ops.object.mode_set(mode='OBJECT')
            verts = bpy.context.object.data.vertices

            endpath_vert_index = 0
            
            i = 0
            for v in verts:
                if v.select:
                    endpath_vert_index = i
                i += 1
            
            i = bpy.context.object['beginpath_active_vert']
            while i < endpath_vert_index:
                bpy.context.object.data.vertices[i].select = True
                i += 1
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value":(0, 0, distance)})
            deselect_all()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.object.data.vertices[endpath_vert_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')
'''
