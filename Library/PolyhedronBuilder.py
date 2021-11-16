import NemAll_Python_Geometry as AllplanGeo
from typing import Tuple, Dict, List

class PolyhedronError(Exception):
    """
    Error class for PolyhedronBuilder
    """

    def __init__(self, message: str, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class PolyhedronBuilder:
    """
    Wrapper class for building custom polyhedra. 
    The vertices and edges are represented by strings and saved in dictionaries where they can be looked by their name.


    Note:
        This builder was tested on smaller objects
        It might have problem with large amounts of edges and vertices due to the string dictionary lookup

    Hints:
        1) 
        If the number of vertices, edges and faces of a polyhedron is static, 
        create the polyhedron normally, and then check the number of each of the 
        elements by calling get_specs(), and then hard-code the number of elements

        2)
        If the number of parts of the polyhedron is larger than one, and you need it to be one part (to be a volume)
        Print out the parts of the polyhedron by calling builder.polyhedron.GetParts() and check which faces are in seperate parts.
        When you identify which faces are seperate, when creating that face, instead of calling builder.create_face(edge_list) call
        the builder.create_face_inverted(edge_list) function
    
    Usage example:
        # Create a simple tetrahedron
        builder = PolyhedronBuilder()

        # Add vertices
        builder.add_vertex("b1", 0, 0, 0)
        builder.add_vertex("b2", 0, 100, 0)
        builder.add_vertex("b3", 100, 50, 0)
        builder.add_vertex("top", 50, 50, 50)

        # Add edges
        builder.add_edge("e1", "b1", "b2")
        builder.add_edge("e2", "b2", "b3")
        builder.add_edge("e3", "b3", "b1")
        builder.add_edge("e4", "b1", "top")
        builder.add_edge("e5", "b2", "top")
        builder.add_edge("e6", "b3", "top")

        # Create faces
        builder.create_face(["e1", "e5", "e4"])
        builder.create_face(["e2", "e6", "e5"])
        builder.create_face(["e3", "e4", "e6"])
        # Has to be inverted so the model is one part
        builder.create_face_inverted(["e1", "e2", "e3"])

        # Creation
        polyhedron = builder.create()
        mod_ele = AllplanBasisElements.ModelElement3D(com_prop, polyhedron)

        Another (a bit more complicated) example can be found in the Lichtschacht PythonPart
    """


    def __init__(self, p_type:AllplanGeo.PolyhedronType=AllplanGeo.PolyhedronType.tVolume, vertices: int=0, edges: int=0, faces: int=0):
        """
        Constructor for the PolyhedronBuilder class
        The vertices, edges and faces arguments are not necessary, but useful for preallocation 
        You can check the number of total vertices, edges and faces by calling the get_specs() function on a finished polyhedron

        Parameters:
            p_type: AllplanGeo.PolyhedronType   Type of polyhedron being created, default = tVolume
            verices, edges, faces: int          Number of expected vertices, edges and vertices
        """
        # Create Allplan polyhedron and builder encapsulated by this class
        self.polyhedron = AllplanGeo.Polyhedron3D(p_type, vertices, edges, faces, False)
        self.builder = AllplanGeo.Polyhedron3DBuilder(self.polyhedron)
        
        # Vertices and the counter for debugging purposes
        self.vertices: Dict[str, int] = {}
        self.vertex_count: int        = 0

        # Edges and edge index
        self.edges: Dict[str, Tuple[int, AllplanGeo.GeometryEdge]]  = {}
        self.index: int = 0

        # Total face counter
        self.face_count = 0

    def add_vertex(self, name: str, x: float, y: float, z: float) -> int:
        """
        Adds vertex with coordinates (x, y, z) to the polyhedron.
        Adds vertex index to the vertices dictionary under the given name

        Parameters:
            name: str           Name under which the vertex is going to be added to the dictionary
            x, y, z: float      Coordinates of the vertex
        Throws:
            PolyhedronError:    The AppendVertex function returns error
            PolyhedronError:    Vertex with the same name already exists and was overwritten
        Returns:
            Index of the created vertex
        """
        err, index = self.builder.AppendVertex(AllplanGeo.Point3D(x, y, z))
        if err != AllplanGeo.eGeometryErrorCode.eOK:
            raise PolyhedronError("Error adding vertex to the builder!", err)
        self.vertices[name] = index

        # Check if vertex has been added under the same name
        if len(self.vertices) == self.vertex_count:
            raise PolyhedronError(f"Vertex with name '{name}' already exists and was overwritten!")
        self.vertex_count += 1
        
        return index

    def add_edge(self, name: str, v1: str, v2: str) -> Tuple[int, AllplanGeo.GeometryEdge]:
        """
        Adds edge specified by vertices v1 and v2 to the polyhedron
        Adds edge index and edge to the edges dictionary under given name
        Using names for v1 and v2 is preffered because of code readability

        Parameters:
            name: str           Name under which the edge is going to be added to the dictionary
            v1, v2: str         Name of the vertices that specify the start and end of the edge
        Throws:
            PolyhedronError:    The AppendEdge function returns error
            PolyhedronError:    Edge with the same name already exists and was overwritten
            ValueError:         v1 or v2 is not in the dictionary vertices dictionary
        Returns:
            Tuple of the created edge index and created edge object
        """
        edge = AllplanGeo.GeometryEdge(self.vertices[v1], self.vertices[v2])
        err = self.polyhedron.AppendEdge(edge)
        if err != AllplanGeo.eGeometryErrorCode.eOK:
            raise PolyhedronError(f"Edge from '{v1}' to '{v2}' can't be added to the polyhedron!", err)
        self.edges[name] = (self.index, edge)

        # Check if edge has been added under the same name
        if len(self.edges) == self.index:
            raise PolyhedronError(f"Edge with name '{name}' already exists and was overwritten!")
        self.index += 1

        return (self.index - 1, edge)

    def create_face(self, edge_list: List[str], invert_start: bool=False) -> AllplanGeo.PolyhedronFace:
        """
        Creates face specified by the given edges
        The input is a list of edges that have to be in the same plane and form a closed loop
        The orientation of the edges is adjusted by the function and does not have to be considered
            
            v2        In this example the vertices are v0, v1, v2 and the edges e0, e1, e2
            /\        e0 connects v0 and v1 and so on
        e2 /  \ e1    If we want to create a face, the order of the edges matters,
          /    \      [e0, e1, e2] is valid
         /______\     If we want to pass it in the reverse order [e0, e2, e1] 
        v0  e0   v1   we need to reverse the first edge by setting the invert_start flag to True
        
        Parameters:
            edge_list: List[str]    List of edges that will form the new face
            invert_start: bool      Shoud the direction of the first face be inverted
        Throws:
            PolyhedronError:    The AppendEdge function returns error
            ValueError:         v1 or v2 is not in the dictionary vertices dictionary
        Returns:
            Tuple of the created edge index and created edge object
        """
        # Created face
        face = self.polyhedron.CreateFace(len(edge_list))
    

        previous_name = edge_list[0]
        index, edge = self.edges[previous_name]

        # Next vertex is the one on which the next edge will connect, while the end vertex is the one where the loop will be closed
        if invert_start:
            end_vertex  = edge.GetEndIndex()
            next_vertex = edge.GetStartIndex()
        else:
            end_vertex  = edge.GetStartIndex()
            next_vertex = edge.GetEndIndex()

        # not invert_start because in the OrientedEdge the flag is for positive/negative direction
        # where positive means from start to end vertex and so on
        face.AppendEdge(AllplanGeo.OrientedEdge(index, not invert_start))


        for name in edge_list[1:]:
            # Fetch index and edge
            index, edge = self.edges[name]
            
            # If else because of possible error
            if edge.GetStartIndex() == next_vertex:
                # Positive direction
                face.AppendEdge(AllplanGeo.OrientedEdge(index, True))
                next_vertex = edge.GetEndIndex()
            elif edge.GetEndIndex() == next_vertex:
                # Negative direction
                face.AppendEdge(AllplanGeo.OrientedEdge(index, False))
                next_vertex = edge.GetStartIndex()
            else:
                # The current edge cannot connect to the previous vertex
                vals = list(self.vertices.values())
                keys = list(self.vertices.keys())
                vartex_name = keys[vals.index(next_vertex)]
                raise PolyhedronError(f"The edge {name} cannot connect to the connecting vertex {vartex_name} that is on the edge {previous_name}!")
            previous_name = name

        # Check if the the edges formed a loop by comparing the first and last vertex of the loop
        if next_vertex != end_vertex:
            first_edge = edge_list[0]
            last_edge  = edge_list[-1]
            vals = list(self.vertices.values())
            keys = list(self.vertices.keys())
            first_vertex = keys[vals.index(end_vertex)]
            last_vertex  = keys[vals.index(next_vertex)]                
            raise PolyhedronError(f"First ({first_edge}) and last edge ({last_edge}) did not connect, the loop started with {first_vertex} and ended with {last_verex}!")

        self.face_count += 1
        return face
       
    def create_face_inverted(self, edge_list: List[str]) -> AllplanGeo.PolyhedronFace:
        inverted = edge_list[::-1]
        inverted.insert(0, inverted.pop())
        return self.create_face(inverted, True)

    def create(self) -> AllplanGeo.Polyhedron3D:
        """
        Creates polyhedron and checks for validity.
        
        Throws:
            PolyhedronError: The defined polyhedron is not valid
        Returns:
            Created polyhedron
        """
        self.builder.Complete()
        if not self.polyhedron.IsValid():
            raise PolyhedronError("Polyhedron not valid!")
        return self.polyhedron

    def get_specs(self) -> Tuple[int, int, int]:
        """
        Get number of vertices, indexes and faces of the polyhedron
        
        Returns:
            Tuple with count of verteces, edges and faces
        """
        return self.vertex_count, self.index, self.face_count