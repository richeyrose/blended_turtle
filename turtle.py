from math import degrees, radians
import bpy
import bmesh
from mathutils import Vector
from bpy.props import BoolProperty

C = bpy.context
D = bpy.data
O = bpy.ops
S = C.scene

turtle = C.scene.cursor

bpy.types.Scene.pendownp = bpy.props.BoolProperty(default=True)
bpy.types.Scene.beginpath_vert_index = bpy.props.IntProperty()

def new_canvas():
    """Create a new canvas"""
    
    #zero the turtle rotation
    turtle.rotation_euler = (0,0,0)
    
    if len(D.objects) != 0:
        mode('OBJECT')

    #create "turtle" collection if one doesn't already exist
    scene_collection = C.scene.collection

    #create new mesh
    canvas_mesh = D.meshes.new("canvas_mesh")
    new_canvas = D.objects.new("canvas", canvas_mesh)

    if not "Turtle" in D.collections:
        turtle_collection = D.collections.new("Turtle")
        #link turtle collection to scene collection
        scene_collection.children.link(turtle_collection)
    
    turtle_collection = D.collections["Turtle"]
   
    #add canvas to collection
    turtle_collection.objects.link(new_canvas)
    layer_collection = C.view_layer.layer_collection.children[turtle_collection.name]
    C.view_layer.active_layer_collection = layer_collection
    
    new_canvas.location = turtle.location
    
    select(new_canvas.name)
    activate(new_canvas.name)
    mode('EDIT')
    home()
    
    pd()

    return new_canvas

def pd():
    """pen down"""
    O.mesh.primitive_vert_add()
    S.pendownp =True

def pu():
    """pen up"""
    deselect_all()
    S.pendownp = False
    
def pos():
    """returns the turtle's position"""
    return turtle.location

def heading():
    """returns the turtle's heading in degrees"""
    rot = turtle.rotation_euler
    return Vector((degrees(rot[0]), degrees(rot[1]), degrees(rot[2])))

def cs():
    """homes the turtle and deletes all vertices"""
    home()
    delete_all()
    O.mesh.primitive_vert_add()
    return {'FINISHED'}

def home():
    """Moves the turtle to the centre of the canvas and zeros its heading"""
    C.scene.cursor.location = C.object.location
    C.scene.cursor.rotation_euler = (0, 0, 0)
    

def fd(distance):
    """move turtle forward"""
    bpy.ops.transform.translate(
        value = (0, distance, 0),
        orient_type ='CURSOR',
        cursor_transform = True)        
    
    if S.pendownp:
        bpy.ops.mesh.extrude_vertices_move(
            TRANSFORM_OT_translate=
            {"value":(0, distance, 0),
             "orient_type":'CURSOR'})
  
def bk(distance):
    """move turtle backward"""
    bpy.ops.transform.translate(
        value = (0, -distance, 0),
        orient_type ='CURSOR',
        cursor_transform = True)
            
    if S.pendownp:
        bpy.ops.mesh.extrude_vertices_move(
            TRANSFORM_OT_translate=
            {"value":(0, -distance, 0),
             "orient_type":'CURSOR'})
            
def up(distance):
    """move turtle up"""
    bpy.ops.transform.translate(
        value = (0, 0, distance),
        orient_type ='CURSOR',
        cursor_transform = True)
            
    if S.pendownp:
        bpy.ops.mesh.extrude_vertices_move(
            TRANSFORM_OT_translate=
            {"value":(0, 0, distance),
             "orient_type":'CURSOR'})
             
def dn(distance):
    """move turtle down"""
    bpy.ops.transform.translate(
        value = (0, 0, -distance),
        orient_type ='CURSOR',
        cursor_transform = True)
            
    if S.pendownp:
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
            
    if S.pendownp:
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
            
    if S.pendownp:
        bpy.ops.mesh.extrude_vertices_move(
            TRANSFORM_OT_translate=
            {"value":(distance, 0, 0),
             "orient_type":'CURSOR'})
       
def lt(degrees):
    """rotate turtle counter-clockwise"""
    turtle.rotation_euler = [
        turtle.rotation_euler[0],
        turtle.rotation_euler[1],
        turtle.rotation_euler[2] - radians(degrees)]

def rt(degrees):
    """rotate turtle clockwise"""
    turtle.rotation_euler = [
        turtle.rotation_euler[0],
        turtle.rotation_euler[1],
        turtle.rotation_euler[2] + radians(degrees)]

def lu(degrees):
    """turtle pitch (look) up"""
    turtle.rotation_euler = [
        turtle.rotation_euler[0] + radians(degrees),
        turtle.rotation_euler[1],
        turtle.rotation_euler[2]]
        
def ld(degrees):
    """turtle pitch (look) down"""
    turtle.rotation_euler = [
        turtle.rotation_euler[0] + radians(degrees),
        turtle.rotation_euler[1],
        turtle.rotation_euler[2]]

def setpos(vector):
    """move turtle to specified location"""    
    turtle.location=(vector)
    
    #if pen is down draw a line to the specified location
    if S.pendownp:
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
    turtle.rotation_euler = [
        turtle.rotation_euler[0],
        turtle.rotation_euler[1],
        radians(degrees)]

