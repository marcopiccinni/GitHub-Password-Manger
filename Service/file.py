import os.path as op
import os
import fnmatch
from Service.cypher import Cypher
import yaml


def _filter(paths, includes=(), excludes=()):
    matches = []
    for path in paths:
        append = True
        if includes:
            for include in includes:
                if op.isdir(path) or fnmatch.fnmatch(op.normpath(path), op.normpath(include)):
                    append = True
                    break
                else:
                    append = False
        if excludes:
            for exclude in excludes:
                if (op.isdir(path) and op.normpath(path) == op.normpath(exclude)) \
                        or (fnmatch.fnmatch(op.normpath(path), op.normpath(exclude))):
                    append = False
                    break
        if append:
            matches.append(path)
    return matches


def list_file_dir(rootdir=os.getcwd(), include=('*',), exclude=('*/.git/*',)):
    _tmp_file_list = []
    for root, subFolders, files in os.walk(rootdir, ):
        for file in files:
            _tmp_file_list.append(op.normpath(op.join(root, file)))
    return _filter(_tmp_file_list, includes=include, excludes=exclude)


# return the data structure starting from a clear file or a clear data
def load_clear(filename=None, data=None):
    if filename:
        with open(filename) as stream:
            return yaml.safe_load(stream)
    if data:
        return yaml.safe_load(data)


# return the string in yaml format in a file or in a variable
def dump_clear(data, filename=None):
    if filename:
        with open(filename, 'w') as stream:
            yaml.safe_dump(data, stream)
        return
    return yaml.safe_dump(data)


def load_crypt(password, file_source=None):
    if file_source:
        c = Cypher(password, secure_file=file_source)
        c_message = c.file_decrypt()
        return load_clear(data=c_message)
    return None


def dump_crypt(password, data_source=None, file_source=None):
    if file_source:
        c = Cypher(password, clear_file=file_source)
        c.file_encrypt(True)
        return True
    if data_source:
        c = Cypher(password)
        c.encrypt(dump_clear(data_source), True)
        return True
    return False
