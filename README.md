# akindofmagic

[![Build status](https://ci.appveyor.com/api/projects/status/7yadfn965up6jmqb?svg=true)](https://ci.appveyor.com/project/tritium21/akindofmagic)
[![Build Status](https://travis-ci.org/tritium21/akindofmagic.svg?branch=master)](https://travis-ci.org/tritium21/akindofmagic)

akindofmagic (fork of python-magic) is a python interface to the libmagic file type
identification library.  libmagic identifies file types by checking
their headers according to a predefined list of file types. This
functionality is exposed to the command line by the Unix command
`file`.

## Usage

```python
>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
>>> magic.from_buffer(open("testdata/test.pdf").read(1024))
'PDF document, version 1.2'
>>> magic.from_file("testdata/test.pdf", mime=True)
'application/pdf'
```

There is also a `Magic` class that provides more direct control,
including overriding the magic database file and turning on character
encoding detection.  This is not recommended for general use.  In
particular, it's not safe for sharing across multiple threads and
will fail throw if this is attempted.

### Dependencies

On OSX:

- When using Homebrew: `brew install libmagic`
- When using macports: `port install file`

### Troubleshooting

- 'MagicException: could not find any magic files!': some
  installations of libmagic do not correctly point to their magic
  database file.  Try specifying the path to the file explicitly in the
  constructor: `magic.Magic(magic_file="path_to_magic_file")`.

## Author

Originally written by Adam Hupp in 2001 for a project that never got off the
ground.  It originally used SWIG for the C library bindings, but
switched to ctypes once that was part of the python standard library.

## License

python-magic is distributed under the MIT license.  See the included
LICENSE file for details.