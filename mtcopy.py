# SuperFastPython.com
# copy files from one directory to another concurrently with processes in batch
from os import makedirs
from os import listdir
from os.path import join
from shutil import copy
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import sys, os
from progressbar import ProgressBar, Percentage, Bar, ETA

# copy files from source to destination
def copy_files(src_paths, dest_dir, skip):
    # process all file paths
    for src_path in src_paths:
        #print('src', src_path)
        mydest = join(dest_dir, src_path[skip:])
        #print('dst', mydest)
        # copy source file to dest file
        try:
            dest_path = copy(src_path, mydest)
        except Exception as e:
            print('bad', e)
        # report progress
        #print(f'.copied {src_path} to {dest_path}', flush=True)

# copy files from src to dest
def main(src, dest):
    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create full paths for all files we wish to copy
    srcfiles, dstfiles = list(), list()
    skip = len(src) + 1
    for root, dirs, files in os.walk(src):
        path = root.split(os.sep)
        newfolder = join(dest, root[skip:])
        makedirs(newfolder, exist_ok=True)
        for f in files:
            srcfiles.append(join(root, f))
            #dstfiles.append(join(dest, root[skip:], f))
            
    #print(len(srcfiles))
    # determine chunksize
    n_workers = 4
    chunksize = round(len(srcfiles) / n_workers)
    # create the process pool
    with ProcessPoolExecutor(n_workers) as exe:
        # split the copy operations into chunks
        for i in range(0, len(srcfiles), chunksize):
            # select a chunk of filenames
            filenames = srcfiles[i:(i + chunksize)]
            # submit the batch copy task
            try:
                _ = exe.submit(copy_files, filenames, dest, skip)
            except Exception:
                print('bad')
    print('Done')

# entry point
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no args')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])