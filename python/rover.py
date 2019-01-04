# rover.py

import sys
import signal
from init import *      # declare globals, import libraries, etc.
from OSCrover import *  # setup OSC communications
from motor import *     # set up gpio for motors

###############################################################################
# signal handling stuff
###############################################################################
def signal_handler(sig, frame):
    # exit the program cleanly.
    print 'You pressed Ctrl+C!'
    close()

def close():
    print "stopping motors..."
    drive(0, 0)                 # set motor speeds to 0
    print "stopping gpio..."
    gpio.stop()
    print "closing OSC..."
    closeOSC()
    print "Done."
    sys.exit()
    
# bind signal_handler to Ctrl-C event (SIGINT)
signal.signal(signal.SIGINT, signal_handler)

###############################################################################
# main program
###############################################################################
if __name__ == '__main__':
    i = 0 
    # test
    print "entering main loop"
    try:
        while(1):
            i = i + 1
            if i == 10: quit = 1
            print "quit = %i, i = %i, speed1=%i, speed2=i" % (quit, i, speed1, speed2) 
            if quit: 
                print "quitting main loop"
                close()
                break
            else:
                drive(speed1, speed2) 
                time.sleep(0.5)

    except Exception, err:
        sys.stderr.write("ERROR: %s\n", str(err))
        close()
