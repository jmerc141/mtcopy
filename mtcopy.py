'''

'''

from os import makedirs, walk
from os.path import join
from shutil import copy
import gui, os, threading, time, copyprog

cli = False

# List of threads
jobs = []
# List of source files with full path to be copied
srcFiles = []
# List of destination full paths
dstFiles = []
# Number of threads
t = ''
# Number of chunks files will be broken into
chunksize = 0


'''
    Copy files from source to destination, uses gui progressbars
    i: index of which progressbar to update
    src: chunk of files per thread to copy
    dst: chunk of destination files
'''
def copy_files(i, src, dst):
    c = 0
    length = len(src)-1
    print(i, length)
    for idx in range(0, len(src)):
        d = copy(src[idx], dst[idx])
        # set progress bar value for each thread
        # number of threads and i should be the same
        # else IndexError
        gui.pbs[i]['value'] = (c / length) * 100
        gui.lbls[i].set(os.path.basename(src[idx]))
        c += 1


'''
    Copy files from source to destination, uses cli progressbars
    i: index of which progressbar to update
    src: chunk of files per thread to copy
    dst: chunk of destination files
'''
def copy_cli(i, src, dst):
    c = 0
    length = len(src)-1
    #print(i, length)
    for idx in range(0, len(src)):
        d = copy(src[idx], dst[idx])
        d = copyprog.copy_progress(i, c, length, os.path.basename(src[idx]))
        c += 1


'''
    Start all copy jobs in n threads and
    wait for all to finish, clears jobs and srcFiles lists
'''
def startCopy():
    st = time.perf_counter()
    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    end = time.perf_counter() - st
    
    # reset jobs list
    lenPrevJob = len(jobs)
    jobs.clear()
    srcFiles.clear()
    if cli == False:
        gui.writeLog(f'Done in {round(end, 2)}s')
    else:
        print('\n' * lenPrevJob + f'\033[KDone in {round(end, 2)}s')
        print(lenPrevJob)
    
'''
    Splits files in sourcefile list into semi-even chunks which 
    are assigned to a thread.
    If there are remainders files, they are assigned from first thread to last
'''
def createJobs(func, remainder):
    s = []
    d = []
    remidx = -1
    for th in range(t):
        s = srcFiles[th * chunksize:(th+1) * chunksize]
        d = dstFiles[th * chunksize:(th+1) * chunksize]
        if remainder > 0:
            s.append(srcFiles[remidx])
            d.append(dstFiles[remidx])
            remainder -= 1
            remidx -= 1
        jobs.append(threading.Thread(target=func, args=[th, s, d]))


'''
    Checks for valid paths, walks through source directory and
    populates the srcFiles and dstFiles lists with full paths of
    files to copy. Then calculates chunksize (number of files per thread)
    and creates directory structure. Finally creates jobs list of threads to
    execute with corresponding file chunks
'''
def init(src, dest, threads: int, cl=False):
    global t
    global srcFiles
    global dstFiles
    global cli
    global chunksize

    srcFiles = []
    t = int(threads)
    cli = cl
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
    chunksize = len(srcFiles) // t
    print(chunksize)

    # check if too many threads per file
    if chunksize == 0:
        return 0

    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create all subdirectories
    for d in dstDirs:
        makedirs(d, exist_ok=True)

    if chunksize > 0:
        if cli == False:
            createJobs(copy_files, rem)
        else:
            os.system('cls||clear')
            createJobs(copy_cli, rem)
        startCopy()
        
    return chunksize

