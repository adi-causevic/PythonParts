# Getting started

## Create your PythonPart

The functionality of a PythonPart is split in at least 2 different files. The first file is the `<python_part>.pyp` file that describes the Allplan palette part of the PythonPart (basically the UI for interacting with the code). The second file is the `<python_part>.py` file that contains all the logic of the python part. 

Along those 2 files there are several other optional files:
- `<python_part>.png` - Icon of the python part
- `<python_part>_<lang>.xml` - Stringtable for different languages
- `<python_part>.pal` - Pallette file for the python part

All of these files have to be put in the same directory as the `<python_part>.pyp` file. The png and pallete have to have the same name as the `<python_part>.pyp` file, while the stringtable file has to start with the same name, followed by the abbrevation for language it is made for.

### `<python_part>.pyp`

The `*.pyp` file contains all the information of how the python part should be executed as well as the UI for the PythonPart. The file is written in XML format and the simplest `*.pyp` file would look like this:

```
<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>path\to\python\file.py</Name>
        <Title>My PythonPart</Title>
        <Version>1.0</Version>
        <ReadLastInput>True</ReadLastInput>
        <Interactor>False</Interactor>
    </Script>
    <Page>
        <Name>Page1</Name>
        <Text>Page 1</Text>

        <Parameter>
            <Name>Length</Name>
            <Text>Hello</Text>
            <Value>World</Value>
            <ValueType>Text</ValueType>
        </Parameter>
    </Page>
<Element>
```

#### XML Declaration
The file starts with the XML declaration line where you declare the encoding. But for what it is worth `utf-8` will be more than enough for most uses (I don't know a reason to use something else).

#### `<Script>`

After the XML declaration comes an element with the `Element` tag that has to contain a child element with the `Script` tag. The `Script` element has to contain a `Name` and `Title` element, whereas the `Version`,  `Interactor` and `<ReadLastInput>` elements are optional.

- `<Name>` - contains the path to the python script that holds the logic of the python part, the path is relative to the `PythonPartsScripts` folder that is described in the `<python_script>.py` file.
- `<Title>` - contains the name of the PythonPart that is displayed in the bar in Allplan
- `<Version>` - contains the current version of the PythonPart (Not sure if it has any real function)
- `<Interactor>` - if the PythonPart is supposed to have an interactor, this has to be set to `True` otherwise it can be ignored as the default value is `False`
- `<ReadLastInput>` - if you want the PythonPart to use the values of the input field that were used the last time the PythonPart was run, set the value of this element to `True`, otherwise you can ignore it as the default value is `False`.

#### `<Page>`

After the defined `<Script>` element, you can define the UI of the PythonPart using one or more `<Page>` elements. Each `<Page>` element has to contain 2 different elements:

- `<Name>` - within this element you define the name of the page which serves like the ID for the page
- `<Text>` - This contains the title of the page that will be displayed in Allplan if there are more than 1 pages, in the case there is only one page, the name will not be desplayed

You can populate the page with different input fields, buttons, etc., that you might need for the working of your script. More about this can be found in [official Allplan documentation](https://pythonparts.allplan.com/2021-1/How_to_define_the_PythonPart_pyp_file.htm), or in case we made a `How to define a *.pyp file` documentation.

## Examples

Although the official documentation is not quite the best, the framework comes with an extensive collection of examples that are probably the most useful learning tool. The examples are 

C:\ProgramData\Nemetschek\Allplan\2021\Etc\Examples\PythonParts