def setp(degrees):
    """rotate the turtle to the specified vertical heading (pitch aroun x)"""
    turtle.rotation_euler = [
        radians(degrees),
        turtle.rotation_euler[1],
        turtle.rotation_euler[2]]

def arc(angle, radius, steps):
    """Without moving the turtle, draw an arc centered on the turtle, 
    starting at the turtle's heading"""
    if S.pendownp:
        #we need to switch back to object mode to get selected verts
        mode('OBJECT')
        selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]
        for v in selected_verts:
            original_vert = v.index
        mode('EDIT')
    
    deselect_all()
    
    #add a new vert
    O.mesh.primitive_vert_add()
    
    #transform vert along cursor axis
    bpy.ops.transform.translate(
        value = (0, radius, 0),
        orient_type ='CURSOR')
    
    bpy.ops.mesh.spin(
        steps=steps, 
        angle=radians(angle), 
        center=turtle.location, 
        axis=turtle.rotation_euler)
    
    deselect_all()
    
    if S.pendownp:
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        bm.verts.ensure_lookup_table()
        bm.verts[original_vert].select_set(True)
        bmesh.update_edit_mesh(me, True)
    
def clean():
    """deletes mesh, leaves turtle where it is"""
    delete_all()
    if S.pendownp:
        O.mesh.primitive_vert_add()
        
def qc(cp, ep):
    """moves the turtle on a path described by a quadratic Bezier curve.
    
    Keyword Arguments:
    cp -- coordinates of control point
    ep -- coordinate of end point

    """
    if S.pendownp:
        canvas = bpy.context.object
        canvas_name = canvas.name
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
        turtle.location=ep
        
        #set turtle rotation
        direction_vec = Vector(ep) - Vector(cp)
        rot_quat = direction_vec.to_track_quat('Y','Z')
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
    
    if S.pendownp:
        canvas = bpy.context.object
        canvas_name = canvas.name
        bpy.ops.curve.primitive_bezier_curve_add(
            radius=1, 
            enter_editmode=True)
        bpy.ops.curve.select_all(action='DESELECT')        
        p0 = bpy.context.active_object.data.splines[0].bezier_points[0]
        p1 = bpy.context.active_object.data.splines[0].bezier_points[1]
        
        #set location of first spline point and control point
        p0.co = (0,0,0)
        bpy.ops.curve.select_all(action='DESELECT')
        p0.select_right_handle = True
        p0.handle_right = cp1

        #set location of second spline point and control point
        p1.co = ep
        bpy.ops.curve.select_all(action='DESELECT')
        p1.select_left_handle= True
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
        turtle.location=ep
        
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
    
    if S.pendownp:
        O.object.mode_set(mode='OBJECT')    
        verts = bpy.context.object.data.vertices
        i = 0
        for v in verts:
            if v.select:
                S.beginpath_vert_index = i
            i += 1
        O.object.mode_set(mode='EDIT')
    
def strokepath():
    """draws an edge between selected vert and vert indexed in beginpath"""
    if S.pendownp:
        O.object.mode_set(mode='OBJECT')
        verts = bpy.context.object.data.vertices
        endpath_vert_index = 0
        
        i = 0
        for v in verts:
            if v.select:
                endpath_vert_index = i
            i += 1

        bpy.context.object.data.vertices[S.beginpath_vert_index].select = True
        O.object.mode_set(mode='EDIT')
        bpy.ops.mesh.edge_face_add()
        deselect_all()
        O.object.mode_set(mode='OBJECT')
        bpy.context.object.data.vertices[endpath_vert_index].select = True
        O.object.mode_set(mode='EDIT')
        
def fillpath():
    """draws an edge between selected vert and vert indexed in beginpath
    and then creates a face between all verts created since last beginpath statement"""    
    if S.pendownp:
        O.object.mode_set(mode='OBJECT')
        verts = bpy.context.object.data.vertices

        endpath_vert_index = 0
        
        i = 0
        for v in verts:
            if v.select:
                endpath_vert_index = i
            i += 1
        
        i = S.beginpath_vert_index
        while i < endpath_vert_index:
            bpy.context.object.data.vertices[i].select = True
            i+= 1
            
        O.object.mode_set(mode='EDIT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.edge_face_add()
        deselect_all()
        O.object.mode_set(mode='OBJECT')
        bpy.context.object.data.vertices[endpath_vert_index].select = True
        O.object.mode_set(mode='EDIT')

def extrudepath(distance):
    """Extrudes the path along its normal"""
    if S.pendownp:
        O.object.mode_set(mode='OBJECT')
        verts = bpy.context.object.data.vertices

        endpath_vert_index = 0
        
        i = 0
        for v in verts:
            if v.select:
                endpath_vert_index = i
            i += 1
        
        i = S.beginpath_vert_index
        while i < endpath_vert_index:
            bpy.context.object.data.vertices[i].select = True
            i+= 1
        
        O.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0,0,distance)})
        deselect_all()
        O.object.mode_set(mode='OBJECT')
        bpy.context.object.data.vertices[endpath_vert_index].select = True
        O.object.mode_set(mode='EDIT')
        
    
