'''

'''

from os import makedirs, walk
from os.path import join
from shutil import copy
import gui, os, threading, time, copyprog

jobs = []
srcFiles = []
t = ''
chunksize = 0


# copy files from source to destination
def copy_files(i, src, dst, length):
    c = 0
    print(i, length)
    for idx in range(0, len(src)):
        d = copy(src[idx], dst[idx])
        # set progress bar value for each thread
        try:
            gui.pbs[i]['value'] = (c / length) * 100
            gui.lbls[i].set(os.path.basename(src[idx]))
        except IndexError as ie:
            print('Extra thread but no corresponding gui component')
            pass
        c += 1


def copy_cli(i, src, dst):
    c = 0
    l = len(src)
    for idx in range(0,l):
        d = copyprog.copy_with_progress(c, i, src, dst)
        c += 1


def startCopy():
    st = time.perf_counter()
    for i in range(0, len(jobs)):
        jobs[i].start()

    for j in jobs:
        j.join()

    end = time.perf_counter() - st
    
    # reset jobs list
    jobs.clear()
    srcFiles.clear()
    gui.writeLog(f'Done in {round(end, 2)}s')
    

# copy files from src to dest
def init(src, dest, threads: int):
    global t
    global srcFiles
    srcFiles = []
    t = int(threads)
    if not os.path.isdir(src) and not os.path.isdir(dest):
        raise ValueError('Path must be folder')
    d = os.path.abspath(dest)
    s = os.path.abspath(src)

    dstFiles = []
    dstDirs = []

    nroot = ''
    # walk through all files recursively
    
    for root, dirs, files in walk(s):
        # get substring of subfolders
        nroot = root[len(s):]
        for f in files:
            # make list of all source files (absolute paths)
            srcFiles.append(join(root, f))
            if len(nroot) == 0:
                dstFiles.append(join(dest, f))
            else:
                dstFiles.append(dest + join(nroot, f))
            
        for d in dirs:
            # set list of destination directories
            dstDirs.append(dest + '\\' + join(nroot, d))
    
    # The most rem will be is t-1
    rem = len(srcFiles) % t
    #if rem > 0:
        # split files among t-1 threads and use last thread for remainder
    #    rem = len(srcFiles) % (t-1)
    #    chunksize = len(srcFiles) // (t-1)
    #else:
        # split files evenly
    chunksize = len(srcFiles) // t

    print(len(srcFiles), chunksize, rem)
    # check if too many threads per file
    if chunksize == 0:
        return 0

    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create all subdirectories
    for d in dstDirs:
        makedirs(d, exist_ok=True)


    if chunksize > 0:
        # make list of threads to copy files
        n=0
        s = []
        d = []
        for i in range(0, len(srcFiles), chunksize+rem):
            print(i, i+chunksize)
            s = srcFiles[i:(i + chunksize)]
            d = dstFiles[i:(i + chunksize)]
            jobs.append(threading.Thread(target=copy_files, args=[n, s, d, len(s)-1]))
            n += 1
        
    print(len(jobs))
    return chunksize

