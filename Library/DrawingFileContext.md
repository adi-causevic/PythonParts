# Interactor
## Description
Context manager for Allplan drawing files. Used when you have to modify the state of any drawing file but want to reset the state before exiting the function.

## Usage

```

with DrawingFileContext(doc) as df_service:
    ...
    # do stuff with drawing files
    ...

# State from before the with block reset
```

The `DrawingFileContext` initializer only takes a `DocumentAdapter` as an arguemnt.

On entering the `DrawingFileContext` block, all drawing files are unloaded after the current state of all the files is stored. When exiting the block the state of the drawing files is reset to the previous state.

The `__enter__` method returns a `DrawingFileService` object which can, but does not have to, be used using the `as` keyword, as seen in the example above. 

```
with DrawingFileContext(doc):
    ...
    # do stuff with drawing files
    ...

# State from before the with block reset
```

This is a valid usage for the `DrawingFileContext` but, as you probably plan to do something with drawing files in the block, you will probably create a new instance of a `DrawingFileService`, hence better use the `as df_service` syntax.