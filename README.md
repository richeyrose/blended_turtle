# blended_turtle
An implementation of turtle graphics in blender

# Why?
I'm a long term blender dabbler and occasional hobbyist coder but have never combined the two. I'm working on a project that will involve a lot of procedural generation and so will be implementing something similar to a computer generated architecture add-on over the next few months. Blended turtle is the first step towards this and also a simple (2) weekend project to get me used to the Blender API and teach myself Python as I usually work in C++. I therefore apologise for the code quality!


For more information about turtle graphics and to play around with a traditional 2D Turtle implementation see http://www.logointerpreter.com/logo-reference/

# Installation
This addon depends on "Extra Mesh Objects" extension, install this extension by going to Edit > Preferences > Get Extensions, search and activate it.

Download the latest release and install it in the usual way by going to Edit > Preferences > Add-ons > Install and then activate it.


# Basic Usage
You can use blended turtle either from the blender console or call it from your own scripts or addons. It implements most of the ordinary Logo turtle draw commands, albeit in a less elegant python fashion, and extends them into 3D. The 3D cursor is used as the "Turtle" and an ordinary mesh object is created as the turtle draws edges and faces.


First switch to the "Scripting" workspace by clicking on the "Scripting" tab in the toolbar.


To add a new Turtle mesh object go to Add > Mesh > Add Turtle in Object Mode in the 3D view or enter bpy.ops.turtle.primitive_turtle_add() into the command console. 


You can also turn an existing mesh into a Turtle by selecting a mesh, going into edit mode, moving the 3D cursor to the location of a vertex (Select a vertex > Shift + s > Cursor to selected) and running any turtle draw command from the console. This will add a 'pendownp' property to the object which stores the "pen state" of the turtle i.e. whether to draw an edge when the turtle moves.


Once you've added a turtle object or moved the cursor to a vertice in an existing object and are in 'Edit' mode you can use any of the following commands to move the turtle. For most drawing commands, if the pen is down an edge will be drawn from the turtle's starting location to its ending location. If the pen is up the turtle will move to the ending location without drawing anything,


# Commands
The syntax is a bit different to Logo as each command is a seperate operator. This means that arguments have to be passed as named arguments e.g. to move the turtle forward by 10 units you type bpy.ops.turtle.fd(d=10) into the command console. Since the aim of the addon is to be able to quickly in the 3D view the short form of the turtle commands are used, although if I can work out how to implement aliases in Python I'll add the long form as well. I suggest you start by declaring bpy.ops.turtle as a a shorter variable such as t (enter t=bpy.ops.turtle into the command console) so you can enter t.fd(d=10) rather than bpy.ops.turtle.fd(d=10)

## Draw
    bpy.ops.turtle.fd(d=0) 
   Moves the turtle forward along the positive 'Y' axis by d units

    bpy.ops.turtle.bk(d=0)
   Moves the turtle backward along the negative 'Y' axis by d units

    bpy.ops.turtle.lf(d=0)
   Moves the turtle left along the negative 'X' axis by d units

    bpy.ops.turtle.ri(d=0)
   Moves the turtle right along the positive 'X' axis by d units

    bpy.ops.turtle.up(d=0)
   Moves the turtle up along the positive 'Z' axis by d units

    bpy.ops.turtle.dn(d=0)
   Moves the turtle down along the negative 'Z' axis by d units
   
    bpy.ops.turtle.setp(v=(0, 0, 0))
   Moves the turtle to the specified position in world space
    
    bpy.ops.turtle.lt(d=0)
   Rotates the turtle around the 'Z' axis by negative d degress
   
    bpy.ops.turtle.rt(d=0)
   Rotates the turtle around the 'Z' axis by positive d degress
   
    bpy.ops.turtle.lu(d=0)
   Rotates the turtle around the 'X' axis by positive d degrees (look up)
   
    bpy.ops.turtle.ld(d=0)
   Rotates the turtle around the 'X' axis by negative d degrees (look down)
   
    bpy.ops.turtle.rl(d=0)
   Rotates the turtle around the 'Y' axis by negative d degrees (roll left)
   
    bpy.ops.turtle.rr(d=0)
   Rotates the turtle around the 'Y' axis by positive d degrees (roll right)
   
    bpy.ops.turtle.setrot(v=(0, 0, 0)
   Set the turtles rotation. v = world rotation in degrees (0, 0, 0)
   
    bpy.ops.turtle.seth(d=0)
   rotate the turtle to face the specified horizontal heading around the 'Z' axis
   
    bpy.ops.turtle.setpitch(d=0)
   rotate the turtle to face the specified vertical heading around the 'X' axis
   
    bpy.ops.turtle.setr(d=0)
   rotate the turtle to face the specified roll around the 'Y' axis
   
    bpy.ops.turtle.qc(cp=(0, 0, 0), ep=(0, 0, 0)) 
   Moves the turtle along a path described by a quadratic Bezier curve. 

   Keyword arguments:

   cp = coordinates of control point

   ep = coordinates of end point

    bpy.ops.turtle.cc(cp1=(0, 0, 0), cp2=(0, 0, 0), ep=(0, 0, 0)
   Moves the turtle along a path descriped by a cubic Bezier curve. 
  
   Keyword arguments:

   cp1 = coordinates of 1st control point
   
   cp2 = coordinates of 2nd control point

   ep = coordinates of end point

## Path (Draw faces and closed polys and extrude into 3D)

Blended Turtle uses the Logo path commands to draw closed polygons and filled faces. To draw a polygon you first need to enter the "begin path" bpy.ops.turtle.bp() command. This stores the index of the current vertex. After this you should move the turtle as usual. Once you have drawn your polygon you can then run either the "stroke path" bpy.ops.turtle.sp()or the "fill path" bpy.ops.turtle.fp() command.

Once you have drawn your path you can extrude it into 3D using the "extrude path" bpy.ops.turtle.ep(d=0) command. This will extrude the poly along its normal by "d" blender units.

    bpy.ops.turtle.bp() 
   Begin a path from the currently selected vertex
    
    bpy.ops.turtle.sp()
   Draws an edge between selected vert and vert indexed by begin path command
   
    bpy.ops.turtle.fp()
   Draws an edge between selected vert and vert indexed by begin path command and then creates a face between all vertices created since the last beginpath statement
   
    bpy.ops.turtle.selp() 
   Selects all verts drawn since last Begin Path command
   
    bpy.ops.turtle.ex(d=0)
   Extrudes slected vertices along normal. d = distance in blender units
   
## Pen commands
Whether the pen is up or down determines whether the turtle will draw edges as it moves
    
    bpy.ops.turtle.pu() 
   Raises the pen so the turtle wil NOT draw on move
   
    bpy.ops.turtle.pd()
   Raises the pen so the turtle WILL draw on move
   
## Canvas commands
Commands for homing the turtle and clearing the canvas

    bpy.ops.turtle.home()
   Sets the turtle location and rotation to object origin
   
    bpy.ops.turtle.clean()
   Deletes the mesh while leaving the turtle where it is.
   
    bpy.ops.turtle.cs()
   Deletes the mesh and homes the turtle
   
## Other
    bpy.ops.turtle.sa()
   Selects all vertices

    bpy.ops.turtle.da()
   Deselects all vertices
