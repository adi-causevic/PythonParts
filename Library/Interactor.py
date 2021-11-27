########################################
#                                      #
#   Created by Kookie on 25.11.2021.   #
#                                      #
########################################

import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeo

from BuildingElementPaletteService import BuildingElementPaletteService
from BuildingElementService import BuildingElementService

import xml.etree.ElementTree as ET
import os
from typing import Any, Callable, Dict


class InteractorError(Exception):
    """
    Interactor error class
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class Interactor:
    """
    Wrapper class for the python parts interactor functions

    Usage:

    To use the interactor you first have to notify Allplan that your python part is going to 
    use an interactor by adding an attribute to the script block in the *.pyp file:

    ```
    <Script>
        <Name>path/to/InteractorScript.py</Name>
        <Text>Interactor PythonPart</Text>
		<Interactor>True</Interactor>
    </Script>
    ```
    
    Afterwards you have to create the InteractorScript.py file that should contain at least 3 functions:

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

    Your interactor class has to inherit from the this interactor, and first call this interactors init method.
    Forward all arguments and keywords to the Interactor initializer as well as the name of the python part, 
    this name is the exact name of the *.pyp file. If you want you can skip the .pyp extension and just use the file name.

    The initializer of the Interactor will take care of everything from pallete service creation to event function binding.
    """


    def __init__(self, name: str, coord_input, pyp_path, str_table_service, build_ele_list, build_ele_composite, control_props_list, modify_uuid_list) -> None:
        # Set path
        self.pyp_path               = pyp_path
        # Check if the name includes pyp
        # Assign pyp_file and name variables
        if name.endswith(".pyp"):
            self.name               = name[:-4]
            self.pyp_file           = os.path.join(pyp_path, name)
        else:
            self.name               = name
            self.pyp_file           = os.path.join(pyp_path, f"{name}.pyp")

        # Check if pyp file exists
        if not os.path.exists(self.pyp_file):
            raise InteractorError(f"The file {name}.pyp does not exist, please pass a valid .pyp file name")

        # Set variables
        self.coord_input            = coord_input
        self.str_table_service      = str_table_service
        self.build_ele_service      = BuildingElementService()        
        self.build_ele_composite    = build_ele_composite
        self.build_ele_list         = build_ele_list
        self.build_ele              = self.build_ele_list[0]
        self.control_props_list     = control_props_list
        self.modify_uuid_list       = modify_uuid_list

        self.drawing_minmax         = AllplanGeo.MinMax3D()
        # Create Palette service, and initial show
        self.palette_service        = BuildingElementPaletteService(
                                                self.build_ele_list, 
                                                self.build_ele_composite, 
                                                self.name, 
                                                self.control_props_list, 
                                                self.pyp_file
                                                )
        self.palette_service.show_palette(self.pyp_file)

        self.model_ele_list, self.handles_list = [], []

        # Link buttons and other fields to functions
        self.element_tree = ET.parse(self.pyp_file)
        root = self.element_tree.getroot()
        # Functions called when an event occurs
        self.event_functions: Dict[int, Callable] = {}
        # Functions called when a value is modified
        self.modify_functions: Dict[int, Callable] = {}

        # Add checking of pallette files and #include files
        for child in root.iter("Parameter"):
            type_find = child.find("ValueType")
            if 'Button' in type_find.text:
                # Events occur when a button is pressed
                # Get event id and name, and check if the event id has been already used
                event_id = int(child.find("EventId").text)
                func_name = child.find("Name").text
                if event_id in self.event_functions:
                    raise InteractorError(f"File {self.name}.pyp contains several buttons with EventId={event_id}")
                # Check if function exists
                if not hasattr(self, func_name):
                    raise InteractorError(f"The class {type(self).__name__} does not contain function {func_name}!")
                # Assign function
                self.event_functions[event_id] = getattr(self, func_name)
            else:
                # For everything else modify_element_property function is called
                # Check for potential function name
                func_name = child.find("Name")

                if func_name is None:
                    continue
                func_name = func_name.text
                # Assign function if it exists
                if hasattr(self, func_name):
                    self.modify_functions[func_name] = getattr(self, func_name)

    def get_value(self, key: str):
        if hasattr(self.build_ele, key):
            return getattr(self.build_ele, key).value
        raise InteractorError(f"Key {key} does not exist")

    def set_value(self, key: str, value):
        if hasattr(self.build_ele, key):
            getattr(self.build_ele, key).value = value
            self.palette_service.update_palette(-1, False)
            return
        raise InteractorError(f"Key {key} does not exist")

    def set_hint(self, hint):
        self.coord_input.InitFirstElementInput(AllplanIFW.InputStringConvert(hint))

    def create(self):
        return self.model_ele_list, self.handles_list

    def modify_element_property(self, page: int, name: str, value: Any):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """
        # Check if the name of the modified property is a bound to function
        if name in self.modify_functions:
            # Get result of the function call
            ret = self.modify_functions[name](page, name, value)
            # If the result is not None, assign new values to the element
            if ret is not None:
                value = ret
                self.set_value(name, value)

        print(page, name, value)
        # Modify property and update pallete
        update_palette = self.palette_service.modify_element_property(page, name, value)
        if update_palette:
            self.palette_service.update_palette(-1, False)
        
    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()
        return True

    def on_preview_draw(self):
        """
        Handles the preview draw event
        """

    def on_mouse_leave(self):
        """
        Handles the mouse leave event
        """

    def on_control_event(self, event_id):
        """
        On control event

        Args:
            event_id: event id of control.
        """
        # Get ele and doc
        build_ele = self.build_ele_list[0]
        doc = self.coord_input.GetInputViewDocument()


        # Check if event id is bound to function
        if event_id in self.event_functions:
            # Fetch and call the function
            func = self.event_functions[event_id]
            print(f"Dispatching function: {func.__name__}")

            return func(build_ele, doc)
        raise InteractorError(f"Function for {event_id=} not specified!")

    def process_mouse_msg(self, mouse_msg, pnt, msg_info):
        """
        Process the mouse message event

        Args:
            mouse_msg:  the mouse message.
            pnt:        the input point in view coordinates
            msg_info:   additional message info.

        Returns:
            True/False for success.
        """
        return True
