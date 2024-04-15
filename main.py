'''
Because number of files mod number of threads is not 0,
an extra thread may be neccasary to copy up to (threads - 1)
extra files
If last (threads - 1) files are big and there is a remainder,
they will be copied in the hidden extra thread which may take a
while

'''

import sys, mtcopy, gui

# entry point
if __name__ == '__main__':
    if len(sys.argv) == 1:
        gui.mainGui()
    elif len(sys.argv) == 4:
        source = sys.argv[1]
        destin = sys.argv[2]
        threads = sys.argv[3]

        mtcopy.init(source, destin, threads)
        mtcopy.copy_cli()