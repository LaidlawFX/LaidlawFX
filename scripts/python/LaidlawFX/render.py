# =============================================================================
# IMPORTS
# =============================================================================

import hou
import inspect
import exceptions
import os
import datetime
from shutil     import copyfile
from LaidlawFX  import log
from LaidlawFX  import hq
from LaidlawFX  import path
from LaidlawFX  import renderscripts
from LaidlawFX  import oppath
from LaidlawFX  import color
from LaidlawFX  import queue
from LaidlawFX  import fbx

# =============================================================================
# FUNCTIONS
# =============================================================================                
       
# -----------------------------------------------------------------------------
#    Name: execute_farm(node, localnode)
#  Raises: N/A
# Returns: None
#    Desc: Series of commands that allow you to fire and forget.
# -----------------------------------------------------------------------------

def execute_farm(node, localnode=None):
    if not localnode :
        localnode = node
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:        
        begTime = datetime.datetime.now()
        log.node(node, 2, "\n Begin Time of Total Export: " + str(begTime)+ " \n") 
        if hq.hq_hfs(node)[1] :
            if node.parent().parm("file_type") :
                ext = node.parent().evalParm("file_type")
                if ext == 'md' or ext == 'ip' :
                    log.node(node, 0, "Not rendering to farm as your image type is set to Mplay.")
                    return  

            renderscripts.pre(node)

            log.node(node, 2, "Rendering Node : " +str(node.path()))

            init(node)

            list_dir = []
            list_dir.append(path.hq_project_path(node))           
            if node.parm("hq_hip_action") :                          
                if node.evalParm("hq_hip_action") == "use_target_hip" :
                    list_dir.append(os.path.dirname(path.hq_hip(node)))
                elif node.evalParm("hq_hip_action") == "use_ifd" :
                    list_dir.append(os.path.dirname(path.hq_input_ifd(node)))            
            if node.parm("hq_makeifds") :
                if node.evalParm("hq_makeifds") :
                    list_dir.append(os.path.dirname(path.hq_outputifd(node)))
            if localnode :
                ntype   = localnode.type()
                name    = ntype.nameComponents()[2]
                if name == 'VFX_geometry' :
                    list_dir.append(os.path.dirname(path.sopoutput(node)))                    
                if name == 'VFX_dop' :
                    list_dir.append(os.path.dirname(path.dopoutput(node))) 
                if name == 'VFX_comp' :
                    list_dir.append(os.path.dirname(path.copoutput(node, localnode)))
                if name == 'VFX_opengl' :
                    list_dir.append(os.path.dirname(path.picture(node, localnode)))                                           
                if name == 'VFX_ifd' :
                    list_dir.append(os.path.dirname(path.vm_picture(node, localnode)))
                    if localnode.parm("soho_outputmode") :
                        if localnode.evalParm("soho_outputmode") :
                            list_dir.append(os.path.dirname(path.soho_diskfile(node)))                    
                    if localnode.parm("vm_inlinestorage") :
                        if not localnode.evalParm("vm_inlinestorage") :
                            list_dir.append(os.path.dirname(path.vm_tmpsharedstorage(node)))
                            list_dir.append(os.path.dirname(path.vm_tmplocalstorage(node))) 
                    if localnode.parm("vm_deepresolver") :
                        if localnode.evalParm("vm_deepresolver") == 'shadow' :
                            list_dir.append(os.path.dirname(path.vm_dsmfilename(node)))
                        if localnode.evalParm("vm_deepresolver") == 'camera' :                            
                            list_dir.append(os.path.dirname(path.vm_dcmfilename(node)))
            #relying on soho_mkpath for Extra Image Planes to make the directories
            #vm_filename_plane(hq_node,node,parm)

            makedirs(node, list_dir)

            save(node, 'farm')

            #Print the environment at the time of processing
            env_path = str(path.hq_project_path(node) + '/houdini_environment.json')
            log.node(node, 2, "Houdini Environemt Log : \n" +env_path)            
            log.env(node,env_path)

            if oppath.node_sim(node) :
                log.node(node, 2, "Submitting Simulation")
                node.node("hq_sim/hq_sim").parm('execute').pressButton()
            else :
                log.node(node, 2, "Submitting Renders")
                node.node("hq_render").parm('execute').pressButton()
        
            renderscripts.post(node) 
            
        else:
            hou.ui.displayMessage("Not deployed to the farm due to version mismatch.", title="Version Mismatch")
            
        log.node(node, 2, "Done with all Processing! \n")          

        #TimeCheck
        endTime = datetime.datetime.now()
        tolTime = endTime - begTime
        log.node(node, 2, "End Time of Total Export: " + str(endTime) )
        log.node(node, 2, "Total Time of  Export:    " + str(tolTime) + " \n")        
              
        
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return

   
       
# -----------------------------------------------------------------------------
#    Name: execute_local(node, node_type)
#  Raises: N/A
# Returns: None
#    Desc: Series of commands that allow you to fire and forget.
# -----------------------------------------------------------------------------

