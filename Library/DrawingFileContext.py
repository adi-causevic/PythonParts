########################################
#                                      #
#   Created by Kookie on 27.11.2021.   #
#                                      #
########################################

import NemAll_Python_BaseElements as AllplanBaseElements

class DrawingFileContext:
    """
    Class for saving the current context of the drawing files.

    Arguments:
        doc: DocumentAdapter    Document adapter from the program that is calling the initializer

    Documentation available on github
    """

    def __init__(self, doc) -> None:
        # Inintialization
        self.doc = doc
        self.df_service = AllplanBaseElements.DrawingFileService()

    def __enter__(self):
        # Save context and unload all files
        self.context = self.df_service.GetFileState()
        self.df_service.UnloadAll(self.doc)
        # Return DrawingFileService as it is probably going to be useful
        return self.df_service
        
    def __exit__(self, type, value, traceback):
        # Get the mappings int -> DrawingFileLoadState
        state_map =  AllplanBaseElements.DrawingFileLoadState.values
        # Unload all curretnly active drawing files
        self.df_service.UnloadAll(self.doc)
        # For every drawing file in context set the value to the one before the transaction
        for index, state_val in self.context:
            # Check if the state is valid, sometimes the state is -1 which does not have a corresponding value
            # In case an invalid value is given, ignore
            if state_val not in state_map:
                continue
            state = state_map[state_val]
            self.df_service.LoadFile(self.doc, index, state)


