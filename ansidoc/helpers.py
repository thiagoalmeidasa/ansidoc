import os
import fnmatch
# fixme: unable to import only safe_load
# from yaml import yaml.safe_load
import yaml


def load_yml_file(fpath):
    """safe_load yaml file."""
    with open(fpath, 'r') as stream:
        return yaml.safe_load(stream)


def write_file(data, fpath):
    """write a file to disk only if content has changed."""
    if not os.path.isfile(fpath):
        with open(fpath, 'w') as f:
            f.write(data)
    else:
        with open(fpath, 'r+') as f:
            # replace content only if needed
            if data != f.read():
                f.truncate(0)
                f.seek(0)
                f.write(data)


def get_filenames(dpath):
    """Return *.{yml,json} files in given directory."""
    for file in os.listdir(dpath):
        if fnmatch.fnmatch(file, '*.json') or fnmatch.fnmatch(file, '*.yml'):
            yield (file)


def read_file(fpath):
    """
    Read a file a literaly return content.

    If file is yaml, it must skip the stream header.
    """
    with open(fpath, 'r') as f:
        # skip '---' header of yaml streams
        if os.path.splitext(fpath)[1] == ".yml":
            f.readline()

        # eat up every empty lines
        pos = f.tell()
        line = f.readline()

        while not line.strip():
            pos = f.tell()
            line = f.readline()

        # go back to non-empty line
        f.seek(pos)

        return f.read()


def read_files(dpath, verbose):
    """
    Read every files files under a given directory.

    Return a list of dictionaries. Each dictionary contains the filename
    and the file content.
    """
    if os.path.isdir(dpath):
        dfiles = []
        for f in get_filenames(dpath):
            if verbose:
                print("Reading file " + os.path.join(dpath, f))
            dfiles.append(
                {"filename": f, "content": read_file(os.path.join(dpath, f))})
        return dfiles
    else:
        return None
        if verbose:
            print(dpath + " directory doesn't exist...skipping")

# def make_doc_dir():
#     """Create docs folder inside role."""
#     docdir = path.abspath(rolepath + "/docs")

#     # make sure destination exist, if not create it
#     if not path.isdir(symlink_target):
#         mkdir(symlink_target,'755')