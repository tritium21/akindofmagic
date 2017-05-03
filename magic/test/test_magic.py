import magic
import os.path

TEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'test.zip')

def test_from_file_mime():
    expected = 'application/zip'
    actual = magic.from_file(TEST_FILE, mime=True)
    assert actual == expected

def test_from_file():
    expected = 'Zip archive data'
    actual = magic.from_file(TEST_FILE)
    assert actual.startswith(expected)

def test_from_buffer_mime():
    expected = 'application/zip'
    with open(TEST_FILE, 'br') as f:
        actual = magic.from_buffer(f.read(), mime=True)
    assert actual.startswith(expected)

def test_from_buffer():
    expected = 'Zip archive data'
    with open(TEST_FILE, 'br') as f:
        actual = magic.from_buffer(f.read())
    assert actual.startswith(expected)