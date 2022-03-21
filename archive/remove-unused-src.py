import os.path
import glob
import shutil

from fnmatch import fnmatch

path_src = r'X:\97584\linux-3.3-3.7\linux'
#path_src = r'X:\97584\linux-3.3-3.7\linux\drivers\mtd'

def generate_dest_path(src):
    if os.path.exists(src) and os.path.isdir(src):
        dest = os.path.join(os.path.dirname(src), os.path.basename(src) + '-unused')
        if not os.path.exists(dest):
            os.mkdir(dest)
    else:
        print('generate_dest path error!')
        dest = ''
    return dest

def get_subdir_list(path):
    dirs = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    return dirs

def get_file_list(path, pattern):
    files = [item for item in os.listdir(path) if fnmatch(item, pattern)]
    return files

def process_dir(src, dest, pat1, pat2):
    print(src)
    # check dest dir
    if not os.path.exists(dest):
        os.mkdir(dest)

    # check files
    objs = get_file_list(src, pat1)
    #print(objs)

    # convert to '.c' files
    objs_src = [os.path.splitext(name)[0]+os.path.splitext(pat2)[1] for name in objs]
    #print(objs_src)

    all_src = get_file_list(src, pat2)
    #print(all_src)

    unused_src = [file for file in all_src if file not in objs_src]
    #print(unused_src)

    for file in unused_src:
        # new file name
        file1 = os.path.join(src, file)
        file2 = os.path.join(dest, file)

        # copy file1 to file2
        if os.path.exists(file1) and os.path.isfile(file1):
            #action = 'cp -f %s %s' % (file1, file2)
            #print(action)
            #print('%s -> %s' % (file1, file2))
            #shutil.copy2(file1, file2)
            shutil.move(file1, file2)

    # check sub dirs
    subdirs = get_subdir_list(src)

    for dir in subdirs:
        src_path = os.path.join(src, dir)
        dest_path = os.path.join(dest, dir)
        if os.path.islink(src_path) or os.path.ismount(src_path):
            pass
        else:
            process_dir(src_path, dest_path, pat1, pat2)

if __name__ == '__main__':
    dest = generate_dest_path(path_src)
    print('dest:', dest)

    process_dir(path_src, dest, '*.o', '*.c')

    print('done!')