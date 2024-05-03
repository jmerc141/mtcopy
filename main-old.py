'''
Some threads may have a few more or less files than the rest,
because of remainder in total_files // threads

I'm leaving gui here because it is faster than the modern gui

Fix:
    closing while copying thread

'''

import sys, gui

# entry point
if __name__ == '__main__':
    if len(sys.argv) == 1:
        gui.mainGui()
    else:
        print('No args plz')
