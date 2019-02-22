"""
Automated Comment Checker: A comment checker that checks for different types of comments and lines
in each file.

Author: Jeremy Shih
"""

# PLEASE READ THE "README.txt" FILE FOR FURTHER INSTRUCTIONS ON HOW TO RUN THE PROGRAM.

import re
import os
import csv
import argparse

# Prevent printing stracktrace when raising an exception
import sys
sys.tracebacklimit = 0


def read_csv_file(csv_file):
    """ Scan a csv_file and store the different ways of commenting single line comments and multi line comments for
     different languages into two different dictionaries.

    @param string csv_file:
    @rtype: dict single_commenting_syntax:
    @rtype: dict multi_commenting_syntax:
    @rtype: list extension_list:
    """

    # Read in excel for commenting syntax of different languages and add them into two dictionaries
    single_commenting_syntax = {}
    multi_commenting_syntax = {}

    # List of file extensions in the .csv file
    extension_list = []

    try:
        with open(csv_file, 'r') as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                extension_list.append(row[0])

                # populate single line commenting dictionary (add first syntax for single line comments)
                single_commenting_syntax[row[0]] = [row[2]]

                # Check if csv file is in right format, if not raise exception
                if row[1].isdigit() is False:
                    raise Exception("CSV file is in wrong format.")
                if int(row[1]) == 0:
                    raise Exception("Need to include single line commenting syntax.")

                # Index that shows the number of ways to comment block comments
                multi_num = int(row[1]) + 2

                if row[multi_num].isdigit() is False:
                    raise Exception("CSV file is in wrong format.")
                if int(row[multi_num]) == 0:
                    raise Exception("Need to include multi line commenting syntax.")

                # if there are more than one ways of single line commenting, add them in the dictionary
                if int(row[1]) > 1:
                    for i in range(int(row[1]) - 1):
                        single_commenting_syntax[row[0]].append(row[i + 3])

                # populate multi line commenting dictionary
                syntax = row[int(row[1]) + 3].split(' ')
                # add starting syntax of first syntax for multi line comments
                multi_commenting_syntax[row[0]] = [syntax[0]]
                # add ending syntax of first syntax for multi line comments
                multi_commenting_syntax[row[0]].append(syntax[1])
                # if there are more than one ways of single line commenting, add them in the dictionary
                if int(row[multi_num]) > 1:
                    for i in range(int(row[multi_num]) - 1):
                        syntax = row[i + multi_num + 2].split(' ')
                        multi_commenting_syntax[row[0]].append(syntax[0])
                        multi_commenting_syntax[row[0]].append(syntax[1])

    except FileNotFoundError:
        print("Please input csv file from the same folder.")
        sys.exit(1)

    return single_commenting_syntax, multi_commenting_syntax, extension_list


def build_regex(single_commenting_syntax, multi_commenting_syntax, extension):
    """ Build and return a regex for identifying single line comments and a regex for identifying
     both singlie line and multi line comments.

    @param dict single_commenting_syntax:
    @param dict multi_commenting_syntax:
    @param str extension:
    @rtype: str single_line_regex:
    @rtype: str regex:
    """

    # Build single_line_regex and full regex
    regex = "("
    single_line_regex = ""
    try:
        # Add single line syntax to regex
        for i in range(len(single_commenting_syntax[extension])):
            # single_syntax_length is the length of the single line commenting syntax
            single_syntax_length = len(single_commenting_syntax[extension][i])
            for j in range(single_syntax_length):
                regex += "\\" + single_commenting_syntax[extension][i][j]
            regex += "(?:.*)$|"

        single_line_regex = single_line_regex + regex[:-1]

        # Add multi line syntax to regex
        for i in range(0, len(multi_commenting_syntax[extension]), 2):
            for j in range(2):
                multi_syntax_length = len(multi_commenting_syntax[extension][i + j])
                # Add each character/symbol of a multi line commenting syntax one at a time into the regex
                for k in range(multi_syntax_length):
                    regex += "\\" + multi_commenting_syntax[extension][i + j][k]
                # When done adding the start and end of a multi line commenting syntax, add regex
                if j == 0:
                    regex += "(?:(?:.|\\n)*?)"
            # When we aren't finished adding the different ways to comment, add a or to the regex
            if (i + 2) < len(multi_commenting_syntax[extension]):
                regex += "|"

        regex += ")"
        single_line_regex += ")"
    except KeyError:
        print("Please add the syntax for commenting for that specific langauge in the .csv file to proceed.")
        sys.exit(1)

    return single_line_regex, regex


