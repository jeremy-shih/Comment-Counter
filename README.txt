In order to run the program, please run "automated_comment_checker.py" with two command line arguments: the .csv provided in the folder and the file you want to run it with.

Example: "python automated_comment_checker.py commenting_syntax.csv helloworld.java"

The program will print to standard out all the information.



PLEASE NOTE:
1. Please keep the file you want to test in the same folder as the program. 

2. Please keep the .csv in the same folder as the program. The program will read in a csv file which contains the different ways of commenting in different programming languages. (This was done because it would be easier for people to add the different commenting syntaxes of files they want to test.) 

3. If you would like to add additional languages to the csv file, please follow this format:
column 1 = file extension
column 2 = number of ways to have single line comments
Followed by all the ways you can have single line comments
Number of ways to have multi line comments
Followed by all the ways you can have multi line comments

4. FOR PYTHON files: It was unclear to me how the python example counted for block line comments, so I used this wikipedia page's syntax to identify block line comments.

https://en.wikipedia.org/wiki/Comparison_of_programming_languages_(syntax)#Comments


