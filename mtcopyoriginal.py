# SuperFastPython.com
# copy files from one directory to another concurrently with processes in batch
from os import makedirs
from os import listdir
from os.path import join
from shutil import copy
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import sys
from progressbar import ProgressBar, Percentage, Bar, ETA

# copy files from source to destination
def copy_files(src_paths, dest_dir):
    # process all file paths
    for src_path in src_paths:
        # copy source file to dest file
        dest_path = copy(src_path, dest_dir)
        # report progress
        print(f'.copied {src_path} to {dest_path}', flush=True)

# copy files from src to dest
def main(src, dest):
    # create the destination directory if needed
    makedirs(dest, exist_ok=True)
    # create full paths for all files we wish to copy
    files = [join(src,name) for name in listdir(src)]
    print(files)
    print(m)
    # determine chunksize
    n_workers = 4
    chunksize = round(len(files) / n_workers)
    # create the process pool
    with ProcessPoolExecutor(n_workers) as exe:
        # split the copy operations into chunks
        for i in range(0, len(files), chunksize):
            # select a chunk of filenames
            filenames = files[i:(i + chunksize)]
            # submit the batch copy task
            _ = exe.submit(copy_files, filenames, dest)
    print('Done')

# entry point
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('no args')
        sys.exit(0)
    main(sys.argv[1], sys.argv[2])