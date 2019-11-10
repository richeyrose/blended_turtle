from math import floor, sqrt
import bpy
from mathutils import *

turtle = bpy.context.scene.cursor
t = bpy.ops.turtle

outer_w = 6                 # outer ring width
slot_w = 4.6                # slot width
slot_h = 6.1                # slot height
support_w = 3               # slot support width
support_h = 1.39            # slot support height
extra_sup_dist = 23.4      # distance between extra supports for large tiles


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
    z = dimensions[2]
    
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

    #bridge bevels
    leg = support_w / sqrt(2)
    t.pu()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w + slot_w)
    t.ri(d=x / 2 - outer_w - slot_w - leg)

    t.select_at_cursor()
    t.bk(d=slot_w)
    t.ri(d=slot_w)
    t.select_at_cursor()
    

    t.ri(d=leg)
    t.fd(d=leg)
    t.select_at_cursor()

    t.fd(d=slot_w)
    t.lf(d=slot_w)
    t.select_at_cursor()
    bpy.ops.mesh.edge_face_add()
    t.deselect_all()
    t.select_at_cursor()
    t.lf(d=leg)   
    t.bk(d=leg)
    t.select_at_cursor()
    bpy.ops.mesh.delete(type='EDGE')

    t.bk(d=slot_w)
    t.ri(d=slot_w)
    t.select_at_cursor()
    t.fd(d=leg)
    t.ri(d=leg)
    t.select_at_cursor()
    bpy.ops.mesh.delete(type='EDGE')
    
    

    # check if either side is greater than 101.6mm (4").
    # if yes we add some extra support between outer and inner ring
    if x >= 101.6:
        x_supports = 1 + floor((x - 101.6) / 50.8)
    else: x_supports = 0

    if y >= 101.6:
        y_supports = 1 + floor((y - 101.6) / 50.8)
    else: y_supports = 0

    t.home()
    t.pu()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.rt(d=90) 
    
    if x_supports > 0:
        add_extra_supports(x_supports, 'x', support_w, slot_w, x, y, leg, outer_w, start_loc)
    '''
    t.home()
    t.ri(d=x / 2 - outer_w)
    t.rt(d=180)
    
    if y_supports > 0:
        add_extra_supports(y_supports, 'y', support_w, slot_w)
    
    t.pu()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.rt(d=90)
 
    if x_supports > 0:
        clean_extra_supports(x_supports, 'x', support_w, slot_w)

    t.home()
    t.ri(d=x / 2 - outer_w)

    if y_supports > 0:
        clean_extra_supports(y_supports, 'y', support_w, slot_w)

    # extrude inner sides up 1
    t.pd()
    t.select_all()
    t.up(d=support_h)
    t.select_all()
    t.merge()
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)

    #join outer edges
    t.pd()    
    t.select_at_cursor()
    t.fd(d=outer_w)
    t.deselect_all()
    t.pu()
    t.fd(d=slot_w)  
    t.pd()
    t.select_at_cursor()
    t.fd(d=y / 2 - slot_w - outer_w)
    t.ri(d = x / 2 - slot_w - outer_w)
    t.pu()
    t.deselect_all()
    t.ri(d=slot_w)
    t.pd()
    t.select_at_cursor()
    t.ri(d=outer_w)
    t.select_all()
    t.merge()
    
 
    # fill base
    t.pu()
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.select_by_location(
            lbound=turtle.location, 
            ubound=(turtle.location[0] + x / 2,
                    turtle.location[1] + y / 2,
                    turtle.location[2]))
               
    bpy.ops.mesh.fill()
    t.select_all()
    bpy.ops.mesh.normals_make_consistent()


    # draw extra support roofs
    t.pu()
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.rt(d=90) 
    t.up(d=support_h)

    if x_supports > 0:
        fill_extra_supports(x_supports, 'x', support_w, slot_w)
        
    t.home()
    t.ri(d=x / 2 - outer_w)
    t.rt(d=180)
    t.up(d=support_h)
    
    if y_supports > 0:
        fill_extra_supports(y_supports, 'y', support_w, slot_w)

    # draw corner support roofs
    t.deselect_all()
    t.pu
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.up(d=support_h)
    t.ri(d=x / 2 - outer_w - leg)
    t.select_at_cursor()
    t.ri(d=leg)
    t.fd(d=leg)
    t.select_at_cursor()

    t.fd(d=slot_w)
    t.lf(d=slot_w)
    t.select_at_cursor()
    t.lf(d=leg)
    t.bk(d=leg)
    t.select_at_cursor()
    bpy.ops.mesh.edge_face_add()

   
    #bridge_slot
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.up(d=support_h)
    t.select_at_cursor()
    t.pd()
    t.fd(d=slot_w)
    t.deselect_all()
    t.pu()
    t.ri(d=x / 2 - outer_w - slot_w)
    t.fd(d=y / 2 - outer_w - slot_w)
    t.select_at_cursor()
    t.pd()
    t.ri(d=slot_w)
    t.pu()

    #draw duplicate top of supports and slot
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.up(d=support_h)
    t.select_by_location(
                lbound=turtle.location,
                ubound=(turtle.location[0] + x / 2 - outer_w,
                        turtle.location[1] + y / 2 - outer_w,
                        turtle.location[2]))
    
    bpy.ops.mesh.duplicate_move(
        TRANSFORM_OT_translate={
                    "value": (0, 0, slot_h - support_h),
                    "orient_type": 'CURSOR'})
    t.merge()
    bpy.ops.mesh.edge_face_add()
    


    # extrude down and clean
    t.pd()
    t.dn(d=slot_h - support_h)
    bpy.ops.mesh.delete(type='FACE')

    # clean non-manifolds at end
    t.pu()
    t.deselect_all()
    t.home()
    t.set_position(v=start_loc)
    t.fd(d=outer_w)
    t.up(d=support_h)
    t.select_at_cursor()
    t.fd(d=slot_w)
    t.select_at_cursor()
    bpy.ops.mesh.delete(type='EDGE')

    t.ri(d= x / 2 - outer_w)
    t.fd(d=y / 2 - outer_w - slot_w)
    t.select_at_cursor()
    t.lf(d=slot_w)
    t.select_at_cursor()

    bpy.ops.mesh.delete(type='EDGE')

    # draw outer wall
    t.pu()
    t.home()
    t.set_position(v=start_loc)
    t.up(d=support_h)
    t.select_at_cursor()
    t.ri(d=x / 2)
    t.select_at_cursor()
    t.fd(d=y / 2)
    t.select_at_cursor()
    t.pd()
    t.up(d=z - support_h)

    # draw top
    t.pu()
    t.deselect_all()
    t.home()
    t.up(d=z)
    t.pd()  
    t.add_vert()
    t.begin_path()
    t.ri(d=x / 2)
    t.select_path()
    t.bk(d=y / 2)

    #clean up
    t.select_all()
    t.merge()
    bpy.ops.mesh.normals_make_consistent()
    t.deselect_all()
    t.home()

    '''
      
    
