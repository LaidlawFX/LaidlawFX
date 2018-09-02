# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import json
from LaidlawFX import log

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: jsonpath(node)
#  Raises: N/A
# Returns: None
#    Desc: Check 
# -----------------------------------------------------------------------------

def jsonpath(node):

    pref        = os.environ.get("HOUDINI_USER_PREF_DIR")
    dirpath     = os.path.dirname(pref)
    prefpath    = dirpath + "/houdini_user_settings.json"
    
    return prefpath

# -----------------------------------------------------------------------------
#    Name: hq_emailTo()
#  Raises: N/A
# Returns: None
#    Desc: Check 
# -----------------------------------------------------------------------------

def hq_emailTo(node):
    prefpath    = jsonpath(node)
    
    address     = ""
    data        = {}
    if os.path.exists(prefpath):
        with open(prefpath, 'r') as f:
            data = json.load(f)
    address     = data['email']      
               
    return address
    
# -----------------------------------------------------------------------------
#    Name: create_email(node)
#  Raises: N/A
# Returns: None
#    Desc: Check 
# -----------------------------------------------------------------------------

def create_email(node):
    msg         = hou.ui.readInput("Enter e-mail : ", buttons=("OK", "Cancel"),help="Please provide your ubisoft e-mail address so we can record it locally for faster processing.", title="Local E-mail Preference", initial_contents=hou.getenv("USER","username")+"@Ubisoft.com")
    if msg[0]:
        log.node(node, 1, "E-mail will not be stored.")
        return
    elif  "@ubisoft.com" not in msg[0]:
        log.node(node, 1, "It needs to be a Ubisoft e-mail address.")
        return        
    else :
        email   = msg[1]    
        user    = hou.getenv("USER")
        data    = {}
        data["user"]=user
        data["email"]=email
        with open(jsonpath(node), 'w') as f:
            json.dump(data, f)  