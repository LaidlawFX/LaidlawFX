# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import subprocess
from LaidlawFX import log

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: mplay(node, path)
#  Raises: N/A
# Returns: None
#    Desc: Launch and explorer window to the defined directory
# -----------------------------------------------------------------------------

def mplay(node, path):
    mplay           = hou.getenv('HFS') + r"\\bin\mplay.exe"
    
    if not os.path.isfile(pathCheck):
        hou.ui.displayMessage('An image has not been written yet.', severity=hou.severityType.Warning, help="Current image path is:  " + path, title="Mplay File Check")
    else :
        log.node(node, 1, "Opening: " + path) 
        proc = subprocess.Popen([mplay,path], shell=True)

# -----------------------------------------------------------------------------
#    Name: gplay(node, path)
#  Raises: N/A
# Returns: None
#    Desc: Launch and explorer window to the defined directory
# -----------------------------------------------------------------------------

def gplay(node, path):
    gplay           = hou.getenv('HFS') + r"\\bin\gplay.exe"
    
    if not os.path.isfile(pathCheck):
        hou.ui.displayMessage('A geometry has not been written yet.', severity=hou.severityType.Warning, help="Current geometry path is:  " + path, title="Gplay File Check")
    else :
        log.node(node, 1, "Opening: " + path) 
        proc = subprocess.Popen([gplay,path], shell=True)