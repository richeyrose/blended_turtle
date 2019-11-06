import bpy
turtle = bpy.context.scene.cursor
t = bpy.ops.turtle


#x = 25.4
x = 101.6
#y = 25.4
y = 101.6
z = 7

t.add_turtle()

#draw outer bit of tile bottom
t.begin_path()
t.forward(d=y)
t.right(d=x)
t.backward(d=y)
t.stroke_path()
t.select_path()

#move to inner bit
t.pen_up()
t.forward(d = 6 )
t.left(d=6 + 2.12)

#draw inner bit
t.pen_down()
t.add_vert()
t.rt(d=45)
t.fd(d=3)
t.lt(d=45)

#make sure we add reinforcements if 6" tile
for i in range(4):
    if i % 2 == 0:
        axis = y
    else:
        axis = x

    if axis >= 101.6:
        center = axis/2 - 8.12
        t.fd(d=center - 13.84)
        t.fd(d=3)
        t.fd(d=21.67)
        t.fd(d=3)
        t.fd(d=center - 13.84)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
    else:
        t.fd(d=axis-8.12*2)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
                
t.select_all()
t.merge()
t.bridge()
t.deselect_all()
t.pen_up()

for i in range(4):
    if i % 2 == 0:
        axis = y
    else:
        axis = x
    if axis >= 101.6:
        center = axis/2 - 8.12
        t.fd(d=center - 13.84)
        
        #extrude additional supports 1 in towards center
        t.select_at_cursor(additive=True)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.lf(d=4.7)
        t.pen_up()
        t.deselect_all()
        
        #extrude additional supports up
        t.select_at_cursor(additive=True)
        t.ri(d=4.7)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.up(d=1.39)
        t.bk(d=3)
        t.dn(d=1.39)
        t.deselect_all()
        t.pen_up()
        t.fd(d=3)
        
        #extrude additional supports 2 in towards center
        t.fd(d=21.67)
        t.select_at_cursor(additive=True)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.lf(d=4.7)
        t.pen_up()
        t.deselect_all()
        
        
        #extrude additional supports up
        t.select_at_cursor(additive=True)
        t.ri(d=4.7)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.up(d=1.39)
        t.bk(d=3)
        t.dn(d=1.39)
        t.deselect_all()
        t.pen_up()
        t.fd(d=3)
        
        t.fd(d=center - 13.84)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
    else:
        t.fd(d=axis-8.12*2)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
            
t.rt(d=45)
t.bk(d=3)

# extrude corner supports in towards center
for i in range(4):
    t.select_at_cursor(buffer=0.1, additive=True)
    t.fd(d=3)
    t.select_at_cursor(buffer=0.1, additive=True)
    t.pd()
    t.lf(d=6.45)
    t.deselect_all()
    t.pu()
    t.ri(d=6.45)
    t.lt(d=45)
    if i % 2 == 0:
        t.fd(d = y - ((6 + 2.12)*2))
    else:
        t.fd(d = x - ((6 + 2.12)*2))
    t.lt(d=45)
    

t.select_all()
t.merge()
t.deselect_all()

# select central area and create a face
t.set_rotation(v=(0, 0, 0))

t.lf(d = x - ((6 + 2.12)*2) -2)
t.fd(d=1)
t.select_by_location(
        lbound = turtle.location, 
        ubound = (turtle.location[0] + x - ((6 + 2.12)*2) -1, 
        turtle.location[1] + y - ((6 + 2.12)*2) -1, 
        turtle.location[2]))
        
bpy.ops.mesh.edge_face_add()
t.deselect_all()
t.home()

#prepare to draw corner supports

t.ri(d=8.12)
t.fd(d=6)
t.rt(d=45)

#draw corner supports
for i in range(4):
    t.select_at_cursor(additive=True)
    t.fd(d=6.45)
    t.select_at_cursor(additive=True)
    t.pd()
    t.up(d=1.39)
    t.deselect_all()
    t.pu()
    t.lf(d=3)
    t.dn(d=1.39)
    t.select_at_cursor(additive=True)
    t.bk(d=6.45)
    t.select_at_cursor(additive=True)
    t.pd()
    t.up(d=1.39)
    t.ri(d=3)
    t.merge()
    t.deselect_all()
    t.pu()
    t.dn(d=1.39)
    t.rt(d=45)
    if (i % 2) == 0:
        t.fd(d = x - ((6 + 2.12)*2))
    else:
        t.fd(d = y - ((6 + 2.12)*2))
    t.lt(d=45)
    t.fd(d=3)
    t.lt(d=90)
    
