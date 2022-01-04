# How to write a `*.pyp` file

[Here](https://pythonparts.allplan.com/2021-1/How_to_define_the_PythonPart_pyp_file.htm) you can find the official documentation on this topic. The documentation is actually so good, and the topic so long, that I will urge you to go visit the official documentation. In this document I'll just add my pinch of salt.

## Boolean operations

To most of the nodes you can add the `<Visible>` and `<Enable>` child nodes with which you can control if the parent node is visible/enabled. These child nodes are purely esthetic, but using them might lead to a better/cleaner UI. 

The `<Visible>` node, as the name might suggest determines if the parent node is visible in the Allplan UI. On the other hand, the `<Enable>` node is used in various input nodes and when the value of the `<Enable>` node is set to False, the user cannot modify/click the input.

Both nodes take a boolean values/expressions as the input. 

```
    // An example of a hidden input field might
    <Parameter>
        <Name>hidden_text</Name>
        <Value>I am hidden</Value>
        <Visible>False</Visible>
        <ValueType>String</ValueType
    </Parameter>
```

Where these nodes become really useful is when using boolean expressions. The values in the boolean expressions can be constants as well as the values of different input fields of the same PythonPart. 

For example, if you want your input to be enabled if a checkbox is set to true, you can simply write the name of the checkbox as the boolean value in the enabled node:

```
    // Other nodes used in boolean expressions
    <Parameter>
        <Name>checkbox_1</Name>
        <Value>True</Value>
        <ValueType>Checkbox</ValueType
    </Parameter>
    <Parameter>
        <Name>integer_input</Name>
        <Value>1337</Value>
        <Enable>checkbox_1</Enable>
        <ValueType>Integer</ValueType
    </Parameter>
```

Comparisons are also possible, but the `<` character is not allowed in any shape or form as the parser confuses it with the start of the closing tag of the node. Hence, if you need to compare quantites you will have to use the `>` or `>=` operator:

```
    ...
    <Visible> value_x > 10 </Visible>
    ...
```

If you want to use any basic boolean operator, they are the same as in python: `and`, `or` and `not`. Parentheses and text comparisons are also allowed:

```
    ...
    <Visible> (value_x > 10) and (value_text != "") </Visible>
    ...
```

Last but not least, if you need to check if a value is in a set of values, you can do it using the `in` operator:

```
    ...
    <Visible> value_pen in {2, 3, 7}</Visible>
    ...
```

## `*.pal` files

If you want to seperate the options in the `*.pyp` file from the pallete, you can do it by extracting the UI to a  `*.pal` file.I will try to write a simple explanation, but it is easier just looking at one of many examples. 

The `*.pal` file has to have the same name as the `*.pyp` file that describes the options. The `*.pal` file has to have the same structure as the `*.pyp` file (`<Element>`, `<Script>`, `<Page>`, etc.) where the only difference is that within the `<Script>` node you only have to define the `<Title>` of the PythonPart. The title written in the `*.pal` file should be the same as the title in the `*.pyp` file.

All in all, I don't see a realistic use of this separation.

## `#include`

As with `C` and `C++` the `#include <file>` option just copy pastes the contents of the file included into the `*.pyp` file. An example of a usecase is if you have a standard header/footer for every page of your PythonPart, instead of copy-pasting the code every time something changes, you can just define it in a separate file and `#include` it in the `*.pyp` file. 