"""
 vim: tw=80
SVN Log Reader

Takes in input in various forms and attempts to interpret it as a series
of SvnLogEntry objects, which can be searched for and filtered upon.
"""

from optparse import OptionParser
import sys
import re

from parser import SvnLogParser, SVN_LOG_SEPARATOR

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

def filter(entries, filters):

    if len(filters) == 0:
        return entries
    
    #trading space for time
    filtered_entries = entries[:]

    for filter, pattern in filters.iteritems():
        re_matcher = re.compile(pattern)

        for entry in filtered_entries:
            entry_attr = getattr(entry, filter)

            if not re_matcher.search(entry_attr):
                filtered_entries.remove(entry)

    return filtered_entries

def process(svnlog_file, filters, callback = None):
    
    buffer = []
    filtered_entries = []

    for line in svnlog_file:
        if line.strip() == SVN_LOG_SEPARATOR: 

            if len(buffer) > 0:
                entry_text = '\n'.join(buffer)
                entry = SvnLogParser.parse_log_entry(entry_text)
                
                filtered_entry = filter([entry], filters)
                filtered_entries += filtered_entry

                if callback:
                    callback(filtered_entry)

                buffer = []

        else:
            buffer.append(line)

    return filtered_entries

def printer_callback(x):
    if x:
        print x

def main():
    
    options, args = parse_arguments()

    svnlog_file = None
    if options.filename == '-':
        svnlog_file = sys.stdin
    elif options.filename:
        svnlog_file = file(options.filename, 'r')
    else:
        print >> sys.stderr, ("filename must be selected, please select a file"
                              " with -f or --filter options")
        sys.exit(255)

    filters = {}

    for attribute in dir(options):
        if attribute.startswith('filter_'):

            key = attribute[len('filter_'):]
            value = getattr(options, attribute)

            if value: filters[key] = value

    filtered_entries = process(svnlog_file, filters, printer_callback)

    if len(filtered_entries) == 0:
        #grep-like behavior
        sys.exit(1)

if __name__ == '__main__':
    main()
