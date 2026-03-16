import unittest

from StaticSiteGenerator.src.gencontent import extract_title

class TestFunctions(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        md2 = """This is a text with multiple line
# with header at line 2     
and extra text after"""
        md3 = "text with no title"
        title = extract_title(md)
        self.assertEqual("Hello", title)
        title = extract_title(md2)
        self.assertEqual("with header at line 2", title)
        try:
            title = extract_title(md3)
        except Exception as e:
            self.assertEqual(e.args[0],"Missing H1/title in markdown")