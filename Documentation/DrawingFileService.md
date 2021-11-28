# DrawingFileService

The `DrawingFileService` class is a service class for all the functions that you might want to do with any drawing file, you can find the official documentation on this class [here](https://pythonparts.allplan.com/2021-1/2021-1/NemAll_Python_BaseElements.html#DrawingFileService), where it is quite well documented. Several use cases of this class are covered in the examples provided by Allplan (most of them are in the interactor examples DrawingFileDataInteractor, ExportImportInteractor, ...).

Some of the functions are called on an instance, while some other are called on the class. In the documentation you can see if a function is called on the class or instance by checking the type of the first argument. If the type of the first argument is DrawingFileService, the function in called on an instance of the class, and vice versa.

## `ExportDWG(DrawingFileService, DocumentAdapter, str, str, float) -> None`

Using this function you can export the contents of the current active drawing file to a file using the AutoCAD DWG format. A example usage of this function can be found in the ExportImportInteractor example.

Arguments:
- `DocumentAdapter: document adapter`
- `fileName: file name string`
- `configFileName: path to the config file`
- `version: DWG version`

There are 2 problems with the function worth mentioning. The first problem is the path of the config file, which can be set to `os.path.join(AllplanSettings.AllplanPaths.GetUsrPath(), "nx_AllFT_AutoCad.cfg")`.

Althought in the example no `version` is given, when I tried doing that, Allplan decided to crash, hence I had to provide the `version`. After some googling and testing, i found the version numbers for nine different DWG versions:
- `12 -> AC1009, AutoCAD Release 11, AutoCAD Release 12`
- `13 -> AC1012, AutoCAD Release 13`
- `14 -> AC1014, AutoCAD Release 14`
- `2000 -> AC1015, AutoCAD 2000, AutoCAD 2000i, AutoCAD 2002`
- `2004 -> AC1018, AutoCAD 2004, AutoCAD 2005, AutoCAD 2006`
- `2007 -> AC1021, AutoCAD 2007, AutoCAD 2008, AutoCAD 2009`
- `2010 -> AC1024, AutoCAD 2010, AutoCAD 2011, AutoCAD 2012`
- `2013 -> AC1027, AutoCAD 2013, AutoCAD 2014, AutoCAD 2015, AutoCAD 2016, AutoCAD 2017`
- `2018 -> AC1032, AutoCAD 2018, AutoCAD 2019, AutoCAD 2020, AutoCAD 2021, AutoCAD 2022`

, where the higher numbers mean newer versions. The newest DWG version is hence 2018.