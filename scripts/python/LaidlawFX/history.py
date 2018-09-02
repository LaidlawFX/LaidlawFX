# =============================================================================
# IMPORTS
# =============================================================================

import hou
import inspect
import exceptions
import os
import shutil
import fnmatch
import re
from LaidlawFX  import path
from LaidlawFX  import log


# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: execute(node)
#  Raises: N/A
# Returns: None
#    Desc: Prompt and removes files associated to this node.
# -----------------------------------------------------------------------------
def execute(node):
    dC        = node.evalParm('enable_ondelete')
    
    if dC == 1 :
        path_cache = path.hq_project_path(node)
        if os.path.isdir(path_cache) :
            log.node(node, 0, "The cache directory proposed to be removed is: " + path_cache)
            if not hou.hscriptExpression('opisquitting()'):
                if hou.ui.displayMessage("Do you want to PERMANENTLY delete the caches created by: " + node.path(), buttons=("Yes, I do not need these caches for any scene file or asset.", "No, I'll clean my files up later."), severity=hou.severityType.ImportantMessage, default_choice=1, close_choice=1, help="Inorder to help with project cleanup, this is a method for you to help delete dead file trees on disk, and as the author of this content you'll know best if you'll ever need these files again.  " + path_cache, title="File Cache Cleanup") == 0:
                    if hou.ui.displayMessage("As a warning these files can not be undeleted.", buttons=("Yes, I understand I am deleting my caches forever.", "Oops, I do not want my caches deleted."), severity=hou.severityType.Warning, default_choice=1, close_choice=1, help="As one last heads up we want to double check that you do want to delete your file caches PERMANENTLY. This is a check encase you've created any asset or are referencing these files in another scene. " + path_cache, title="File Cache Cleanup") == 0:
                        log.node(node, 0, path_cache)
                        shutil.rmtree(path_cache)


# -----------------------------------------------------------------------------
#    Name: current()
#  Raises: N/A
# Returns: history_cur
#    Desc: 
# -----------------------------------------------------------------------------

def current(node):
    history_cur = os.path.dirname(path.sopoutput(node)) 
    return history_cur

# -----------------------------------------------------------------------------
#    Name: update()
#  Raises: N/A
# Returns: None
#    Desc: Removes all the files except the ones here.
# -----------------------------------------------------------------------------

def update(node):
    nodePath            = node.path()
    function            = inspect.stack()[0][3]
    try:
        history_list    = node.evalParm("history_list") 
        history_cur     = current(node)
        log.node(node, 2, "-- Updating Unlocked History --")
        log.node(node, 2, "Current      History: " + history_cur)
        log.node(node, 2, "Number of History: " + str(history_list))
        log.node(node, 2, "-------------------------")

        #check if it is zero then add one space
        if history_list == 0 :
            node.parm('history_list').deleteAllKeyframes()
            node.parm('history_list').set(1)   
            hl += 1
            
        # Check if each line is full then add a new line
        hlcheck = 0
        for i in range(hl,0,-1):
            history_lock    = node.evalParm('history_lock'+str(i))
            history_dir     = node.evalParm('history_dir' +str(i))      
            if history_lock == 0 and history_dir != "" :
                hlcheck += 1
        #print hlcheck
        if hlcheck == hl :
            node.parm('history_list').deleteAllKeyframes()
            node.parm('history_list').set(hl+1)
            hl += 1
                         
        for i in range(1,hl+1):
            history_lock       = node.evalParm('historyLock'+str(i))
            history_dir        = node.evalParm('historydir' +str(i))
            history_dirPrev    = node.evalParm('historydir' +str(max(i-1,1)))
            log.node(node, 2, "History Number : " + str(i))               
            log.node(node, 2, "History Directory: " + str(history_dir))
                             
            if history_lock == 1 :
                log.node(node, 2, "History is locked/n")
                continue
            elif history_lock == 0 :
                log.node(node, 2, "History is not locked/n")
                if history_dir == "" and history_cur != history_dirPrev : 
                    #node.parm('history_list').deleteAllKeyframes()
                    #node.parm('history_list').set(hl+1) 
                    node.parm('historydir'+str(i)).deleteAllKeyframes()
                    node.parm('historydir'+str(i)).set(history_cur)
                    log.node(node, 2, "Blank History & make sure it's not equal/n")
                    break
                if history_dir == history_dirPrev :                
                    log.node(node, 2, "They are the same./n")
                    continue
                if history_dir != "" :                
                    log.node(node, 2, "Skip to next./n")
                    continue
                if eVil >=2 :                          
                    log.node(node, 2, "End Update")                   
                    break                
    
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return                                    
           