def file_summary(csv_file, file_name):
    """ Scan a file and output the total number of lines, comment lines, single line comments,
    comment lines within block comments, block line comments, and TODO's in the comments.

    @param str csv_file:
    @param str file_name:
    @rtype: list summary:
    """

    # Read csv file and keep commenting syntax in two dictionaries using helper function
    single_commenting_syntax, multi_commenting_syntax, extension_list = read_csv_file(csv_file)

    # Import file and read lines without newline character and blank lines (for total number of lines)
    try:
        with open(file_name) as file_handler:
            contents = (line.rstrip() for line in file_handler)  # Strip the empty space at the end of each line
            contents = list(line for line in contents if line)  # Non-blank lines in a list
    except FileNotFoundError:
        print("Please input program file from the same folder.")
        sys.exit(1)

    # Identify type of file
    name_extension = os.path.splitext(file_name)
    extension = name_extension[1]

    # Build Regex using helper function
    single_line_regex, regex = build_regex(single_commenting_syntax, multi_commenting_syntax, extension)

    # Create 5 lists that contain lines that meet the following criteria:
    # comment_lines, single_line_comments, comment_lines_within_block, block_line_comments, and todos
    comment_lines, single_line_comments, comment_lines_within_block, block_line_comments, todos = [], [], [], [], []

    # Open file
    file_handler = open(file_name)

    # Create a string containing the whole file
    whole_file = ''.join(file_handler.readlines())

    # Create list of all comments (single or block) for that langauge
    all_comments = re.findall(regex, whole_file, re.M)

    # Comment Lines
    for comment in all_comments:
        # For comments with a new line characters, split into two comments
        if '\n' in comment:
            split_lines = comment.split("\n")
            for line in split_lines:
                comment_lines.append(line)
        else:
            comment_lines.append(comment)

    # Single Line Comments
    single_line_comments = re.findall(single_line_regex, whole_file, re.M)

    # Block Line Comments
    block_line_comments = []
    for comment in all_comments:
        if comment not in single_line_comments:
            block_line_comments.append(comment)

    # Comment Lines Within Block
    for comment in block_line_comments:
        split_lines = comment.split("\n")
        for line in split_lines:
            comment_lines_within_block.append(line)

    # Comment lines with ToDos
    for comment in all_comments:
        if 'TODO' in comment:
            todos.append(comment)

    # Count number of items in each list
    total_lines = len(contents)
    comment_lines = len(comment_lines)
    single_line_comments = len(single_line_comments)
    comment_lines_within_block = len(comment_lines_within_block)
    block_line_comments = len(block_line_comments)
    todos = len(todos)

    # Close File
    file_handler.close()

    summary =[total_lines, comment_lines, single_line_comments, comment_lines_within_block, block_line_comments,
              todos]

    return summary


def output_file_summary(csv_file, file_name):
    """ Scan a file and output the total number of lines, comment lines, single line comments,
    comment lines within block comments, block line comments, and TODO's in the comments.

    @param str csv_file:
    @param str file_name:
    @rtype: NoneType:
    """

    summary = file_summary(csv_file, file_name)
    total_lines, comment_lines, single_line_comments, comment_lines_within_block, block_line_comments, todos\
        = summary

    # Print out Counts
    print("Total # of lines: {}".format(total_lines))
    print("Total # of comment lines: {}".format(comment_lines))
    print("Total # of single line comments: {}".format(single_line_comments))
    print("Total # of comment lines within block comments: {}".format(comment_lines_within_block))
    print("Total # of block line comments: {}".format(block_line_comments))
    print("Total # of TODO's : {}".format(todos))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="please pass in .csv file containing commenting syntaxes", type=str)
    parser.add_argument("file", help="please pass in file", type=str)
    args = parser.parse_args()
    output_file_summary(args.csv, args.file)