def add_extra_supports(num_supports, axis, support_w, slot_w, x, y, leg, outer_w, start_loc):

    t.select_at_cursor()
    bpy.ops.mesh.select_more()
    bpy.ops.mesh.subdivide(number_cuts=num_supports * 2)

    if axis == 'x':
        subdivision_dist=((x /2 )- outer_w - leg)  / ((num_supports * 2) + 1)
        t.deselect_all()

        for i in range(num_supports*2):
            if i == 0:
                t.fd(d=subdivision_dist)
                t.select_at_cursor()
                t.pd()
                t.bk(d=subdivision_dist, m = True)
                t.fd(d=extra_sup_dist / 2, m = True)
                t.pu()
                t.deselect_all()
                t.bk(d=extra_sup_dist / 2)
                t.fd(d=subdivision_dist)
            elif i == 1:
                t.fd(d=subdivision_dist)
                t.select_at_cursor()
                t.pd()
                t.bk(d=subdivision_dist * 2 - extra_sup_dist / 2 - support_w, m = True)
                t.pu()
                t.deselect_all()
            else:
                t.set_position(v=start_loc)
                t.lf(d=outer_w)
                t.fd(d=subdivision_dist * (i + 1) )
                t.select_at_cursor()
                t.pd()
                t.bk(d=subdivision_dist * (i + 1), m = True)
                t.fd(d=extra_sup_dist / 2 + support_w, m = True)
                if i % 2 == 0:
                    t.fd(d=extra_sup_dist * (i-1), m = True)
                else:
                    t.fd(d=extra_sup_dist * (i-2) + support_w, m = True)
                t.pu()
                t.deselect_all()
            
            
            '''            
            t.fd(d=extra_sup_dist * i -1, m = True)
            
            if i % 2 == 0:
                t.fd(d=support_w, m = True)
            t.pu()
            t.deselect_all()


                
            
                
            #t.fd(d=support_w, m = True)

        

        elif i == 1:
            t.pd()[
            t.bk(d=subdivision_dist, m = True)
            t.fd(d=extra_sup_dist / 2 + support_w, m = True)
            t.pu()
            t.deselect_all()
            t.bk(d=extra_sup_dist / 2 + support_w)
            t.fd(d=subdivision_dist)

    
    
    


    t.pd()
    t.bk(d=subdivision_dist, m=True)
    t.fd(d=extra_sup_dist / 2, m=True)
    t.deselect_all
    t.pu()
    t.fd(d=subdivision_dist)

#    bpy.ops.transform.translate(value=(extra_sup_dist / 2, 0, 0))
    t.deselect_all()
    t.bk(d=subdivision_dist)
    t.fd(d=subdivision_dist * 2)
    t.select_at_cursor()
    bpy.ops.transform.translate(value=((subdivision_dist * 2)*-1, 0, 0))
    bpy.ops.transform.translate(value=((extra_sup_dist / 2) + support_w, 0, 0))
    
    

#    for i in range(num_supports):
#        if i == 0:
        if axis == 'x':
        t.fd(d=extra_sup_dist / 2)
    else:
        t.bk(d=extra_sup_dist / 2)  
    add_support(axis, slot_w, support_w)
          
        else:
            if axis == 'x':
                t.fd(d=extra_sup_dist)
            else:
                t.bk(d=extra_sup_dist)
            add_support(axis, slot_w, support_w)
   
    t.select_all()
    bpy.ops.tinycad.intersectall()
    bpy.context.tool_settings.mesh_select_mode = (True, False, False)
    t.select_all()
    bpy.ops.mesh.remove_doubles(threshold=0.0100)
    '''

    

        
