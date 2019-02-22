"""
Automated Comment Checker Unit Test: Unit Tests for the automated_comment_checker program.

Author: Jeremy Shih
"""

import unittest
from automated_comment_checker import file_summary
from automated_comment_checker import read_csv_file
from automated_comment_checker import build_regex


class TestFileSummary(unittest.TestCase):

    """Test whether file_summary function works properly.

    """

    def testPythonFile(self):
        """ Test program with a Python File.
        """
        self.output = file_summary("commenting_syntax.csv", "test/gui_controller.py")
        self.assertEqual(self.output, [41, 37, 19, 18, 2, 3])

    def testJavaFile(self):
        """ Test program with a Java File.
        """
        self.output = file_summary("commenting_syntax.csv", "test/Flight.java")
        self.assertEqual(self.output, [77, 28, 6, 22, 2, 1])

    def testCFile(self):
        """ Test program with a C File.
        """
        self.output = file_summary("commenting_syntax.csv", "test/compare.c")
        self.assertEqual(self.output, [26, 10, 0, 10, 1, 0])

    def testHTMLFile(self):
        """ Test program with a HTML File.
        """
        self.output = file_summary("commenting_syntax.csv", "test/index.html")
        self.assertEqual(self.output, [53, 2, 2, 0, 0, 0])

    def testCSSFile(self):
        """ Test program with a CSS File.
        """
        self.output = file_summary("commenting_syntax.csv", "test/style.css")
        self.assertEqual(self.output, [163, 41, 41, 0, 0, 0])

    def testCapsFileExtension(self):
        """ Test program with a Java File which has a file extension in full caps.
        """
        self.output = file_summary("commenting_syntax.csv", "test/TestCaps.JAVA")
        self.assertEqual(self.output, [77, 28, 6, 22, 2, 1])

    def testAlternatingUpperLowerCaseFileExtension(self):
        """ Test program with a Java which has a file extension with alternating upper and lower cases.
        """
        with self.assertRaises(SystemExit) as output:
            file_summary("commenting_syntax.csv", "test/test_alternating_characters.JaVa")

        self.assertEqual(output.exception.code, 1)

    def testEmptyFile(self):
        """ Test program with an empty program File.
        """

        self.output = file_summary("commenting_syntax.csv", "test/empty.py")
        self.assertEqual(self.output, [0, 0, 0, 0, 0, 0])

    def testSingleLineComments(self):
        """ Test program with just singe line comments.
        """

        self.output = file_summary("commenting_syntax.csv", "test/single_line.py")
        self.assertEqual(self.output, [1, 1, 1, 0, 0, 0])

    def testSingleLineWithinSingleLineComments(self):
        """ Test program with a Single Line commenting syntax within a single line comment.
        """

        self.output = file_summary("commenting_syntax.csv", "test/two_single_same_line.py")
        self.assertEqual(self.output, [1, 1, 1, 0, 0, 0])

    def testBlockComments(self):
        """ Test program with just block/multi-line comments.
        """

        self.output = file_summary("commenting_syntax.csv", "test/multi_line.py")
        self.assertEqual(self.output, [3, 3, 0, 3, 1, 0])

    def testNestedBlockComments(self):
        """ Test program with just nested block comments
        """

        self.output = file_summary("commenting_syntax.csv", "test/nested_multi_line_comment.py")
        self.assertEqual(self.output, [3, 4, 0, 4, 2, 0])

    def testTODOComments(self):
        """ Test program with just TODO comments.
        """

        self.output = file_summary("commenting_syntax.csv", "test/todo.py")
        self.assertEqual(self.output, [1, 1, 1, 0, 0, 1])

    def testCodeWithComment(self):
        """ Test program with a line that contains code and comments.
        """

        self.output = file_summary("commenting_syntax.csv", "test/code_and_comment.py")
        self.assertEqual(self.output, [1, 1, 1, 0, 0, 0])

    def testSingleCommentandMultiCommentSameLine(self):
        """ Test program with a line that contains both single line comments and multi line comments.
        """

        self.output = file_summary("commenting_syntax.csv", "test/single_and_multi.py")
        self.assertEqual(self.output, [2, 2, 1, 2, 1, 0])

    def testProgramFileNotInFolder(self):
        """ Test program with input file not in folder.
        """
        with self.assertRaises(SystemExit) as output:
            file_summary("commenting_syntax.csv", "not_in_folder.py")

        self.assertEqual(output.exception.code, 1)

    def InvalidProgramFileName(self):
        """ Test program with invalid program filename.
        """

        with self.assertRaises(SystemExit) as output:
            file_summary("commenting_syntax.csv", ".sdf")

        self.assertEqual(output.exception.code, 1)

    def InvalidCSVFileName(self):
        """ Test program with invalid CSV file name.
        """

        with self.assertRaises(SystemExit) as output:
            file_summary("wrong_csv.csv", "test.py")

        self.assertEqual(output.exception.code, 1)


