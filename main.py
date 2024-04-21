'''
Last thread may have a few more or less files than the rest,
because of remainder in total_files // threads
'''

import sys, mtcopy, gui, os

# entry point
if __name__ == '__main__':
    if len(sys.argv) == 1:
        gui.mainGui()
    elif len(sys.argv) == 4:
        source = sys.argv[1]
        destin = sys.argv[2]
        threads = sys.argv[3]
        mtcopy.init(source, destin, threads, cl=True)
    else:
        print('need source destination number_of_threads')
