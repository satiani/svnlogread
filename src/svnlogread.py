"""
 vim: tw=80
SVN Log Reader

Takes in input in various forms and attempts to interpret it as a series
of SvnLogEntry objects, which can be searched for and filtered upon.
"""

from optparse import OptionParser

from parser import SvnLogParser

def parse_arguments():
    parser = OptionParser()

    parser.add_option("-f", "--file", dest="filename",
                      help=("read from FILE, put '-' if you want to read "
                      "from standard input"), metavar="FILE")

    parser.add_option("-a", "--author", dest="filter_author", 
                      metavar="AUTHOR", help=("filter by AUTHOR, where AUTHOR "
                                          "is a regular expression."))

    parser.add_option("-c", "--comment", dest="filter_comment", 
                      metavar="COMMENT", help=("filter by COMMENT, where "
                                          "COMMENT is a regular expression."))

    parser.add_option("-r", "--revision", dest="filter_revision", 
                      metavar="REVISION", help=("filter by REVISION, where "
                                          "REVISION is a regular expression."))

    parser.add_option("-l", "--lines", dest="filter_lines", 
                      metavar="LINES", help=("filter by LINES, where LINES is "
                                          "a regular expression."))

    parser.add_option("-g", "--fogbugz", dest="filter_fogbugz", 
                      metavar="FOGBUGZ", help=("filter by FOGBUGZ, where "
                                          "FOGBUGZ is a regular expression."))

    options, args = parser.parse_args()

    return options, args

def main():
    
    options, args = parse_arguments()

    print options

if __name__ == '__main__':
    main()