def execute_local(node, node_type):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        begTime = datetime.datetime.now()
        log.node(node, 2, "\nBegin Time of Total Export: " + str(begTime)+ " \n")       
        
        renderscripts.pre(node)

        init(node)

        if node_type == 'first':
            log.node(node, 1, "Render first frame only.")
            execute_first(node)
        elif node_type == 'local':
            log.node(node, 1, "Render Local.")
        elif node_type == 'back':
            log.node(node, 1, "Render Local in Background.")

        list_dir = []
        list_dir.append(os.path.dirname(path.file(node))) 
        makedirs(node, list_dir)


        node.parm('loadfromdisk').deleteAllKeyframes()
        node.parm('loadfromdisk').set(1)
        node.parm('ver').deleteAllKeyframes()
        node.parm('ver').set(hou.getenv("HIPNAME",'default-0001'))
        if node.evalParm("f1") != node.evalParm("f2") :
            node.parm('frame').deleteAllKeyframes()
            node.parm('frame').setExpression('$FF')

        save(node)

        file_type = node.evalParm("file_type")

        if file_type == '.abc' :
            log.node(node, 1, "Caching ABC: " + str(nodePath))
            node.node("AlembicCaching").parm('execute').pressButton()
            node.node("import_alembic").parm('reload').pressButton()  
        if file_type == '.fbx' :
            log.node(node, 1, "Caching FBX: " + str(nodePath))
            fbx.exexcute(node)
            node.node("import_fbx").parm('reload').pressButton()               

        if node_type == 'local' or node_type == 'first':
            log.node(node, 1, "Caching Local: " + str(nodePath))
            node.node("ROPs/geometry").parm('execute_local').pressButton()
            node.node("read_back").parm('reload').pressButton()           
        if node_type == 'back'  :
            log.node(node, 1, "Caching Local in Background: " + str(nodePath))
            node.node("ROPs/geometry").parm('executebackground').pressButton()
            node.node("read_back").parm('reload').pressButton()
                           
        if node.evalParm("mantra_archive") and file_type in '.bgeo' :
            log.node(node, 1, "Caching Mantra Archive: " + str(nodePath))
            node.node("ROPs/MantraArchive").parm('execute').pressButton()
            node.node("read_back").parm('reload').pressButton()

        if node.evalParm("history_auto") :
            history.update(node)

        if node.evalParm("enable_queue") and not node.evalParm("que") :
            queue.Execute(node)                          

        color.change(node)                       

        renderscripts.post(node) 
            
        log.node(node, 1, "Done with all Processing! \n")          

        #TimeCheck
        endTime = datetime.datetime.now()
        tolTime = endTime - begTime
        log.node(node, 2, "End Time of Total Export: " + str(endTime) )
        log.node(node, 2, "Total Time of  Export:    " + str(tolTime) + " \n")        
              
        
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return

# -----------------------------------------------------------------------------
#    Name: execute_first(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets the frame to one so you can write and read a model
# -----------------------------------------------------------------------------

def execute_first(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        one     = 1
        node.parm('frame').deleteAllKeyframes()
        node.parm('f1').deleteAllKeyframes()
        node.parm('f2').deleteAllKeyframes()
        node.parm('f3').deleteAllKeyframes()
        node.parm('frame').set(one)
        node.parm('f1').set(one)
        node.parm('f2').set(one)
        node.parm('f3').set(one)
        
    except (KeyboardInterrupt, SystemExit):
        print("Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return 

# -----------------------------------------------------------------------------
#    Name: init(node)
#  Raises: N/A
# Returns: None
#    Desc: Initialize hip variables
# -----------------------------------------------------------------------------        
        
def init(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:        
        hou.hscript('setenv ASSET = '+path.asset(node))
        hou.hscript('setenv COMPONENT = '+path.component(node))
        hou.hscript('setenv JOB = '+path.hq_project_path(node).replace('\\','/'))
        #hou.putenv("ASSET",     path.asset(node))
        #hou.putenv("COMPONENT", path.component(node)) 
        #hou.putenv("JOB",       path.hq_project_path(node))         
               
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return          
        
        
# -----------------------------------------------------------------------------
#    Name: Directories(node)
#  Raises: N/A
# Returns: None
#    Desc: Enable color script, Changes the node color to a render color, if already rendered brightens it up
# -----------------------------------------------------------------------------        
        
def makedirs(node, list_dir):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:        
        log.node(node, 2, "Making Directories.")   
            
        for path in list_dir :
            log.node(node, 2, path)
            if not os.path.exists(path):
                os.makedirs(path)

            
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return       
        
# -----------------------------------------------------------------------------
#    Name: save(node)
#  Raises: N/A
# Returns: None
#    Desc: If the save scene file is toggled on it will save the scene before executing.
# -----------------------------------------------------------------------------        
        
def save(node, farm=None):
    nodePath        = node.path()
    function        = inspect.stack()[0][3]
    try:       
        hiplocal    = os.path.abspath(hou.hipFile.name())
        hipfarm     = path.hq_hip(node)                      

        log.node(node, 1, "Saving your local hip.")
        log.node(node, 2, hiplocal)
        hou.hipFile.save()
        log.node(node, 1, "Backing up your local hip.")        
        hou.hipFile.saveAsBackup()
        if farm :         
            log.node(node, 1, "Copying your hip to the farm.")
            log.node(node, 2, hipfarm)        
            copyfile(hiplocal, hipfarm)        
        
    except (KeyboardInterrupt, SystemExit):
        log.node(node, 1, "Interrupt requested of "+function+" for "+nodePath+"...exiting")
        return


        