'''
def add_support(axis, slot_w, support_w):

    if (axis == 'x'):
        # draw support
        t.ri(d=0.01)
        t.add_vert()
        t.pd()
        t.lf(d=slot_w + 0.02)
        t.pu()
        t.fd(d=support_w)
        t.pd()
        t.add_vert()
        t.ri(d=slot_w + 0.02)
        t.pu()
    else:
        t.ri(d=0.05)
        t.add_vert()
        t.pd()
        t.lf(d=slot_w + 0.1)
        t.pu()
        t.bk(d=support_w)
        t.pd()
        t.add_vert()
        t.ri(d=slot_w + 0.1)
        t.pu() 
'''

def clean_extra_supports(num_supports, axis, support_w, slot_w):
    for i in range(num_supports):
        if i == 0:
            t.fd(d=extra_sup_dist / 2)
            clean_support(axis, slot_w, support_w)
            
        else:
            t.fd(d=extra_sup_dist)
            clean_support(axis, slot_w, support_w)
            


def clean_support(axis, slot_w, support_w):
    if(axis == 'x'):
        t.select_at_cursor()
        t.fd(d=support_w)
        t.select_at_cursor()        
        bpy.ops.mesh.delete(type='EDGE')
        t.deselect_all()
        t.lf(d=slot_w)
        t.select_at_cursor()
        t.bk(d=support_w)
        t.select_at_cursor()    
        bpy.ops.mesh.delete(type='EDGE')
        t.ri(d=slot_w)
        t.fd(d=support_w)
    else:
        t.select_at_cursor()
        t.fd(d=support_w)
        t.select_at_cursor()        
        bpy.ops.mesh.delete(type='EDGE')
        t.deselect_all()
        t.ri(d=slot_w)
        t.select_at_cursor()
        t.bk(d=support_w)
        t.select_at_cursor()
        bpy.ops.mesh.delete(type='EDGE')
        t.lf(d=slot_w)
        t.fd(d=support_w)
    
    
def fill_extra_supports(num_supports, axis, support_w, slot_w):
    for i in range(num_supports):
        if i == 0:
            t.fd(d=extra_sup_dist / 2)
        else:
            t.fd(d=extra_sup_dist + (extra_sup_dist / 2))
        
        if(axis == 'x'):
            t.select_at_cursor()
            t.fd(d=support_w)
            t.select_at_cursor()
            t.lf(d=slot_w)
            t.select_at_cursor()
            t.bk(d=support_w)
            t.select_at_cursor()
            t.ri(d=slot_w)
            t.fd(d=support_w)
            bpy.ops.mesh.edge_face_add()
            t.deselect_all()
            
        else:
            t.select_at_cursor()
            t.fd(d=support_w)
            t.select_at_cursor()        
            t.ri(d=slot_w)
            t.select_at_cursor()
            t.bk(d=support_w)
            t.select_at_cursor()
            t.lf(d=slot_w)
            t.fd(d=support_w)
            bpy.ops.mesh.edge_face_add()
            t.deselect_all()


bpy.context.scene.cursor.location = (0.5, 0.8, 0)
'''
make_floor(dimensions=(25.4, 25.4, 7))
t.lf(d=100)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(25.4, 50.8, 7))
t.lf(d=100)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(50.8, 25.4, 7))
t.lf(d=100)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(76.2, 25.4, 7))
t.lf(d=100)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(25.4, 76.2, 7))
t.lf(d=100)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(101.6, 25.4, 7))
t.lf(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(25.4, 101.6, 7))
t.lf(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
'''
make_floor(dimensions=(25.4, 152.4, 7))
t.lf(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(152.4, 400, 7))
#t.lf(d=125)
#bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
'''
make_floor(dimensions=(50.8, 101.6, 7))
t.bk(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(101.6, 50.8, 7))
t.ri(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(101.6, 101.6, 7))
t.ri(d=125)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(205, 25.4, 7))
t.ri(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(25.4, 205, 7))
t.ri(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(50.8, 205, 7))
t.bk(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(205, 50.8, 7))
t.lf(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(205, 101.6, 7))
t.lf(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(101.6, 205, 7))
t.lf(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

make_floor(dimensions=(205, 205, 7))
t.lf(d=225)
bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

'''