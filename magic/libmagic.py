import ctypes
import ctypes.util
from ctypes import c_char_p, c_int, c_size_t, c_void_p
import glob
import os
import os.path
import sys

from magic.utility import windows_path, extend_path, MagicException

if sys.version_info[0] >= 3:
    unicode = str

def find_magic():
    dll = (
        ctypes.util.find_library('magic') or
        ctypes.util.find_library('magic1') or
        ctypes.util.find_library('cygmagic-1')
    )
    if dll:
        return ctypes.CDLL(dll)
    library_path = []
    system_path = None
    _platform = sys.platform
    if _platform == 'win32':
        lp = windows_path()
        if os.path.exists(lp):
            system_path = lp
            library_path = ['magic1.dll']
    elif _platform == 'cygwin':
        library_path = ['cygmagic-1.dll']
    elif _platform == 'darwin':
        library_path = [
            '/opt/local/lib/libmagic.dylib',
            '/usr/local/lib/libmagic.dylib',
        ]
        library_path.extend(
            glob.glob('/usr/local/Cellar/libmagic/*/lib/libmagic.dylib')
        )
    elif _platform.startswith('linux'):
        library_path = ['libmagic.so.1']
    if not library_path:
        raise ImportError("Platform not supported")
    for dll in library_path:
        try:
            with extend_path(system_path):
                return ctypes.CDLL(dll)
        except OSError:
            pass
    raise ImportError('failed to find libmagic.  Check your installation')

libmagic = find_magic()


magic_t = ctypes.c_void_p

def errorcheck_null(result, _, args):
    if result is None:
        err = magic_error(args[0])
        raise MagicException(err)
    else:
        return result

def errorcheck_negative_one(result, _, args):
    if result is -1:
        err = magic_error(args[0])
        raise MagicException(err)
    else:
        return result

def coerce_filename(filename):
    if filename is None:
        return None
    is_unicode = isinstance(filename, unicode)
    if is_unicode:
        return filename.encode('utf-8')
    return filename

magic_open = libmagic.magic_open
magic_open.restype = magic_t
magic_open.argtypes = [c_int]

magic_close = libmagic.magic_close
magic_close.restype = None
magic_close.argtypes = [magic_t]

magic_error = libmagic.magic_error
magic_error.restype = c_char_p
magic_error.argtypes = [magic_t]

magic_errno = libmagic.magic_errno
magic_errno.restype = c_int
magic_errno.argtypes = [magic_t]

_magic_file = libmagic.magic_file
_magic_file.restype = c_char_p
_magic_file.argtypes = [magic_t, c_char_p]
_magic_file.errcheck = errorcheck_null

def magic_file(cookie, filename):
    return _magic_file(cookie, coerce_filename(filename))

_magic_buffer = libmagic.magic_buffer
_magic_buffer.restype = c_char_p
_magic_buffer.argtypes = [magic_t, c_void_p, c_size_t]
_magic_buffer.errcheck = errorcheck_null

def magic_buffer(cookie, buf):
    return _magic_buffer(cookie, buf, len(buf))


_magic_load = libmagic.magic_load
_magic_load.restype = c_int
_magic_load.argtypes = [magic_t, c_char_p]
_magic_load.errcheck = errorcheck_negative_one

def magic_load(cookie, filename):
    return _magic_load(cookie, coerce_filename(filename))

magic_setflags = libmagic.magic_setflags
magic_setflags.restype = c_int
magic_setflags.argtypes = [magic_t, c_int]

magic_check = libmagic.magic_check
magic_check.restype = c_int
magic_check.argtypes = [magic_t, c_char_p]

magic_compile = libmagic.magic_compile
magic_compile.restype = c_int
magic_compile.argtypes = [magic_t, c_char_p]



MAGIC_NONE = 0x000000 # No flags
MAGIC_DEBUG = 0x000001 # Turn on debugging
MAGIC_SYMLINK = 0x000002 # Follow symlinks
MAGIC_COMPRESS = 0x000004 # Check inside compressed files
MAGIC_DEVICES = 0x000008 # Look at the contents of devices
MAGIC_MIME = 0x000010 # Return a mime string
MAGIC_MIME_ENCODING = 0x000400 # Return the MIME encoding
MAGIC_CONTINUE = 0x000020 # Return all matches
MAGIC_CHECK = 0x000040 # Print warnings to stderr
MAGIC_PRESERVE_ATIME = 0x000080 # Restore access time on exit
MAGIC_RAW = 0x000100 # Don't translate unprintable chars
MAGIC_ERROR = 0x000200 # Handle ENOENT etc as real errors

MAGIC_NO_CHECK_COMPRESS = 0x001000 # Don't check for compressed files
MAGIC_NO_CHECK_TAR = 0x002000 # Don't check for tar files
MAGIC_NO_CHECK_SOFT = 0x004000 # Don't check magic entries
MAGIC_NO_CHECK_APPTYPE = 0x008000 # Don't check application type
MAGIC_NO_CHECK_ELF = 0x010000 # Don't check for elf details
MAGIC_NO_CHECK_ASCII = 0x020000 # Don't check for ascii files
MAGIC_NO_CHECK_TROFF = 0x040000 # Don't check ascii/troff
MAGIC_NO_CHECK_FORTRAN = 0x080000 # Don't check ascii/fortran
MAGIC_NO_CHECK_TOKENS = 0x100000 # Don't check ascii/tokens
