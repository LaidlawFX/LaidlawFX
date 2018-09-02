#orbolt safe

# =============================================================================
# IMPORTS
# =============================================================================

import hou
import time

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: parm_check()
#  Raises: N/A
# Returns: None
#    Desc: Check range completeness.
# -----------------------------------------------------------------------------

def parm_check(node,parm):
    value = 1.0
    if node.parm(parm) :
        value = node.evalParm(parm)
    if value == 1.0 :
        value = int(value)
    else :
        value = float(value)
    return value

# -----------------------------------------------------------------------------
#    Name: percent()
#  Raises: N/A
# Returns: None
#    Desc: Check range completeness.
# -----------------------------------------------------------------------------

def percent(node):
    frame_start = parm_check(node, 'f1')

    frame_end   = parm_check(node, 'f2')

    frame_inc   = parm_check(node, 'f3')  

    if frame_start == frame_end and frame_start == frame_inc and frame_end == frame_inc:
        pc      = 'Frame 1 (1 of 1, 100%) - '+date+ ' from: ' + str(node.path())
        return pc    

    if frame_inc == 1.0 :
        if node.parm("frame") :
            frame   = int(node.evalParm("frame"))         
        else :
            frame   = hou.intFrame()
    else :
        if node.parm("frame") :
            frame   = float(node.evalParm("frame"))            
        else :
            frame   = hou.frame()

    padlen  = len(str(abs(frame_end)))
    date    = str(time.strftime("%X %p"))
    #Total Frame is (Beg Frame - End Frame + One Frame) / divisions
    frame_total      = (frame_end-frame_start+1) / frame_inc
    #Current Frame is 

    if frame <= frame_start :
        frame_cur      = 1 
    elif frame>=frame_end :
        frame_cur      = frame_total
    else :
        frame_cur = (frame-frame_start+1)

    #Percentage
    per     = int(float(frame_cur)/float(frame_inc))/float(frame_total)
    p       = int(10000 * per )/100
    #Print Message
    
    pc      = 'Frame '+str(frame).zfill(padlen)+' ('+str(frame_cur).zfill(padlen)+' of '+str(frame_total).zfill(padlen)+', '+str(p).zfill(2)+'%) - '+date+ ' from: ' + str(node.path())
     
    return pc