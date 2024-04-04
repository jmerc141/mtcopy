'''

'''

from os import makedirs, walk
from os.path import join
from shutil import copy
import gui, os, threading, time

jobs = []
srcFiles = []
t = ''
chunksize = 0

# copy files from source to destination
def copy_files(i, src, dst):
    c = 0
    l = len(src)
    for idx in range(0, l):
        d = copy(src[idx], dst[idx])
        # set progress bar value for each thread
        gui.pbs[i]['value'] = (c / l) * 100
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

    print('Done', end)

def resetJobs():
    global jobs
    jobs = []

def threadCheck():
    global chunksize
    chunksize = round(len(srcFiles) / t)
    # check if too many threads per file
    if chunksize == 0:
        gui.log.insert('end', 'Too many threads')


# copy files from src to dest
def init(src, dest, threads: int):
    global t
    t = threads
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
    
    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create all subdirectories
    for d in dstDirs:
        makedirs(d, exist_ok=True)

    threadCheck()

    if chunksize > 0:
        # make list of threads
        n=0
        for i in range(0, len(srcFiles), chunksize):
            s = srcFiles[i:(i + chunksize)]
            d = dstFiles[i:(i + chunksize)]
            jobs.append(threading.Thread(target=copy_files, args=[n, s, d]))
            n += 1
        
    
    
        
