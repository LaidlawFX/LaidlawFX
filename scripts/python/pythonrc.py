#"""Perform tasks when houdini is launched."""
# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import sys
import random
import subprocess
import exceptions

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
    print "Running : pythonrc.py"
if hou.getenv('HOUDINI_ADMIN'): 
    startup_check()

# -----------------------------------------------------------------------------
#    Name: houVer()
#  Raises: N/A
# Returns: None
#    Desc: Prints the Houdini Version, when you have multiple installed
# -----------------------------------------------------------------------------

def houVer():

    houTypeRaw  = hou.applicationName()
    houApp      = hou.isApprentice()
    houType     = "houdiniDefault"
    addedWarning = 0

    if houTypeRaw == "houdini" and houApp == True :
        houType = "Houdini Apprentice"
        addedWarning = 1
    elif houTypeRaw == "houdini" :
        houType = "Houdini"
        addedWarning = 0
    elif houTypeRaw == "hescape" :
        houType = "Houdini Escape"
        addedWarning = 1
    elif houTypeRaw == "engine" :
        houType = "Houdini Engine"
        addedWarning = 0        

    print "Launching " + houType + " Version: " + hou.applicationVersionString()
    if addedWarning == 1 :
        print "Warning: Dynamics not accessible in this version."
    
houVer()

# -----------------------------------------------------------------------------
#    Name: houSplashScreen()
#  Raises: N/A
# Returns: None
#    Desc: Updates the Splash Screen so I know the environment is running
# -----------------------------------------------------------------------------

def houSplashScreen():
    path            = os.path.dirname(os.path.dirname(sys.argv[0]))
    splash_number   = str(random.randrange(1,10))
    splash_path     = path + '/splash/Splash_' + splash_number + '.jpg'

    #Runs the SplashScreen Code
    if os.path.isfile(splash_path) :
        #print "Updating Splash Screen Variable. You can change this in the +343 Menu."
        pipe = subprocess.Popen(['setx', 'HOUDINI_SPLASH_FILE', splash_path], shell=False)
        #pipe = subprocess.Popen(['setx', 'HOUDINI_SPLASH_MESSAGE', 'Message 1 //n Message 2'], shell=False)

houSplashScreen()

# =============================================================================
# END
# =============================================================================
# print " "
