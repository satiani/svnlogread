"""
Parser to convert the following text:

r36715 | amcauthor | 2010-02-05 12:38:05 -0500 (Fri, 05 Feb 2010) | 1 line

Fix for BugID #1231 in Program B.

to an SvnLogEntry instance.
"""

from api import SvnLogEntry

import re
import datetime

COMMIT_METADATA_RE = re.compile(('r([0-9]+) \| ([^ ]+) \| (....)-(..)-(..) '
                                 '(..):(..):(..) [^|]+ \| ([0-9]+) lines?'))

CHANGED_PATHS_STR = 'Changed paths:'

PATH_RE = re.compile('^   [A-Z] ((/[^/]+)+/?)$')

FOGBUGZ_RE = re.compile('(FB|FogBugz|BUGZID|Case|BugID) *#* *([0-9]+)')

SVN_LOG_SEPARATOR = '-'*72

class SvnLogParser(object):
    
    @staticmethod
    def parse_log_entry(entry_text):
        lines = entry_text.splitlines()

        assert len(lines) > 2, ("Invalid SVN log entry text, must have at "
                                "least 3 lines in input")
        
        commit_metadata = lines[0]
        
        re_obj = COMMIT_METADATA_RE.match(commit_metadata)

        assert re_obj, ("Invalid SVN log entry text, unrecognized "
                        "metadata %s") % commit_metadata

        revision, author, year, month, day, hour, minute, second, \
        lines_changed = re_obj.groups()

        commit_date = datetime.datetime(*map(int, (year, month, day, hour,
                                                   minute, second)
                                            )
                                       )

        fogbugz = None

        changed_paths = []

        if lines[1].strip() == CHANGED_PATHS_STR:
            for line in lines[2:]:
                re_obj = PATH_RE.match(line)
                if re_obj:
                    changed_paths.append(re_obj.groups()[0])
                else:
                    break

        #calculate line offset for comments given whether the log has changed paths in it
        line_offset = 2 + (len(changed_paths) and 1 + len(changed_paths) or 0)

        for line in lines[line_offset:]:
            re_obj = FOGBUGZ_RE.search(line, re.I)
            if re_obj:
                fogbugz = re_obj.groups()[1]
                break

        comment = '\n'.join(lines[line_offset:])

        return SvnLogEntry(revision, author, commit_date, lines_changed,
                           comment, fogbugz, changed_paths)
