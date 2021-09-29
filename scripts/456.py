#"""Perform tasks when houdini is launched."""
# =============================================================================
# IMPORTS
# =============================================================================

import hou

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: startup_check()
#  Raises: N/A
# Returns: None
#    Desc: For admin tells you what script is running.
# -----------------------------------------------------------------------------

def startup_check():
    print("Running : 456.py")
if hou.getenv('HOUDINI_ADMIN'): 
    startup_check()


# -----------------------------------------------------------------------------
#    Name: houDir()
#  Raises: N/A
# Returns: None
#    Desc: Set the prompt to display the current directory followed by an arrow
# -----------------------------------------------------------------------------

def houDir():

    currentDirectory = hou.hscript("oppwf()")[0][:-1]
    commandPrompt = str(currentDirectory) + " -> "
    hou.hscript("prompt '`strcat(oppwf(), \" -> \")`'")
    hou.cd(currentDirectory)

    #print("The current directory  is: " + currentDirectory)
    #print("The directory should be: " + commandPrompt)
    #print("The current node is: " + str(hou.node('.').path()))
    #print("test")
    #print("The updated directory  is: " + updatedDirectory)
houDir()


# =============================================================================
# END
# =============================================================================
# print(" ")
