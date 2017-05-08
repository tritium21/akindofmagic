import contextlib
import os.path
import platform

class MagicException(Exception):
    def __init__(self, message):
        super(MagicException, self).__init__(message)
        self.message = message

@contextlib.contextmanager
def extend_path(path=None):
    if path:
        oldpath = os.environ['PATH']
        os.environ['PATH'] = '{};{}'.format(str(path), os.environ['PATH'])
    yield
    if path:
        os.environ['PATH'] = oldpath

def maybe_decode(s):
    if str == bytes:
        return s
    return s.decode('utf-8')

def windows_path(filename=None):
    path = os.path.dirname(os.path.abspath(__file__))
    arch = platform.architecture()[0]
    parts = [path]
    parts.append('win64' if arch == '64bit' else 'win32')
    if filename:
        parts.append(filename)
    return os.path.join(*parts)
