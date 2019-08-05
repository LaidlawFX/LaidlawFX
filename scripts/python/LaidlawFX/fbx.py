# =============================================================================
# IMPORTS
# =============================================================================

import hou
import inspect
import exceptions
import datetime
import sys

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: execute()
#  Raises: N/A
# Returns: None
#    Desc: Creates a fbx tree to export geometry based on names, and apply game materials.
# -----------------------------------------------------------------------------

def execute(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
    
        eVil                   = node.evalParm('enableVerbosity') 
        begTime = datetime.datetime.now()
        if eVil >= 1 :
            print(' ')
            print('Begin Time of Obj Creation : ' + str(begTime))
               
        exportNode             = node.node('objectHierarchy')
        nodeOut                = node.node('objects/OUT')         

        for child in exportNode.children():
            child.destroy()
            
        eDebug                 = node.evalParm('enableObjDebug')
        nameList               = ()
        try:        
            geo                = nodeOut.geometry()
            attr               = geo.findPrimAttrib('name')
            nameList           = attr.strings()
        except (KeyboardInterrupt):
            print('Exiting because user decided geometry cook is taking too long.')
            return        
                    
        for name in nameList : 
            
            if eVil >= 2 :
               print("Creating Object : " + name)

            animNode                = exportNode.createNode('geo', name)          
            animNode.setColor(hou.Color( (0.9, .5, 0) ) )
            animNode.moveToGoodPosition()
            
            animNode.createNode('object_merge','Import')
            animNodeImport         = animNode.node('Import')
            animNodeImport.parm('xformtype').set('none')
            animNodeImport.parm('objpath1').set(nodeOut.path())
            
            animNodeBlast          = animNode.createNode('blast', name)           
            animNodeBlast.parm('negate').set(1)
            deleteGroup            = '@name=`opname(".")`'
            animNodeBlast.parm('group').set(deleteGroup)
            animNodeBlast.parm('grouptype').set('prims')
            animNodeBlast.setFirstInput(animNodeImport,0)
            animNodeBlast.moveToGoodPosition()  
            animNodeBlast.setDisplayFlag(True)
            animNodeBlast.setRenderFlag(True)             
            
                                 
        endTime = datetime.datetime.now()
        tolTime = endTime - begTime
        
        if eVil >= 1 :
            print "End    Time of Obj Creation: " + str(endTime)
            print "Total  Time of Obj Creation: " + str(tolTime) 
            
    except (KeyboardInterrupt):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return
    except (SystemExit):
        return

# -----------------------------------------------------------------------------
#    Name: clear()
#  Raises: N/A
# Returns: None
#    Desc: Remove objects.
# -----------------------------------------------------------------------------

def clear(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
               
        exportNode             = hou.node('objectHierarchy')        
        for child in exportNode.children():
            child.destroy()
            
    except (KeyboardInterrupt):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return
    except (SystemExit):
        return            