'''utilities'''
def select_all():
    """Selects all objects if in OBJECT mode or verts / edges / faces if in EDIT mode"""
    if len(D.objects) != 0:
        current_mode = C.object.mode
        if current_mode == 'EDIT':
            O.mesh.select_all(action="SELECT")
            return {'FINSIHED'}
        elif current_mode == 'OBJECT':
            O.object.select_all(action="SELECT")
            return {'FINISHED'}
        else:
            return {'FINSIHED'}

def deselect_all(): #TODO:make work with curves
    """Deselects all objects if in OBJECT mode or verts / edges / faces if in EDIT mode"""
    if len(D.objects) != 0:    
        current_mode = C.object.mode
        if current_mode == 'EDIT':
            O.mesh.select_all(action="DESELECT")
            return {'FINISHED'}
        if current_mode == 'OBJECT':
            O.object.select_all(action="DESELECT")
            return {'FINISHED'}

    return {'FINSIHED'}

def delete_all():
    """delete all objects or verts / edges /faces"""
    if len(D.objects) != 0:
        current_mode = C.object.mode
        if current_mode == 'OBJECT':
            select_all()
            O.object.delete(use_global=False)
        if current_mode == 'EDIT':
            select_all()
            O.mesh.delete()

def mode(mode_name):
    """switch modes, ensuring that if we enter edit mode we deselect all selected vertices"""
    if len(D.objects) != 0:
        O.object.mode_set(mode=mode_name)
        if mode_name == "EDIT":
            O.mesh.select_all(action="DESELECT")

#select object by name
def select(obj_name):
    """select object by name"""
    O.object.select_all(action='DESELECT')
    D.objects[obj_name].select_set(True)

def activate(obj_name):
    """activate object by name """
    C.view_layer.objects.active = D.objects[obj_name]
    
def in_bbox(lbound, ubound, v, buffer=0.001):
    """Returns vertices that are in a bounding box
    
    Keyword arguments:
        
    lbound -- lower left bound of bounding box
    rbound -- upper right bound of bounding box
    v -- verts
    buffer - buffer around selection box within which to also select verts
    """
    return lbound[0]-buffer <=v[0]<=ubound[0]+buffer and \
        lbound[1]-buffer<=v[1]<=ubound[1]+buffer and \
        lbound[2]-buffer<=v[2]<=ubound[2]+buffer

def select_by_loc(lbound=(0,0,0), ubound=(0,0,0), 
    select_mode='VERT', coords='GLOBAL', buffer = 0.001):
        """select faces, edges or verts by location that are wholly 
        within a boundingcuboid
        
        Keyword arguments:
            
        lbound -- lower left bound of bounding box
        rbound -- upper right bound of bounding box
        select_mode -- default 'VERT'
        coords -- default 'GLOBAL'
        buffer - buffer around selection default = 0.001
        """
        
        #set selection mode
        bpy.ops.mesh.select_mode(type=select_mode)
        #grab the transformation matrix
        world = bpy.context.object.matrix_world
        
        #instantiate a bmesh object and ensure lookup table (bm.faces.ensure... works for all)
        bm = bmesh.from_edit_mesh(bpy.context.object.data)
        bm.faces.ensure_lookup_table()
        
        #initialise list of verts and parts to be selected
        verts=[]
        to_select=[]
        
        #for VERT, EDGE or FACE
            #grab list of global or local coords
            #test if the piece is entirely within the rectangular
            #prism defined by lbound and ubound
            #select each piece that returned TRUE and deselect each piece that returned FALSE
            
        if select_mode=='VERT':
            if coords =='GLOBAL':
                [verts.append((world @ v.co).to_tuple())for v in bm.verts]
            elif coords == 'LOCAL':
                [verts.append(v.co.to_tuple())for v in bm.verts]
        
            [to_select.append(in_bbox(lbound, ubound, v))for v in verts]
            
            for vertObj, select in zip(bm.verts, to_select):
                vertObj.select = select
        
        if select_mode == 'EDGE':
            if coords == 'GLOBAL':
                [verts.append([(world @ v.co).to_tuple() for v in e.verts]) for e in bm.edges]
            elif coords=='LOCAL':
                [verts.append([v.co.to_tuple()for v in e.verts]) for e in bm.edges]
                
            [to_select.append(all(in_bbox(lbound, ubound, v)for v in e)) for e in verts]
            
            for edgeObj, select in zip(bm.edges, to_select):
                edgeObj.select = select
                
        if select_mode == 'FACE':
            if coords == 'GLOBAL':
                [verts.append([(world @ v.co).to_tuple() for v in f.verts])for f in bm.faces]
            elif coords == 'LOCAL':
                [verts.append([v.co.to_tuple()for v in f.verts]) for f in bm.faces]
            
            [to_select.append(all(in_bbox(lbound, ubound, v, buffer) for v in f))for f in verts]
            
            for faceObj, select in zip(bm.faces,to_select):
                faceObj.select = select