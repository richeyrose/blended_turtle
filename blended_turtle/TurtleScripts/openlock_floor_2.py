from math import floor, sqrt
import bpy
from mathutils import *

turtle = bpy.context.scene.cursor
t = bpy.ops.turtle

outer_w = 6                 # outer ring width
slot_w = 4.7                # slot width
slot_h = 6.1                # slot height
support_w = 3               # slot support width
support_h = 1.39            # slot support height
extra_sup_dist = 21.68      # distance between extra supports for large tiles


def make_floor(dimensions=(25.4, 25.4, 7)):
    x = dimensions[0]
    y = dimensions[1]
    z = dimensions[2]

    t.add_turtle()

    # We want our tile to have its origin at the center
    # so we make sure the pen is up
    # and move the cursor back along the Y axis by 0.5 Y
    t.pu()
    t.bk(d=y / 2)
    t.pd()
    t.add_vert()
    start_loc = turtle.location.copy()

    draw_quarter_floor(dimensions, start_loc)

    
def draw_quarter_floor(dimensions, start_loc):
    x = dimensions[0]
    y = dimensions[1]
    
    # draw loop 1
    t.ri(d=x / 2)
    t.fd(d=y / 2)
    
    #move turtle
    t.pu()
    t.deselect_all()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.pd()
    
    # draw loop 2
    t.add_vert()
    t.begin_path()
    t.ri(d=x / 2 - outer_w)
    t.fd(d=y / 2 - outer_w)
    t.select_path()
    
    # create bevel for corner supports
    bpy.ops.mesh.bevel(offset_type='WIDTH', offset=3, offset_pct=0, vertex_only=True)

    # move turtle
    t.pu()
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w + slot_w)
    t.pd()

    # draw loop 3
    t.add_vert()
    t.begin_path()
    t.ri(d= x / 2 - slot_w - outer_w)
    t.fd(d= y / 2 - slot_w - outer_w)
    t.select_path()
    
    # create bevel for corner supports
    bpy.ops.mesh.bevel(offset_type='WIDTH', offset=3, offset_pct=0, vertex_only=True)
    
    # move cursor
    leg = support_w / sqrt(2)
    t.pu()
    t.bk(d=y / 2 - outer_w)
    t.lf(d=leg)

    # select bevels
    t.select_by_location(
                lbound=turtle.location,
                ubound=(x / 2 - outer_w,
                        turtle.location[1] + slot_w + leg,
                        turtle.location[2]))

    # delete bevel edges
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.delete(type='EDGE')
    
    # create bridges
    t.fd(d=slot_w)
    t.select_at_cursor()
    t.set_position(v=(start_loc))
    t.fd(d=outer_w)
    t.ri(d=x / 2 - outer_w - leg)
    t.select_at_cursor()
   
    bpy.ops.mesh.edge_face_add()
    t.deselect_all()
    
    t.set_position(v=(start_loc))
    t.fd(d=outer_w + leg)
    t.ri(d=x / 2 - outer_w)
    t.select_at_cursor()
    t.fd(d=slot_w)
    t.lf(d=slot_w)
    t.select_at_cursor()
        
    bpy.ops.mesh.edge_face_add()
    t.deselect_all()
    
    
           

    # check if either side is greater than 101.6mm (6").
    # if yes we add some extra support between outer and inner ring

    x_supports = floor(x / 101.6)
    y_supports = floor(y / 101.6)
    
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.rt(d=90) 
    if x_supports > 0:
        add_extra_supports(x_supports, 'x', support_w, slot_w)
    t.home()
    t.ri(d=x / 2 - outer_w)
    t.rt(d=180)
    if y_supports > 0:
        add_extra_supports(y_supports, 'y', -support_w, -slot_w)


    
def add_extra_supports(num_supports, axis, support_w, slot_w):
    for i in range(num_supports):
        if i == 0:
            t.fd(d=extra_sup_dist / 2)
        else:
            t.fd(d=extra_sup_dist + (extra_sup_dist / 2))

        t.add_vert()
        t.begin_path()
        t.fd(d=support_w)
        t.add_vert()
        t.select_path()
        t.pd()
        t.lf(d=slot_w)
        t.ri(d=slot_w)
        t.select_all()
        bpy.ops.tinycad.intersectall()
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        t.deselect_all()
        '''
        t.pu()
        t.ri(d=slot_w)
        t.select_at_cursor()
        t.bk(d=support_w)
        t.select_at_cursor()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='EDGE')
        t.select_at_cursor()
        t.fd(d=support_w)
        t.select_at_cursor()
        t.lf(d=slot_w)
        t.select_at_cursor()
        t.bk(d=support_w)
        t.select_at_cursor()
        t.pd()
        t.up(d=support_h)
        bpy.ops.mesh.edge_face_add()
        t.pu()
        t.select_all()
        t.merge()
        t.deselect_all()
        t.dn(d=support_h)
        t.ri(d=slot_w)
        '''
'''
make_floor(dimensions=(25.4, 25.4, 7))
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.scene.cursor.location = (50, 0, 0)
make_floor(dimensions=(25.4, 50.8, 7))
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.scene.cursor.location = (100, 0, 0)
make_floor(dimensions=(101.6, 50.8, 7))
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
bpy.context.scene.cursor.location = (0, -50, 0)
'''
bpy.context.scene.cursor.location = (0, 0, 0)
make_floor(dimensions=(205, 205, 7))
