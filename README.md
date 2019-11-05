# blended_turtle
An implementation of turtle graphics in blender

# Why?
I'm a long term blender dabbler and occasional hobbyist coder but have never combined the two. I'm working on a project that will involve a lot of procedural generation and so will be implementing something similar to a computer generated architecture add-on over the next few months. Blended turtle is the first step towards this and also a simple (2) weekend project to get me used to the Blender API and teach myself Python as I usually work in C++. I therefore apologise for the code quality!


For more information about turtle graphics and to play around with a traditional 2D Turtle implementation see http://www.logointerpreter.com/logo-reference/

# Installation
Download the latest release and install it in the usual way by going to Edit > Preferences > Add-ons > Install and then activate it


# Basic Usage
You can use blended turtle either from the blender console or call it from your own scripts or addons. It implements most of the ordinary Logo turtle draw commands, albeit in a less elegant python fashion, and extends them into 3D. The 3D cursor is used as the "Turtle" and an ordinary mesh object is created as the turtle draws edges and faces. If the turtle's "pen" is down any vertices that are currently selected will be extruded in the direction of movement of the turtle. When the "pen" is up the turtle can move freely without effecting the mesh.


When you add a new turtle object a single vert is added at the object's origin and by extruding this vert and creating closed paths you can create arbitrary shaped meshes.


There are several helper functions provided to allow you to select and deselct portions of the mesh as it is created and also to assign and unassign vertices to vertex groups.


First switch to the "Scripting" workspace by clicking on the "Scripting" tab in the toolbar.


To add a new Turtle mesh object go to Add > Mesh > Add Turtle in Object Mode in the 3D view or enter `bpy.ops.turtle.add_turtle()` into the command console. 


You can also turn an existing mesh into a Turtle by selecting a mesh, going into edit mode, moving the 3D cursor to the location of a vertex (Select a vertex > Shift + s > Cursor to selected) and running any turtle draw command from the console. This will add a 'pendownp' property to the object which stores the "pen state" of the turtle i.e. whether to draw an edge when the turtle moves.


Once you've added a turtle object or moved the cursor to a vertice in an existing object and are in 'Edit' mode you can use any of the following commands to move the turtle. For most drawing commands, if the pen is down an edge will be drawn from the turtle's starting location to its ending location. If the pen is up the turtle will move to the ending location without drawing anything,


# Commands
The syntax is a bit different to Logo as each command is implemented as a seperate blender operator. This means that arguments have to be passed as named arguments e.g. to move the turtle forward by 10 units you type `bpy.ops.turtle.fd(d=10)` or `bpy.ops.turtle.forward(d=10)` into the command console. Since the aim of the addon is to be able to work quickly in the 3D view from the command console as well as produce more complex procedural scripts that are easy to reason about, both the short form and long form of the turtle commands can be used. I suggest you start by declaring bpy.ops.turtle as a a shorter variable such as t (enter `t=bpy.ops.turtle` into the command console) so you can enter `t.fd(d=10)` rather than `bpy.ops.turtle.fd(d=10)`


It can also be useful to access the Turtle's location and rotation. There are two methods built into blender that allow you to do this easily: `bpy.context.scene.cursor.location` and `bpy.context.scene.cursor.rotation_euler`


`bpy.context.scene.cursor.rotation_euler` returns co-ordinates in radians rather than degrees, while the blended turtle commands all take degrees for their arguments, so you'll need to convert between the two.

## Draw

```python
bpy.ops.turtle.fd(d=0)
bpy.ops.turtle.forward(d=0)
```
Moves the turtle forward along the positive 'Y' axis by d units

```python
bpy.ops.turtle.bk(d=0)
bpy.ops.turtle.backward(d=0)
```
Moves the turtle backward along the negative 'Y' axis by d units

```python
bpy.ops.turtle.lf(d=0)
bpy.ops.turtle.left(d=0)
```
Moves the turtle left along the negative 'X' axis by d units

```python
bpy.ops.turtle.ri(d=0)
bpy.ops.turtle.right(d=0)
```
Moves the turtle right along the positive 'X' axis by d units

```python
bpy.ops.turtle.up(d=0)
```
Moves the turtle up along the positive 'Z' axis by d units

