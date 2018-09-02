# =============================================================================
# IMPORTS
# =============================================================================

import os
import hou
import inspect
from LaidlawFX import log

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: pre(node)
#  Raises: N/A
# Returns: None
#    Desc: Render Pre-Script
# -----------------------------------------------------------------------------

def pre(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        if node.evalParm("tprerender"):
            script = node.evalParm("prerender")
            if script:
                if node.evalParm("lprerender") == "python":
                    exec(script)
                else:
                    hou.hscript(script)
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return
# -----------------------------------------------------------------------------
#    Name: post(node)
#  Raises: N/A
# Returns: None
#    Desc: Render Post-Script
# -----------------------------------------------------------------------------

def post(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        if node.evalParm("tpostrender"):
            script = node.evalParm("postrender")
            if script:
                if node.evalParm("lpostrender") == "python":
                    exec(script)
                else:
                    hou.hscript(script)
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return            

# -----------------------------------------------------------------------------
#    Name: pre_menu(node)
#  Raises: N/A
# Returns: None
#    Desc: Search directory for rendered folders
# -----------------------------------------------------------------------------

def pre_menu(node):
    try:
        path = str(internal.hm().path.dirHeader(node,internal)[0])
        dirList = os.listdir(path)
        dirs = []
        for dirName in dirList:
                      fullPath = os.path.normpath(os.path.join(path, dirName))
                      if os.path.isdir(fullPath):
                                     dirs += [dirName, dirName]
        
        return dirs
    except :
        return ["ElementNotRendered", "ElementNotRendered"]              