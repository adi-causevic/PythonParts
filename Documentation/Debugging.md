# Debugging

Debugging PythonParts is done by either using the DebugPy package or the deprecated PTVSD package, so in the first step we will check/install one of the packages.

## Installing DebugPy

The first step for debugging your PythonPart scripts is to install the DebugPy package. 

To do so, open PowerShell or cmd and move into the Allplan Python interpreter directory that should be located at PRG/Python (eg. `C:\Program Files\Allplan\Allplan <VERSION>\Prg\Python`), where the python interpreter should be located (you can check that by listing the contents of the directory with `ls`).

Next, we will check if the we already have DebugPy installed by executing `python -m pip show debugpy`. In the case the package is installed `pip` will list out some information about the package like the name, version, summary... In the case the package is not installed, a warning will be issued `WARNING: Package(s) not found: debugpy`.

In the case you got the warning, you have to install the package by executing `python -m pip install debugpy`, and a short while later almost everything is ready for debugging.

## Starting debugging

To start debugging we first need to open a port for debugging. That can be done by hand, but as the Allplan Gods have blessed us, there is already a script present for doing just that.

Go to the PythonParts examples directory (`ETC/Examples/PythonParts`) and in the `ToolsAndStartExamples` folder you should find the `StartPythonDebug.pyp` PythonPart. Copy that PythonPart (and the `*.png` if you wish) into a Library folder of your choice (eg. `USR/<user>/Library` for the private library), so you can use it. 

Next go to Allplan and find the `StartPythonDebug` PythonPart and run it.
The PythonPart will open create a message box with the following instructions:

```
Close the info dialog and

Visual Studio Code:
    - Select 'Attach to Allplan'
    - Click 'RUN AND DEBUG'

Visual Studio:
    - Attach to Process
    - Connection type: Python remote (ptvsd)
    - Connection target: localhost:5678
    - Enter
    - Select the Python process
```

After which it will check if you have DebugPy or PTVSD installed and open the 5678 port for debugging.
In the case you have already run the PythonPart you might get an error message. Look at the trace window, and if the error is:

```
Traceback (most recent call last):
  File "C:\ProgramData\Nemetschek\Allplan\2021\Etc\PythonPartsFramework\GeneralScripts\BuildingElementInput.py", line 795, in create_element
    preview_ele_list = self.build_ele_script.create_element(self.build_ele_list[0],
  File "C:\ProgramData\Nemetschek\Allplan\2021\Etc\PythonPartsScripts\ToolsAndStartExamples\StartPythonDebug.py", line 85, in create_element
    debugpy.listen(("localhost", 5678))
  File "C:\Program Files\Allplan\Allplan 2021\Prg\Python\Lib\site-packages\debugpy\__init__.py", line 113, in listen
    return api.listen(address)
  File "C:\Program Files\Allplan\Allplan 2021\Prg\Python\Lib\site-packages\debugpy\server\api.py", line 143, in debug
    log.reraise_exception("{0}() failed:", func.__name__, level="info")
  File "C:\Program Files\Allplan\Allplan 2021\Prg\Python\Lib\site-packages\debugpy\server\api.py", line 141, in debug
    return func(address, settrace_kwargs, **kwargs)
  File "C:\Program Files\Allplan\Allplan 2021\Prg\Python\Lib\site-packages\debugpy\server\api.py", line 243, in listen
    raise RuntimeError(str(endpoints["error"]))
RuntimeError: Can't listen for client connections: [WinError 10048] Only one usage of each socket address (protocol/network address/port) is normally permitted
```

everything is allright, the error is just indicating that the debugger is already active.

## Attaching in Visual Studio Code

### Creating the attach option

If you are using Visual Studio Code for developing PythonParts, you need to create a launch option for attaching VisualStudioCode to the process. To do that, go into the `Run and Debug` tab and click `create a launch.json file` and follow the steps:
- Select what you want do debug (workspace or a specific folder)
- Select `Python` as the environment
- Select `Remote Attach` as for the debug configuration
- Use `localhost` or `127.0.0.1` as the host
- Set the port for the connection to be `5678`

After you click enter after the last step, a launch option that looks like this should be added to the `launch.json` file:

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to remote",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}

Here, you can play with the options, but I only suggest changing the name to `Attach to Allplan` or something like that.

### Attaching the process

After you have started the `StartPythonDebug` PythonPart and clicked `OK`, run the above described launch option. And now you should be able to debug.

## Attaching in Visual Studio

Attachnig to the process in Visual Studio is a bit less straight forward, but nontheless quite easy. After you have started the debugger from Allplan, go to Visual Studio and in the debug dropdown click on `Attach to process...` or click `Ctrl + Alt + P` and follow the steps:
- For the connection type select `Python remote (debugpy)`
- Write `tcp://localhost:5678` as the connection target
- And while the cursor is still in the connection target input field, press enter (DO NOT PRESS THE `Find` BUTTON)
- Press enter or click the `Attach` button
- YOU ARE DEBUGGING

Clicking the `Find` button does nothing but delete the contents of the input field.
