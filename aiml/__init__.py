import os
import sys
import traceback


# The Kernel class is the only class most implementations should need.
from .kernel import Kernel

__all__ = [
    'Kernel',
    'main',
    'USAGE'
]


USAGE = """
Usage:
    python -m aiml [BRAIN_PATH] [OPTIONS]
    
BRAIN_PATH  
    The path to the .brn "brain file" where the compiled AIML is stored.

-r 
--reset
    Reset the "brain file".
    
-n
--no-std
    Do not automatically load the standard AIML rules.

""".strip()


def main():
    """
    This script demonstrates how to create a bare-bones, fully functional
    chatbot using PyAIML.
    """

    # Create a Kernel object.
    kern = Kernel()

    # When loading an AIML set, you have two options: load the original
    # AIML files, or load a precompiled "brain" that was created from a
    # previous run. If no brain file is available, we force a reload of
    # the AIML files.

    brain_path = None
    reset = False
    no_std = False
    for arg in sys.argv[1:]:
        if arg in ('-r', '--reset'):
            reset = True
        elif arg in ('-n', '--no-std'):
            no_std = True
        elif brain_path is None:
            brain_path = arg
            if not brain_path.endswith('.brn'):
                brain_path += '.brn'
        else:
            print("Unexpected argument: %s" % arg)
            print(USAGE)
            return 1

    if brain_path is None:
        brain_path = os.path.expanduser('~/.aiml/default.brn')

    if not os.path.isfile(brain_path):
        reset = True

    brain_loaded = False

    if not reset:
        # Attempt to load the brain file.  If it fails, fall back on the
        # Reload method.
        # noinspection PyBroadException
        try:
            # The optional branFile argument specifies a brain file to load.
            kern.bootstrap(brainFile=brain_path)
            brain_loaded = True
        except Exception:
            print("Error loading saved brain file:")
            traceback.print_exc()
            reset = True

    if reset:
        print("Resetting.")
        # Use the Kernel's bootstrap() method to initialize the Kernel. The
        # optional learnFiles argument is a file (or list of files) to load.
        # The optional commands argument is a command (or list of commands)
        # to run after the files are loaded.
        if no_std:
            kern.bootstrap(commands=())
        else:
            kern.bootstrap(commands="load std aiml")
        brain_loaded = True
        # Now that we've loaded the brain, save it to speed things up for
        # next time.
        kern.saveBrain(brain_path)

    assert brain_loaded, "The brain file was not loaded."

    # Enter the main input/output loop.
    print("\nINTERACTIVE MODE (ctrl-c to exit)")
    while True:
        try:
            print(kern.respond(input("> ")))
        except KeyboardInterrupt:
            break

    kern.saveBrain(brain_path)

    return 0
