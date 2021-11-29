# DrawingFileService

The `DrawingFileService` class is a service class for all the functions that you might want to do with any drawing file, you can find the official documentation on this class [here](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_BaseElements.html#DrawingFileService), where it is quite well documented. Several use cases of this class are covered in the examples provided by Allplan (most of them are in the interactor examples DrawingFileDataInteractor, ExportImportInteractor, ...).

If you plan on loading on unloading any drawing files, make sure that in the end you leave at least one drawing file active or even better restore the state that was present before any modifications to the drawing file states. It is a bit tideous to do it by hand, hence I made a small context manager class [DrawingFileContext](../Library/DrawingFileContext.py). You can find the [documentation](../Library/DrawingFileContext.md) in the same folder.

Some of the functions are called on an instance, while some other are called on the class. In the documentation you can see if a function is called on the class or instance by checking the type of the first argument. If the type of the first argument is DrawingFileService, the function in called on an instance of the class, and vice versa.


## Loading and unloading drawing files

As already noted above, if you plan on loading and unloading drawing files, make sure that when execution of your program is finished that at least one drawing file is loaded. For that you can use the [DrawingFileContext](../Library/DrawingFileContext.py) class.

### `LoadFile(self: DrawingFileService, doc: DocumentAdapter, file_index: int, load_state: DrawingFileLoadState) -> None`
Load drawing file `index` and set the state to the `DrawingFileLoadState`. The `DrawingFileLoadState` is an enum from the same class and you can choose from 3 different values:
- `ActiveBackground` 
- `ActiveForeground` 
- `PassiveBackground` 

Within the class there is also a map `values` that maps the integers 1, 2 and 3 to the load states. Which is usefull as the `GetFileState()` function returns the state of the drawing files as a number (1, 2, or 3) and not as an enum.

### `UnloadFile(self: DrawingFileService, doc: DocumentAdapter, file_index: int) -> None`
Unloads the drawing file with index `file_index`.
### `UnloadAll(self: DrawingFileService, doc: DocumentAdapter) -> None`
Unloads all drawing files.


## `ExportDWG(self: DrawingFileService, doc: DocumentAdapter, path: str, config: str, version: float) -> None`

Using this function you can export the contents of the current active drawing file to a file using the AutoCAD DWG format. A example usage of this function can be found in the ExportImportInteractor example. 

If you want to export a drawing file that is currently not active, then you have to first load that drawing file, and then call the function. 

```
config = os.path.join(AllplanSettings.AllplanPaths.GetUsrPath(), "nx_AllFT_AutoCad.cfg")
index = ...

dfs.LoadFile(doc, index, AllplanBaseElements.DrawingFileLoadState.ActiveForeground)
dfs.ExportDWG(doc, f"drawing_file_{index}.dwg", config, 2018) -> None
```

Arguments:
- `doc: document adapter`
- `fileName: file name string`
- `configFileName: path to the config file`
- `version: DWG version`

There are 2 problems with the function worth mentioning. The first problem is the path of the config file, which can be set to `os.path.join(AllplanSettings.AllplanPaths.GetUsrPath(), "nx_AllFT_AutoCad.cfg")`.

Althought in the example no `version` is given, when I tried doing that, Allplan decided to crash, hence I had to provide the `version`. After some googling and testing, i found the version numbers for nine different DWG versions:
- `12` -> `AC1009, AutoCAD Release 11, AutoCAD Release 12`
- `13` -> `AC1012, AutoCAD Release 13`
- `14` -> `AC1014, AutoCAD Release 14`
- `2000` -> `AC1015, AutoCAD 2000, AutoCAD 2000i, AutoCAD 2002`
- `2004` -> `AC1018, AutoCAD 2004, AutoCAD 2005, AutoCAD 2006`
- `2007` -> `AC1021, AutoCAD 2007, AutoCAD 2008, AutoCAD 2009`
- `2010` -> `AC1024, AutoCAD 2010, AutoCAD 2011, AutoCAD 2012`
- `2013` -> `AC1027, AutoCAD 2013, AutoCAD 2014, AutoCAD 2015, AutoCAD 2016, AutoCAD 2017`
- `2018` -> `AC1032, AutoCAD 2018, AutoCAD 2019, AutoCAD 2020, AutoCAD 2021, AutoCAD 2022`

, where the higher numbers mean newer versions. The newest DWG version is hence 2018 and the one that you should most probably use.

For any further questions check out the `BatchExport` project.

## `ExportIFC(self: DrawingFileService, doc: DocumentAdapter, file_index: List[int], version: IFC_Version, file_name: str) -> None`

Using this function you can export the contents of several different drawing files to a [IFC file](https://en.wikipedia.org/wiki/Industry_Foundation_Classes), it is easier to use than the ExportDWG function, as you dont need any config file nor a mysterious non-documented floating point number for the version.

Arguments:
- `doc: document adapter`
- `file_index: list of indexes of all the drawing files you want to export`
- `version: the version of the IFC format you want to use, it is an enum in the IFC_Version class`
- `file_name: path of the exported file`

There are 4 versions of IFC available for export (`Ifc_2x3`, `Ifc_4`, `Ifc_XML_2x3`, `Ifc_XML_4`), 2 of them are normal IFC files (`*.ifc` extension), while the other 2 are XML version of IFC files (`*.ifcXML` extension). 

```
file_index = [10, 11, 12]
version = AllplanBaseElements.IFC_Version.Ifc_4
file_name = "./three_drawing_files.ifc"
dfs.ExportIFC(doc, file_index, version, file_name)
```

For any further questions check out the `BatchExport` project, there both IFC and DWG files are exported.
