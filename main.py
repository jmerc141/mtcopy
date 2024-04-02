'''
source / dest must be plain not ".\dir\"
progress bar is not finished
not sure if actually multithread because of as_completed,
'''

import sys, mtcopy, gui

# entry point
if __name__ == '__main__':
    if len(sys.argv) < 2:
        gui.mainGui()

        #g = mtcopy.MtCopy()
        #g.mainGui()
        #sys.exit(0)
    elif len(sys.argv) == 2:
        m = mtcopy.MtCopy()
        m.main(sys.argv[1], sys.argv[2])