```python
bpy.ops.turtle.dn(d=0)
bpy.ops.turtle.down(d=0)
```
Moves the turtle down along the negative 'Z' axis by d units
   
```python
bpy.ops.turtle.setp(v=(0, 0, 0))
bpy.ops.turtle.set_position(v=(0, 0, 0))
```
Moves the turtle to the specified position in world space

```python    
bpy.ops.turtle.lt(d=0)
bpy.ops.turtle.left_turn(d=0)
```
Rotates the turtle around the 'Z' axis by negative d degress

```python   
bpy.ops.turtle.rt(d=0)
bpy.ops.turtle.right_turn(d=0)
```
Rotates the turtle around the 'Z' axis by positive d degress
   
```python
bpy.ops.turtle.lu(d=0)
bpy.ops.turtle.look_up(d=0)
```
Rotates the turtle around the 'X' axis by positive d degrees (look up)
   
```python
bpy.ops.turtle.ld(d=0)
bpy.ops.turtle.look_down(d=0)
```
Rotates the turtle around the 'X' axis by negative d degrees (look down)

```python   
bpy.ops.turtle.rl(d=0)
bpy.ops.turtle.roll_left(d=0)
```
Rotates the turtle around the 'Y' axis by negative d degrees (roll left)
   
```python
bpy.ops.turtle.rr(d=0)
bpy.ops.turtle.roll_right(d=0)
```
Rotates the turtle around the 'Y' axis by positive d degrees (roll right)

```python   
bpy.ops.turtle.setrot(v=(0, 0, 0)
bpy.ops.turtle.setrotation(v=(0, 0, 0)
```
Set the turtles rotation. v = world rotation in degrees (0, 0, 0)

```python   
bpy.ops.turtle.seth(d=0)
bpy.ops.turtle.set_heading(d=0)
```
rotate the turtle to face the specified horizontal heading around the 'Z' axis

```python   
bpy.ops.turtle.set_pitch(d=0)
```
rotate the turtle to face the specified vertical heading around the 'X' axis
   
```python
bpy.ops.turtle.setr(d=0)
bpy.ops.turtle.set_roll(d=0)
```
rotate the turtle to face the specified roll around the 'Y' axis

```python   
bpy.ops.turtle.qc(cp=(0, 0, 0), ep=(0, 0, 0)) 
bpy.ops.turtle.quadratic_curve(cp=(0, 0, 0), ep=(0, 0, 0)) 
```
Moves the turtle along a path described by a quadratic Bezier curve. 

Keyword arguments:

   cp = coordinates of control point

   ep = coordinates of end point

```python
bpy.ops.turtle.cc(cp1=(0, 0, 0), cp2=(0, 0, 0), ep=(0, 0, 0)
bpy.ops.turtle.cubic_curve(cp1=(0, 0, 0), cp2=(0, 0, 0), ep=(0, 0, 0)
```
Moves the turtle along a path described by a cubic Bezier curve. 
  
Keyword arguments:

cp1 = coordinates of 1st control point
   
cp2 = coordinates of 2nd control point

ep = coordinates of end point

## Path (Draw faces and closed polys)

Blended Turtle uses the Logo path commands to draw closed polygons and filled faces. To draw a polygon you first need to enter the "begin path" `bpy.ops.turtle.begin_path()` command. This stores the index of the current vertex. After this you should move the turtle as usual. Once you have drawn your polygon you can then run either the "stroke path" `bpy.ops.turtle.stroke_path()`or the "fill path" `bpy.ops.turtle.fill_path()` command.

```python
bpy.ops.turtle.begin_path()
```
Begin a path from the currently selected vertex

```python    
bpy.ops.turtle.stroke_path()
```
Draws an edge between selected vert and vert indexed by begin path command

```python   
bpy.ops.turtle.fill_path()
```
Draws an edge between selected vert and vert indexed by begin path command and then creates a face between all vertices created since the last beginpath statement
   
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
   
## Selection commands
    bpy.ops.turtle.sa()
   Selects all vertices

    bpy.ops.turtle.da()
   Deselects all vertices

```python   
bpy.ops.turtle.select_path() 
```
Selects all verts drawn since last Begin Path command
