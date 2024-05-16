'''
Some threads may have a few more or less files than the rest,
because of remainder in total_files // threads

I'm leaving gui here because it is faster than the modern gui

Safe copy not working

Fix:
    closing while copying thread
    do another copy after finishing one

'''

import sys, mtcopy, newgui

# entry point
if __name__ == '__main__':
    if len(sys.argv) == 1:
        newgui.App('park', 'dark')
    else:
        print('No args plz')
