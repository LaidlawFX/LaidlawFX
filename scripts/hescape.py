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
    print("Running : hescape.py")
if hou.getenv('HOUDINI_ADMIN'): 
    startup_check()

# =============================================================================
# END
# =============================================================================
# print(" ")
