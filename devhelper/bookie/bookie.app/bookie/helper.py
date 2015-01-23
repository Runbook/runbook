import os
import errno

# Thanks to tzot ( http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python )
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
