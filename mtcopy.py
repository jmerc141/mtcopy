'''

'''

from os import makedirs, walk
from os.path import join
from shutil import copy
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import copyprog, os, threading


# copy files from source to destination
def copy_files(src, dst):
    
    for idx in range(0, len(src), 1):
        #f_dest = dest_dir + src_path[len(self.sourc):]
        #d = copy(src[idx], dst[idx])
        pass
        

        #print(f'copied {src[idx]} to {dst[idx]}')


# copy files from src to dest
def main(src, dest, threads: int):
    d = os.path.abspath(dest)
    s = os.path.abspath(src)

    srcFiles = []
    dstFiles = []
    dstDirs = []

    nroot = ''
    # walk through all files recursively
    
    for root, dirs, files in walk(s):
        for f in files:
            nroot = root[len(s):]
            # make list of all source files (absolute paths)
            srcFiles.append(join(root, f))
            dstFiles.append(join(dest, nroot, f))
        for d in dirs:
            # get substring of subfolders
            nroot = root[len(s):]
            # set list of destination directories
            dstDirs.append(dest + '\\' + join(nroot, d))
    

    #print(srcFiles, dstFiles)
    
    # trianlge number (as_completed returns this many times)
    #tri = ((n_workers**2 + n_workers) / 2) + 5
    # determine chunksize
    chunksize = round(len(srcFiles) / threads)
    # check if too many threads per file
    if chunksize == 0:
        print('Too many threads')
        return
    
    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create all subdirectories
    for d in dstDirs:
        makedirs(d, exist_ok=True)

    jobs = []

    c=0.
    '''
    try:
        
        # create the process pool
        with ThreadPoolExecutor(threads) as exe:
            # split the copy operations into chunks
            for i in range(0, len(srcFiles), chunksize):
                # select a chunk of filenames
                filenames = srcFiles[i:(i + chunksize)]
                # submit the batch copy task
                jobs.append(exe.submit(copy_files, filenames, dest))
                for j in as_completed(jobs):
                    #print('\r', copyprog.progress_percentage(100.*c/len(srcFiles), width=50), end='')
                    print(j)
                    c+=1
                    print(c, i, len(filenames))
    except Exception as e:
        print('Error mid copy', e)
    '''
    print(dstFiles)
    lst = []
    for i in range(0, len(srcFiles), chunksize):
        s = srcFiles[i:(i + chunksize)]
        d = dstFiles[i:(i + chunksize)]
        lst.append(threading.Thread(target=copy_files, args=[s, d]))


    #len(fnames) is 4
    # make list of threads and bind to progressbar somehow
    
    
    lst[0].start()
    print('1 start')
    lst[0].join()

    print('Done')
        
