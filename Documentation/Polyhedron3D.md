# Polyhedron3D

This is a PythonPart class for building custom 3D polyhedra. It is located in the NemAll_Python_Geometry (aka. AllplanGeo) 
module and the official documentation is available [here](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#Polyhedron3D).
A wrapper class for the polyhedron can be found in the [library](../Library/PolyhedronBuilder.py), which you 
can also use to see some usage details for the Polyhedron3D class.

## Create Polyhedron3D

The constructor takes 5 seperate parameters which are all optional.
Out of the 5 parameters, 3 of them describe the number of vertices, edges and faces the polyhedron is expected to have.
They are used for preallocating the needed space for the values for performance reasons.

Parameters:
- type: PolyhedronType 		Type of polyhedron to be constructed
- vertices: int		 		Number of vertices expected
- edges: int		 		Number of edges expected
- faces: int		 		Number of faces expected
- negativeOrientation:bool	Negative orientation

## Adding vertices

To add vertices to the polyhedron, you have to use the Polyhedron3DBuilder class defined in the same module.
Polyhedron3DBuilder takes one argument in the constructor, and that is the Polyhedron3D object to which you want to add vertices.

After you have created the Polyhedron3DBuilder you can use the AppendVertex() function to add a vertex to the polyhedron, 
in return the function returns a tuple that contains an error code and the index of the created vertex.

If the vertex has been added successfully, the error code returned is eOK.

## Adding edges

Adding edges id done directly on the Polyhedron3D class by calling the AppendEdge() function. The function returns an error code
which has to be eOK, if it is not then an error occurred. The function does not return the index of the edge, hence you have to keep
track of the indexes. The index of the first edge added is going to be 0, for the second edge it is going to be 1 and so on. Basically just incremental.

## Creating faces

A face is created using the CreateFace(n_edges) function that returns a PolyhedronFace object that can be used to add edges to the face.
The function takes an integer as an argument, where the integer is the expected number of edges in the face. It is not mandatory for that value to 
be correct, but it helps with optimization. 
To add an edge to the face, you simply call the AppendEdge function that takes 2 arguments. The first argument is an integer that is the index of the edge you want to add
while the second argument is a boolean which indicates if the direction of the edge is from the start to end or reverse.
 
## Finish polyhedron

After you have added all the vertices, edges and faces to the polyhedron, simply call the builder.Complete() on the Polyhedron3DBuilder you have created 
for adding edges. Afterwards you can check if the polyhedron is valid by calling the polyhedron.IsValid() function that returns a boolean indiating the validity of the polyhedron.

## Example

For an example usage of this class check out the [PolyhedronBuilder](../Library/PolyhedronBuilder.py) class.