class TestReadCSVFile(unittest.TestCase):
    """ Test whether read_csv_file works properly.
    """

    def testCSVNotInFolder(self):
        """ Test on a CSV file that is not in the folder.
        """
        with self.assertRaises(SystemExit) as output:
            read_csv_file("not_in_folder.csv")

        self.assertEqual(output.exception.code, 1)

    def testEmptyCSV(self):
        """ Test on an empty CSV file.
        """
        with self.assertRaises(SystemExit) as output:
            read_csv_file("test/empty.csv")

        self.assertEqual(output.exception.code, 1)

    def testSingleLineCSV(self):
        """ Test on a CSV with one line.
        """

        self.single_commenting_syntax, self.multi_commenting_syntax, self.extension_list \
            = read_csv_file("test/single_line.csv")

        self.assertEqual(self.single_commenting_syntax, {'.py': ['#']})
        self.assertEqual(self.multi_commenting_syntax, {'.py': ["''", "'''", '"""', '"""']})
        self.assertEqual(self.extension_list, ['.py'])

    def testmultiLineCSV(self):
        """ Test on a CSV with multiple lines.
        """

        self.single_commenting_syntax, self.multi_commenting_syntax, self.extension_list \
            = read_csv_file("test/multi_line.csv")

        self.assertEqual(self.single_commenting_syntax, {'.py': ['#'], '.PY': ['#'], '.css': ['/*']})
        self.assertEqual(self.multi_commenting_syntax, {'.py': ["''", "'''", '"""', '"""'],
                                                        '.PY': ["''", "'''", '"""', '"""'], '.css': ['/*', '*/']})
        self.assertEqual(self.extension_list, ['.py', '.PY', '.css'])

    def testCSVEmptyLineBeforeFirstLine(self):
        """ Test on CSV file with empty line before first line of data.
        """
        with self.assertRaises(Exception) as output:
            read_csv_file("test/empty_line_before_first_line.csv")

        self.assertTrue('CSV file is in wrong format.', output.exception)

    def testCSVEmptyLinesBetweenLinesOfData(self):
        """ Test on CSV file with empty linse between lines of data.
        """
        with self.assertRaises(Exception) as output:
            read_csv_file("test/empty_lines_between_data.csv")

        self.assertTrue('CSV file is in wrong format.', output.exception)

    def testCSVWrongFormat(self):
        """ Test on CSV file with wrong format.
        """
        with self.assertRaises(Exception) as output:
            read_csv_file("test/wrong_format.csv")

        self.assertTrue('CSV file is in wrong format.', output.exception)


