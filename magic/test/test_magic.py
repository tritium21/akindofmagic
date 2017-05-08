import unittest
import os.path
import io

import magic

TEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'test.zip')

class TestMagic(unittest.TestCase):
    def test_from_file_mime(self):
        expected = 'application/zip'
        actual = magic.from_file(TEST_FILE, mime=True)
        self.assertEqual(actual, expected)

    def test_from_file(self):
        expected = 'Zip archive data'
        actual = magic.from_file(TEST_FILE)
        self.assertTrue(actual.startswith(expected))

    def test_from_buffer_mime(self):
        expected = 'application/zip'
        with io.open(TEST_FILE, 'br') as f:
            actual = magic.from_buffer(f.read(), mime=True)
        self.assertEqual(actual, expected)

    def test_from_buffer(self):
        expected = 'Zip archive data'
        with io.open(TEST_FILE, 'br') as f:
            actual = magic.from_buffer(f.read())
        self.assertTrue(actual.startswith(expected))

if __name__ == '__main__':
    unittest.main()