# -----------------------------------------------------------------------------
#    Name: clear()
#  Raises: N/A
# Returns: None
#    Desc: Clears your history in this list, but does not delete anything. 
#          This can be helpful if you are reseting the node, or you want to clear the list from being saved.
# -----------------------------------------------------------------------------

def clear(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        hl  = node.evalParm("history_list")    
        log.node(node, 1, "Clearing unlocked history")   
        
        for i in range(1,hl+1):
            hL = node.evalParm('historyLock'+str(i))
            if hL != 1:
                node.parm('historydir'+str(i)).deleteAllKeyframes()
                node.parm('historydir'+str(i)).set('')               

    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return


# -----------------------------------------------------------------------------
#    Name: delete()
#  Raises: N/A
# Returns: None
#    Desc: Removes all the files from your parent directoy except those in this list.
# -----------------------------------------------------------------------------

def delete(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        #https://docs.python.org/2/library/os.html -os.walk
        
        history_root = path.hq_project_path(node)
        history_list = node.evalParm("history_list") 
        history_cur  = current(node)
                  
        log.node(node, 1, "Deleting unlocked history")   
            
        history_saved = []
        if os.path.isdir(history_root):
            history_saved.append(history_root)  
        if os.path.isdir(history_cur):
            history_saved.append(history_cur)
        subpath = os.path.normpath(os.path.dirname(history_cur))
        if os.path.isdir(subpath):
            history_saved.append(subpath)
        for i in range(1,history_list+1):
            hL = node.evalParm('history_lock'+str(i))
            history_dir = os.path.normpath(node.evalParm('history_dir'+str(i)))
            if node.evalParm('history_dir'+str(i)) != '':
                if os.path.isdir(history_dir):
                    history_saved.append(history_dir)
                if os.path.isdir(os.path.dirname(history_dir)):
                    history_saved.append(os.path.dirname(history_dir))                    

        log.node(node, 2, "Saved History: ")
        log.node(node, 2, str(history_saved))
        
        for dirpath, dirnames, filenames in os.walk( history_root, topdown=True, onerror=None):
            if os.path.normpath(dirpath) not in history_saved :
                try:                
                    shutil.rmtree(dirpath)
                    log.node(node, 1, "Deleting: " + os.path.normpath(dirpath))                    
                except:
                    log.node(node, 1, "Skipping: " + os.path.normpath(dirpath))              
            else :
                log.node(node, 1, "   Saved: " + os.path.normpath(dirpath))
        log.node(node, 1, "Finished deleting unlocked history") 

    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return 

# -----------------------------------------------------------------------------
#    Name: remove()
#  Raises: N/A
# Returns: None
#    Desc: Deletes this directroy and it's files.
# -----------------------------------------------------------------------------

def remove(node, parm):
    path = os.path.normpath(node.evalParm(parm.replace('deleteHistory','historydir')))
    if path != "" :
        log.node(node, 1, "Removing: " + path )
        try:
            shutil.rmtree(path)
        except:
            print "Directory has been pre-cleared."
        
    node.parm(parm.replace('deleteHistory','historydir')).deleteAllKeyframes()
    node.parm(parm.replace('deleteHistory','historydir')).set('')             