class TestBuildRegex(unittest.TestCase):

    """ Test whether build_regex works properly.
    """

    def testSyntaxNotInCSV(self):
        """ Test with commenting syntax not in CSV.
        """
        single_commenting_syntax, multi_commenting_syntax, extension_list = read_csv_file("test/syntax_not_in_csv.csv")
        extension = ".py"
        with self.assertRaises(SystemExit) as output:
            build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

        self.assertEqual(output.exception.code, 1)

    def testOneSingleCommentingSyntax(self):
        """ Test with one single commenting syntax and no multi line commenting syntax.
        """

        with self.assertRaises(Exception) as output:
            single_commenting_syntax, multi_commenting_syntax, extension_list \
                = read_csv_file("test/one_single_comemnting_syntax.csv")
            extension = ".py"
            build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

        self.assertTrue("Need to include multi line commenting syntax.", output.exception)

    def testTwoSingleCommentingSyntax(self):
        """ Test with two single commenting syntax and no multi line commenting syntax.
        """

        with self.assertRaises(Exception) as output:
            single_commenting_syntax, multi_commenting_syntax, extension_list \
                = read_csv_file("test/two_single_comemnting_syntax.csv")
            extension = ".py"
            build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

        self.assertTrue('Need to include multi line commenting syntax.', output.exception)

    def testOneMultiCommentingSyntax(self):
        """ Test with one multi-line commenting syntax and no multi line commenting syntax.
        """

        with self.assertRaises(Exception) as output:
            single_commenting_syntax, multi_commenting_syntax, extension_list \
                = read_csv_file("test/one_multi_commenting_syntax.csv")
            extension = ".py"
            build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

        self.assertTrue('Need to include single line commenting syntax.', output.exception)

    def testTowMultiCommentingSyntax(self):
        """ Test with two multi-line commenting syntax and no multi line commenting syntax.
        """

        with self.assertRaises(Exception) as output:
            single_commenting_syntax, multi_commenting_syntax, extension_list \
                = read_csv_file("test/two_multi_commenting_syntax.csv")
            extension = ".py"
            build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

        self.assertTrue('Need to include single line commenting syntax.', output.exception)

    def test1SingleAnd1MultiSyntax(self):
        """ Test with one single-line and multi-line commenting syntax.
        """
        single_commenting_syntax, multi_commenting_syntax, extension_list \
            = read_csv_file("test/single_and_multi_syntax.csv")
        extension = ".py"
        single_line_regex, regex = build_regex(single_commenting_syntax, multi_commenting_syntax, extension)
        self.assertEqual(single_line_regex, "(\#(?:.*)$)")
        self.assertEqual(regex, "(\\#(?:.*)$|\\'\\'(?:(?:.|\\n)*?)\\'\\'\\')")

    def test1SingleAnd2MultiSyntax(self):
        """ Test with one single-line and two multi-line commenting syntax.
        """
        single_commenting_syntax, multi_commenting_syntax, extension_list \
            = read_csv_file("test/1single_and_2multi_syntax.csv")
        extension = ".py"
        single_line_regex, regex = build_regex(single_commenting_syntax, multi_commenting_syntax, extension)
        self.assertEqual(single_line_regex, "(\#(?:.*)$)")
        self.assertEqual(regex, '(\\#(?:.*)$|\\\'(?:(?:.|\\n)*?)\\\'\\\'\\\'|\\"\\"\\"(?:(?:.|\\n)*?)\\"\\"\\")')

    def test2SingleAnd1MultiSyntax(self):
        """ Test with two single-line and one multi-line commenting syntax.
        """
        single_commenting_syntax, multi_commenting_syntax, extension_list \
            = read_csv_file("test/2single_and_1multi_syntax.csv")
        extension = ".py"
        single_line_regex, regex = build_regex(single_commenting_syntax, multi_commenting_syntax, extension)
        self.assertEqual(single_line_regex, "(\#(?:.*)$|\/\/(?:.*)$)")
        self.assertEqual(regex, "(\\#(?:.*)$|\\/\\/(?:.*)$|\\'\\'(?:(?:.|\\n)*?)\\'\\'\\')")

    def test2SingleAnd2MultiSyntax(self):
        """ Test with two single-line and two multi-line commenting syntax.
        """
        single_commenting_syntax, multi_commenting_syntax, extension_list \
            = read_csv_file("test/2single_and_2multi_syntax.csv")
        extension = ".py"
        single_line_regex, regex = build_regex(single_commenting_syntax, multi_commenting_syntax, extension)
        self.assertEqual(single_line_regex, "(\#(?:.*)$|\/\/(?:.*)$)")
        self.assertEqual(regex, '(\\#(?:.*)$|\\/\\/(?:.*)$|\\\'\\\'(?:(?:.|\\n)*?)\\\'\\\'\\\''
                                '|\\\"\\\"\\\"(?:(?:.|\\n)*?)\\\"\\\"\\\")')


if __name__ == '__main__':
    unittest.main()