t.select_all()   
t.merge()
t.set_rotation(v=(0, 0, 0))
t.deselect_all()

t.rt(d=90)

# inner ring 1 lower poly
for i in range(4):
    if i % 2 == 0:
        axis = x
    else:
        axis = y
    if axis >= 101.6:
        t.select_at_cursor(additive=True)
        center = axis/2 - 8.12
        t.fd(d=center - 13.84)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.up(d=1.39)
        t.deselect_all()
        t.pen_up()
        t.dn(d=1.39)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.fd(d=21.67)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.up(d=1.39)
        t.deselect_all()
        t.pen_up()
        t.dn(d=1.39)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.fd(d=center - 13.84)
        t.select_at_cursor(additive=True)
        t.pen_down()
        t.up(d=1.39)
        t.deselect_all()
        t.pen_up()
        t.dn(d=1.39)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
    else:
        t.select_at_cursor(additive=True)
        t.fd(d=axis-8.12*2)
        t.select_at_cursor(additive=True)
        t.pd()
        t.up(d=1.39)
        t.deselect_all()
        t.pu()
        t.dn(d=1.39)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
 
t.select_all()
t.merge()
t.deselect_all()
t.set_rotation(v=(0, 0, 0))
t.up(d=1.39)
t.rt(d=90)

# inner ring 1 upper poly
for i in range(4):
    if i % 2 == 0:
        axis = x
    else:
        axis = y
    if axis >= 101.6:
        t.select_at_cursor(additive=True)
        center = axis/2 - 8.12
        t.fd(d=center - 13.84)
        t.select_at_cursor(additive=True)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.fd(d=21.67)
        t.select_at_cursor(additive=True)
        t.fd(d=3)
        t.select_at_cursor(additive=True)
        t.fd(d=center - 13.84)
        t.select_at_cursor(additive=True)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)
    else:
        t.select_at_cursor(additive=True)
        t.fd(d=axis-8.12*2)
        t.select_at_cursor(additive=True)
        t.lt(d=45)
        t.fd(d=3)
        t.lt(d=45)

t.pd()
t.up(d=4.71)
t.select_all()
t.merge()
t.deselect_all()
      
'''
#inner ring 1 upper poly
for i in range(4):
    t.select_at_cursor(additive=True)
    if i % 2 == 0:
        t.fd(d = x - ((6 + 2.12)*2))
    else:
        t.fd(d = y - ((6 + 2.12)*2))
    t.select_at_cursor(additive=True)
    t.lt(d=45)
    t.fd(d=3)
    t.lt(d=45)
    
t.pd()
t.up(d=4.71)
t.deselect_all()
t.pu()
t.set_rotation(v=(0, 0, 0))
t.rt(d=45)
t.fd(d=6.45)
t.rt(d=45)
t.dn(d=6.1)

#Inner ring 2 lower poly
for i in range(4):
    t.select_at_cursor(additive=True)
    if i % 2 == 0:
        t.fd(d = x - ((12.681)*2))
    else:
        t.fd(d = y - ((12.681)*2))
    t.select_at_cursor(additive=True)
    t.pd()
    t.up(d=1.39)
    t.pu()
    t.dn(d=1.39)
    t.deselect_all()
    t.lt(d=45)
    t.fd(d=3)
    t.lt(d=45)


t.select_all()
t.merge()
t.deselect_all()
t.set_rotation(v=(0, 0, 0))

#Inner ring 2 upper poly 
t.up(d=1.39)
t.lf(d=2.2)
t.select_by_location(
    lbound=turtle.location, 
    ubound=(turtle.location[0] + x - 10.48 * 2, 
            turtle.location[1] + y - 10.48 * 2, 
            turtle.location[2]), 
            additive=True)
t.pd()
t.up(d=4.71)
t.select_all()
t.merge()
t.deselect_all()
t.pu()
t.home()
t.up(d=6.1)
t.select_by_location(
    lbound=turtle.location, 
    ubound=(turtle.location[0] + x,
            turtle.location[1] + y, 
            turtle.location[2]), 
            additive=True)

#bridge inner rings. Inside is now done
t.bridge()

t.deselect_all()
t.home()

t.select_at_cursor(additive=True)
 #Select outside
for i in range(2):
    t.fd(d=y)
    t.rt(d=90)
    t.select_at_cursor(additive=True)
    t.fd(d=x)
    t.rt(d=90)
    t.select_at_cursor(additive=True)

#extrude up
t.pd()
t.up(d=7)

#fill top face
bpy.ops.mesh.edge_face_add()

#reset turtle
t.deselect_all()
t.pu()
t.home()

# Turtle bit is done!
'''