# Interactor
## Description
Wrapper class for the python parts interactor functions

## Setup
To use the interactor you first have to notify Allplan that your python part is going to 
use an interactor by adding an attribute to the script block in the *.pyp file:

```
<Script>
    <Name>path/to/InteractorScript.py</Name>
    <Text>Interactor PythonPart</Text>
    <Interactor>True</Interactor>
</Script>
```

Afterwards you have to create the __InteractorScript.py__ file that should contain at least 3 functions:

```
from .Interactor import Interactor

# Method for checking the supported versions
def check_allplan_version(build_ele, version):
    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True

# Method for element creation
def create_element(build_ele, doc):
    # Delete unused arguments
    del build_ele
    del doc

    # No elements are going to be created
    return [], []
    
# Method for interactor creation
def create_interactor(coord_input, pyp_path, show_pal_close_btn, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list):
    return MyInteractor(coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list)

# Interactor class
class MyInteractor(Interactor):
    def __init__(self, *args, **kwds):
        # Init interactor
        super().__init__("MyPythonPart.pyp", *args, **kwds)

```

Your interactor class has to inherit from Interactor, and first call the super `__init__` method. The first argument to the `__init__` method is the exact name of the __*.pyp__ file. If you want you can skip the __.pyp__ extension and just use the file name. After the name, forward all the arguments and keywords you got by the `create_interactor` method, as seen in the code sample.

The Interactor will take care of everything from pallete service creation to event function binding.

## Binding buttons

If you have any kind of button in your pallette, you know you have to assign an __EventId__ to the button, which will be the only argument to the `on_control_event` function when the button is clicked.
The Interactor will parse the __*.pyp__ file and find all the buttons and __EventIds__ and link them to the functions called the same as the button (the name of the button is specified in the __Name__ parameter in the button). Lets look at an example:

### Define the button:
```
        <Parameter>
            <Name>button_holder</Name>
            <Text>Click</Text>

            <ValueType>Row</ValueType>
            <Parameter>
                <Name>button_clicked</Name>
				<TextId>Me!</TextId>
                <ValueType>Button</ValueType>
				<EventId>1337</EventId>
            </Parameter>
        </Parameter>
```

### Define the function
```
# Interactor class
class MyInteractor(Interactor):
    def __init__(self, *args, **kwds):
        # Init interactor
        super().__init__("MyPythonPart.pyp", *args, **kwds)

    # ... other stuffs ...

    def button_clicked(self, build_ele, doc):
        message = "Hey you clicked a button!"
        AllplanUtil.ShowMessageBox(message, AllplanUtil.MB_OK)
```

As you see, the name of the function is the same as the name of the button, and the function has 2 arguments, the build element and the document adapter.

If your __.pyp__ file has a button that has no corresponding function in your interactor, an `InteractorError` is going to be thrown informing you about which function is not implemented. Additionally, if there are 2 buttons that have the same EventId a `InteractorError` is going to be thrown again.

## Binding value fields

If you have a value field in the pallette, every time that field changes the `modify_element_property` function is called. If you want, here you can bind a function that gets called in the case of a field getting updated. Contrary to the __Button__ handling, it is not obligatory to bind a function to every value field, but the binding is done in the same way. If you name a value field and a function in your class the same, the Interactor will bind them. Here is an example: 

### Define the value field:
```
        <Parameter>
            <Name>checkbox_clicked</Name>
            <Text>Check me out</Text>
            <Value>False</Value>
            <ValueType>CheckBox</ValueType>
        </Parameter>
```

### Define the function
```
# Interactor class
class MyInteractor(Interactor):
    def __init__(self, *args, **kwds):
        # Init interactor
        super().__init__("MyPythonPart.pyp", *args, **kwds)

    # ... other stuffs ...

    def checkbox_clicked(self, page, name, value):
        message = f"Hey you {'' if value else 'un'}checked the box!"
        AllplanUtil.ShowMessageBox(message, AllplanUtil.MB_OK)
```

As you see, the name of the function is the same as the name of the checkbox, and the function has 3 arguments, the page of the value field, the name of the value field and the new value.
The defined function has to either return nothing or a value. If you return some value, the value field will be set to that value.


# Other functions

## `set_value(self, key: str, value) -> None`
Set a value field to a new value 

Arguments:
- `key: name of the value to be modified`
- `value: new value`

Throws:
- `InteractorError: In the case the key does not exist`

## `get_value(self, key: str) -> Any`
Get the value of a value field

Arguments:
- `key: name of the value to be fetched`

Throws:
- `InteractorError: In the case the key does not exist`

Returns:
- `value of the field`

