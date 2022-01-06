# Interactor
*Examples: __InteractorExamples/\*__*

Althought we can do a lot with just the basic PythonParts, we can only unlock the full potential of this API using something called an interactor. The interactor is a class that gives us full control over a PythonPart. It is harder to work with, but on the other hand it gives us complete control.

## Setting up

To use the interactor we first need to tell the PythonPart that we will take control by setting the `<Interactor>` node in `<Script>` to `True`:

```
    ...
    <Script>
        <Name>path/to/script.py</Name>
        <Title>MyInteractor</Title>
        <Interactor>True</Interactor>
    </Script>
    ...
```

Now, that we have notified Allplan that we will use an interactor we need to actually create an interactor in our code. The python script for this PythonPart still has to define a function for checking the version, but defining the `create_element` is optional as it is only going to be used to render a library preview. 

In addition to the `check_version` function, we need to define the `create_interactor` function which will be called once, when we open a PythonPart. As the name suggests, the `create_interactor` function has to return a interactor object.

## Interactor object

The interactor you define does not have to inherit from any base class, but it has to define a certain set of functions that are called by Allplan when some events happen:

- `on_control_event`
- `modify_element_property`
- `on_cancel_function`
- `on_preview_draw`
- `on_mouse_leave`
- `process_mouse_msg`

Along with these functions, the interactor has to have a constructor where the whole setup for the PythonPart is done. The setup is non-trivial to explan, hence I will forward you to this [interactor template class](../Library/Interactor.py), where in the constructor you can see how to set up the interactor.

### `on_control_event`
*Example: __InteractorExamples/DrawingFileDataInteractor.pyp__*

```
    def on_control_event(self, event_id):
        """
        Called when a button is clicked

        Args:
            event_id: event id of control.
        """
```

This method is called when a button is clicked in the Allplan UI, and the only argument to this function is the event id of the button. 

### `modify_element_property`
*Example: __InteractorExamples/WallInteractor.pyp__*

```
    def modify_element_property(self, page, name, value):
        """
        Modify property of element

        Args:
            page:   the page of the property
            name:   the name of the property.
            value:  new value for property.
        """

        update_palette = self.palette_service.modify_element_property(page, name, value)

        if update_palette:
            self.palette_service.update_palette(-1, False)
```

This method is called when an input field is modifed, when this happens, we have to update the pallete if needed, which can be seen in the example above.

### `on_cancel_function`
```
    def on_cancel_function(self):
        """
        Check for input function cancel in case of ESC

        Returns:
            True/False for success.
        """

        self.palette_service.close_palette()
        return True
```

This method is called when the PythonPart is closed. The main function of this method is to close the palette when the PythonPart is closed, that is done as in the example above. The function returns `True` if the closing process was sucessful.