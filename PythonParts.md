# PythonParts documentation

As the current documentation about PythonParts is far from perfect
in this unofficial documentation all the quirks and features of 
this great API can be written down. 

In this page some basic instruction on how to write the documentation,
and where else to look for informations will be written down. As well 
as the index of the covered topics.

## Index


## How to find informations

Beside this documentation there are some other resources from which
to learn the basics of how to work with this API. Allplan has a getting 
started tutorial online as well as some other documentation on various
functions. 

Beside that there is a large amount of examples that Allplan
is shipped with, that can be found <ToDo: where>. In the examples, 
numerous topics are covered with code which is quite well commented.

## How to write documentation

This documentation will be completely written in markdown (<ToDo: Cheatsheet>).
When a new file is added it has to be added to the index.
<ToDo: Class documentation>
<ToDo: Function documentation>
Seperated in 3 sections: Tutorials, API documentation, FAQ



Tutorials:
	Getting started
	Debugging
	.pyp
	.py
	Languages
	Icon
	Interactor
	Unit tests
	


## Files

The PythonPart is described using 2 files, the <name>.pyp file 
describes the look of the PythonPart, while the <script_name>.py 
describes its behaviour. These 2 files are the bare minimum for the 
part to function, and everything else is optional

### .pyp file



### <script_name>.py 

### Optional

Along with the .pyp and .py files, additional optional files 
can be defined. All of them have specific names and have to be located
in the same directory as the <name>.pyp file.

#### <name>.png

This file has to be located in the same directory as the 

#### <name>_<lang>.xml






