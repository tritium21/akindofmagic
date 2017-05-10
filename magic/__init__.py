"""
magic is a wrapper around the libmagic file identification library.

See README for more information.

Usage:

>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
>>> magic.from_file("testdata/test.pdf", mime=True)
'application/pdf'
>>> magic.from_buffer(open("testdata/test.pdf").read(1024))
'PDF document, version 1.2'
>>>


"""

import sys
import threading

from magic import libmagic as lm
from magic.utility import maybe_decode, MagicException, windows_path
from pkg_resources import get_distribution

__version__ = get_distribution('akindofmagic').version

class Magic:
    """
    Magic is a wrapper around the libmagic C library.

    """

    def __init__(
            self,
            mime=False,
            magic_file=None,
            mime_encoding=False,
            keep_going=False,
            uncompress=False
        ):
        """
        Create a new libmagic wrapper.

        mime - if True, mimetypes are returned instead of textual descriptions
        mime_encoding - if True, codec is returned
        magic_file - use a mime database other than the system default
        keep_going - don't stop at the first match, keep going
        uncompress - Try to look inside compressed files.
        """
        self.flags = lm.MAGIC_NONE
        if mime:
            self.flags |= lm.MAGIC_MIME
        if mime_encoding:
            self.flags |= lm.MAGIC_MIME_ENCODING
        if keep_going:
            self.flags |= lm.MAGIC_CONTINUE

        if uncompress:
            self.flags |= lm.MAGIC_COMPRESS

        self.cookie = lm.magic_open(self.flags)
        self.lock = threading.Lock()

        if not magic_file and sys.platform == 'win32':
            magic_file = windows_path('magic.mgc')
        lm.magic_load(self.cookie, magic_file)

    def from_buffer(self, buf):
        """
        Identify the contents of `buf`
        """
        with self.lock:  #pylint: disable-msg=not-context-manager
            try:
                return maybe_decode(lm.magic_buffer(self.cookie, buf))
            except MagicException as e:
                return self._handle509Bug(e)

    def from_file(self, filename):
        # raise FileNotFoundException or IOError if the file does not exist
        with open(filename):
            pass
        with self.lock:  #pylint: disable-msg=not-context-manager
            try:
                return maybe_decode(lm.magic_file(self.cookie, filename))
            except MagicException as e:
                return self._handle509Bug(e)

    def _handle509Bug(self, e):
        # libmagic 5.09 has a bug where it might fail to identify the
        # mimetype of a file and returns null from magic_file (and
        # likely _buffer), but also does not return an error message.
        if e.message is None and (self.flags & lm.MAGIC_MIME):
            return "application/octet-stream"
        else:
            raise e

    def __del__(self):
        # no _thread_check here because there can be no other
        # references to this object at this point.

        # during shutdown magic_close may have been cleared already so
        # make sure it exists before using it.

        # the self.cookie check should be unnecessary and was an
        # incorrect fix for a threading problem, however I'm leaving
        # it in because it's harmless and I'm slightly afraid to
        # remove it.
        if self.cookie and lm.magic_close:
            lm.magic_close(self.cookie)
            self.cookie = None

_instances = {}

def _get_magic_type(mime):
    i = _instances.get(mime)
    if i is None:
        i = _instances[mime] = Magic(mime=mime)
    return i

def from_file(filename, mime=False):
    """"
    Accepts a filename and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_file("testdata/test.pdf", mime=True)
    'application/pdf'
    """
    m = _get_magic_type(mime)
    return m.from_file(filename)

def from_buffer(buffer, mime=False):
    """
    Accepts a binary string and returns the detected filetype.  Return
    value is the mimetype if mime=True, otherwise a human readable
    name.

    >>> magic.from_buffer(open("testdata/test.pdf").read(1024))
    'PDF document, version 1.2'
    """
    m = _get_magic_type(mime)
    return m.from_buffer(buffer)
