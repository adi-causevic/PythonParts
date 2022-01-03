# Buttons and control events

In this document only buttons that start events will be discussed, if you are looking for buttons that act as inputs (`PictureButtonList`, `PictureResourceButtonList`, `RadioButtonGroup` and `RadioButton`) take a look at the [PypFile](./PypFile.md) documentation.

In this documentation the two aspects of buttons will be discussed:

- The looks
- The function

## Buttons in `*.pyp` files

There are 3 different button types, that only differ in the way they are showed in the UI. All the buttons are defined similarely as a parameter in a page, with the `ValueType`, `Value` and `Text` elements having different values:

```
    <Parameter>
        <Name>Button1</Name>
        <EventId>1000</EventId>
        <ValueType>***</ValueType>
    </Parameter>
```

The `EventId` and `Name` elements are obligatory. The `Name` tag has no real use, while the `EventId` is used in the script to identify which button was clicked. The `EventId`'s of different buttons should differ, as they are the only way to know which button was clicked. In the case the `EventId`'s are the same, you will not be able to know what button was clicked. 

The buttons have to be defined inside a [`<Row>`](https://pythonparts.allplan.com/2021-1/How_to_define_the_PythonPart_pyp_file.htm#_%3CValueType%3ERow%3C/ValueType%3E) element that is basically used as a tag. 

### `Button`

Simple button that has text written on it. The text displayed is defined in the `Text` element in the XML or using `TextId` if a stringtable is used. 

Example:

```
    <Parameter>
        <Name>SimpleButton</Name>
        <EventId>1001</EventId>
        
        <Text>Click me!</Text>
        <ValueType>Button</ValueType>
    </Parameter>
```

### `PictureButton`

This button is almost the same as the normal button, the only difference being that on top of this button no text is redndered but a picture. The picture to be rendered must be in the same location as the `*.pyp` file, and it is defined in the `<Value>` element: 

```
    <Parameter>
        <Name>PictureButton</Name>
        <EventId>1002</EventId>
        <Text></Text>
        <Value>image.png</Value>
        <ValueType>PictureButton</ValueType>
    </Parameter>
```

### `PictureResourceButton`

The last of the bunch is the `PictureResourceButton` that, like the `PictureButton` has a image rendered on it instead of simple text as in the normal `Button`. The resource id of the resource to be rendered is defined in the `<Value>` element as with the picture button.


```
    <Parameter>
        <Name>PictureResourceButton</Name>
        <EventId>1003</EventId>
        <Text></Text>
        <Value>16433</Value>
        <ValueType>PictureResourceButton</ValueType>
    </Parameter>
```

## Control events in `*.py` scripts

After we defined a button, we need to link the button to some background logic, and that is done by defining the `on_control_event` function. In the case you are using an interactor you have to define the function within the interactor class. If you are not using an interactor, the function just has to be defined withing the `*.py` script.

The `on_control_event(build_ele, event_id)` function takes two arguments:

- Current build element `build_ele`
- The event id of the clicked button `event_id`

A typical simple event handler might look like this:

```
def on_control_event(build_ele, event_id):
    if event_id == 1000:
        func1(build_ele)
        return
    if event_id == 1001:
        func1(build_ele)
        return
    ...
```

While this is perfectly ok to do, it gets messy when you add many buttons, hence mapping the event id's to function can be done a bit more elegantly:

```
event_map = {
    1000: func1,
    1001: func2,
    ...
    1010: func11,
}

def func1(build_ele):
    print("Function 1 has been called")

...

def on_control_event(build_ele, event_id):
    if event_id in event_map:
        event_map[event_id](build_ele)
```


## Interactor

When using the [interactor class](../Library/Interactor.py) the binding of buttons is done automatically. When a button is clicked, a member function of the interactor class, with the same name as the button, is called. This is discussed in more detail [here](../Library/Interactor.py).

