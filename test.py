"""
This script demonstrates how to create a bare-bones, fully functional
chatbot using PyAIML.
"""

import aiml
import sys
import traceback

# Create a Kernel object.
kern = aiml.Kernel()


# When loading an AIML set, you have two options: load the original
# AIML files, or load a precompiled "brain" that was created from a
# previous run. If no brain file is available, we force a reload of
# the AIML files.

force_reload = (len(sys.argv) >= 2 and sys.argv[1] == "reload")
brainLoaded = False

if not force_reload:
    # Attempt to load the brain file.  If it fails, fall back on the
    # Reload method.
    # noinspection PyBroadException
    try:
        # The optional branFile argument specifies a brain file to load.
        kern.bootstrap(brain_file="standard.brn")
        brainLoaded = True
    except Exception:
        print("Error loading saved brain file:")
        traceback.print_exc()
        forceReload = True

if force_reload:
    print("Reloading.")
    # Use the Kernel's bootstrap() method to initialize the Kernel. The
    # optional learnFiles argument is a file (or list of files) to load.
    # The optional commands argument is a command (or list of commands)
    # to run after the files are loaded.
    kern.bootstrap(learn="std-startup.xml", commands="load aiml b")
    brainLoaded = True
    # Now that we've loaded the brain, save it to speed things up for
    # next time.
    kern.save_brain("standard.brn")

assert brainLoaded, "The brain file was not loaded."


# Enter the main input/output loop.
print("\nINTERACTIVE MODE (ctrl-c to exit)")
while True:
    try:
        print(kern.respond(input("> ")))
    except KeyboardInterrupt:
        break
