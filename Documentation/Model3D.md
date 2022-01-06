# 3D elements
*Example: __/GeometryExamples/__*

3D modelling is one of the main usecases of Allplan, and that also makes it one of the main usecases of PythonParts. There is a wide variety of possible 3D objects that can be constructed using the PythonParts API, and here we will discuss some of the objects and properties surrounding them.

If you have experience with the SmartParts tool, [here](https://pythonparts.allplan.com/2021-1/How_to_implement_SmartPart_methods_in_Allplan_Python_API.htm) you can find _translations_ from SmartPart to PythonParts functions, and [here](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html) you can find all the geometric functions offered by the PythonParts API. 

In addition to those resources, in the examples that get shipped with Allplan, there is a whole folder with many useful examples. They should serve as the main source for learning, and here only some quirks will be described.

## How to create elements

Before any 3D object can be created, it first has to be wrapped by the [ModelElement3D](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_BasisElements.html#ModelElement3D) class. 

```
    com_prop = AllplanBaseElements.CommonProperties()
    p0 = AllplanGeo.Point3D(0, 0, 0)
    p1 = AllplanGeo.Point3D(1000, 1000, 1000)
    obj = AllplanGeo.Polyhedron3D.CreateCuboid(p0, p1)
    ele = AllplanBasisElements.ModelElement3D(self.com_prop, obj)
```

The constructor for the ModelElement3D class takes two arguments. The first argument is an instance of the CommonProperties class where we can define stroke/pen/other options related to rendering of the object that is given as the second argument to the function.

Now that we have created a renderable ModelElement3D we can pass it to Allplan to render it. There are 2 different ways to pass the element to Allplan:

### create_element function
*Example: __/GeometryExamples/__*

The first way to pass a 3D element to Allplan is only possible if we are not using an interactor, than we can simply pass it as the return value of the `create_element` function. As the `create_element` function returns a tuple of 2 lists, we can return the element as a part of the first list. Note that any number of elements can be returned in that list.

```
def create_element(build_ele, doc):
    ...
    return ([ele], [])
```

### Create elements by hand
*Example: __/InteractorExamples/WallInteractor.py__*

When using an interactor, creating an element becomes a bit more difficult, namely we need to use the [CreateElements](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_BaseElements.html#-CreateElements) function found in the `BaseElements` package. The function a lot of arguments, but they are not that scary:

- Document adapter of the working document, usually named doc
- Insertion matrix for the elements (if no rotation/translation has to be done, you can simply pass AllplanGeo.Matrix3D())
- A list of model elements that you want to create
- A list of model UUIDS of elements in modification mode (If you are just creating elements, you can pass an empty list as an argument)
- Associative view reference object (No clue what this does, but None is a valid value)

```
    ...
    insertion_mat = AllplanGeo.Matrix3D()
    insertion_mat.Translate(AllplanGeo.Vector3D(100, 200, 300))
    created = AllplanBaseElements.CreateElements(doc, insertion_mat, [ele], [], None)
    ...
```

## Transformations

The 3 main transformations of 3D objects are done using the [Matrix3D](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#Matrix3D) class, and the [Transform](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-Transform) function. First we define the transformation we want using the Matrix, and then we transform the element using the function:

```
    ...
    transform_mat = AllplanGeo.Matrix3D()
    transform_mat.Scaling(0.5, 1, 2)
    transform_mat.Rotation(AllplanGeo.Line3D(1, 0, 0), AllplanGeo.Angle(math.pi/2))
    transform_mat.Translate(AllplanGeo.Vector3D(100, 200, 300))
    obj = AllplanGeo.Transform(obj, transform_mat)
    ...
```

## Breps and polyhedrons

There are 2 ways of representing 3D object in Allplan, the first one is using plain polyhedrons, while the second one is using boundary representations aka. _Brep's_. When deciding what version of a 3D object to use, it best to use to body that suits the task better, and more often than not, it is going to be breps that are the better choice as they are a superset of polygons. 

### Conversion

While converting from a polyhedron to a brep, almost no information is lost. on the other hand, when converting a brep (eg. a boundary representation of a circle or a rotational body) the smooth body has to be converted into flat faces, hence information is going to be lost. The conversions are possible using the functions
[CreateBRep3D](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-CreateBRep3D) and [CreatePolyhedron](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-CreatePolyhedron):

```
err, brep = AllplanGeo.CreateBRep3D(polyhedron)
if err != AllplanGeo.eOK:
    raise RuntimeError("Error creating BRep")

approx_settings = AllplanGeo.ApproximationSettings(AllplanGeo.ASET_BREP_TESSELATION, 0.9)

err, poly = AllplanGeo.CreatePolyhedron(brep, approx_settings)
if err != AllplanGeo.eOK:
    raise RuntimeError("Error creating polyhedron")       
```

In the [approximation settings](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#ApproximationSettings) we define how we want to approximate the BRep. In this specific example we are using tesselation, and the second parameter is floating point value in the range [0, 1] that defines how precise we want the tesselation to be (0 is more precise, 1 is rougher).

Although it might seem silly to convert between types, creating some types of 3D shapes is only possible using one or the other. Furthermore, boolean operations are only possible if both the objects are of the same type.

### Boolean operations

One of the most important parts of 3D modelling is performing boolean operations on objects. Within the [AllplanGeo](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html) package Allplan gives us a variety of functions for doing just that:

- [MakeIntersection](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-MakeIntersection)
- [MakeUnion](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-MakeUnion)
- [MakeSubtraction](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_Geometry.html#-MakeSubtraction)

These function can be done as long as the 2 objects are of the same type (eg. brep and brep). From my limited experience, working with breps is faster than with polygons, but with small objects it should not really matter too much.