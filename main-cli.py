'''
Some threads may have a few more or less files than the rest,
because of remainder in total_files // threads

I'm leaving gui here because it is faster than the modern gui

Fix:
    closing while copying thread

'''

import sys, mtcopy

# entry point
if __name__ == '__main__':
    if len(sys.argv) == 4:
        source = sys.argv[1]
        destin = sys.argv[2]
        threads = sys.argv[3]
        mtcopy.init(source, destin, threads, cl=True)
    elif len(sys.argv) == 5:
        if sys.argv[4] == 'quick':
            source = sys.argv[1]
            destin = sys.argv[2]
            threads = sys.argv[3]
            mtcopy.init(source, destin, threads, cl=True, quick=True)
    else:
        print('need source destination number_of_threads')
