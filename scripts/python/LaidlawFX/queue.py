# =============================================================================
# IMPORTS
# =============================================================================

import hou
import inspect
import re
from LaidlawFX import log

# -----------------------------------------------------------------------------
#    Name: execute(node)
#  Raises: N/A
# Returns: None
#    Desc: Processes all the nodes in series.
# -----------------------------------------------------------------------------

def execute(kwargs):
    node        = kwargs['node']
    nodeName    = node.path()
    function    = inspect.stack()[0][3]
    try:
        que     = node.evalParm("que")
        if que != 0 :
            log.node(node, 1, "\nRendering Queue from: " + str(nodeName))        
        
            for i in range(1,que+1):
                try:
                    render(kwargs, i)
                except:
                    return
                
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodeName+"...exiting")
        return

# -----------------------------------------------------------------------------
#    Name: multiparm_execute(node,ropque)
#  Raises: N/A
# Returns: None
#    Desc: Execute button based on multiparm list.
# -----------------------------------------------------------------------------
    
def multiparm_execute(kwargs,ropque):

    i = str(re.findall('\d+', ropque)[0])
    try:
        render(kwargs, i)  
    except:
        return
        
# -----------------------------------------------------------------------------
#    Name: render(node, i)
#  Raises: N/A
# Returns: None
#    Desc: Presses the buttons.
# -----------------------------------------------------------------------------

def render(kwargs, i):
    node        = kwargs['node']   
    nodeName    = node.path()
    function    = inspect.stack()[0][3]
    try:
        que     = node.evalParm("que")    
        eC      = node.evalParm("enableCommand") 

        if node.evalParm("enableSaveHIP") :
            hou.hipFile.save()       
            hou.hipFile.saveAsBackup()    

        try:
            ropparm = node.node(node.evalParm('rop'+str(i)))
        except (AttributeError):
            log.node(node, 1, "Verify the render path for Queue item: " + str(i))
            return
        if ropparm != None :
            roppath = ropparm.path()
            ropnode = hou.node(roppath)
            if eC == 1 :
                try:            
                    ropcommand = node.evalParm('command')
                    if ropcommand == 'custom' :
                        ropcommand = node.evalParm('custom')
                    if ropcommand == 'rop' and node.evalParm('cmnrop0') != '' :
                        ropcommand = node.evalParm('cmncommand0')                            
                except (AttributeError):
                    log.node(node, 1, 'No button type "' + str(ropcommand) + '" on node ' + str(ropparm.path()))                     
                    return                    
                #else :
                #    print "No Rop button specified to process."
            else :
                ropcommand = node.evalParm('command'+str(i))
            ropenable = node.evalParm('enableQue'+str(i))
            if ropenable == 1 :
                log.node(node, 1, "Queue Item: " + str(i) + " of " + str(que)) 
                log.node(node, 1, "Pressed Button: " + str(ropcommand) + " from node " + str(ropparm.path())) 
                try:
                    if ropnode.parm(str(ropcommand)) != None :
                        ropnode.parm(str(ropcommand)).pressButton()
                    else :
                        node.hm().log.log(node, 1, "Verify the render path for Queue item: " + str(i))
                except (KeyboardInterrupt, SystemExit):
                    log.node(node, 1, "Interrupt requested of "+function+" for "+nodeName+"...exiting")
                except (AttributeError):
                    log.node(node, 1, 'No button type "' + str(ropcommand) + '" on node ' + str(ropparm.path()))                     
                    return
        else :
            log.node(node, 1, "Verify the render path for Queue item: " + str(i))
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodeName+"...exiting")
        return
        
# -----------------------------------------------------------------------------
#    Name: dropdown_menu(kwargs, roptype)
#  Raises: N/A
# Returns: The list of menu options
#    Desc: List butons based on the node path.
# -----------------------------------------------------------------------------

def dropdown_menu(kwargs, roptype):
    node        = kwargs['node']
    ropque      = kwargs['parm'].name()

    button      = []
    que         = str(re.findall('\d+', ropque)[0])
    roppath     = node.evalParm(roptype+que)
    ropnode     = hou.node(roppath)
    ropparm     = hou.parm(roppath)

    if ropnode != None :
        buttonList = [p for p in ropnode.parms() if p.parmTemplate().type() == hou.parmTemplateType.Button]
        #toggles = [p for p in node.parms() if isinstance(p.parmTemplate(), hou.ButtonParmTemplate)]
        for parm in buttonList:
            if str(parm.name()) != 'renderdialog' :
                button.extend([str(parm.name()),str(parm.description())])        
    elif ropparm != None:       
        button  = [str(ropparm.name()), str(ropparm.description()) ]
    else:
        if roptype == 'rop' :
            button = ['execute','Render','reload', 'Reload', 'renderpreview', 'Render To Mplay', 'executebackground', 'Render in Background']
        else :
            button = ['execute', 'Please assign rop']

    return button

    
