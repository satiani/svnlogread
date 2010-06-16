"""
Parser to convert the following text:

r36715 | ntantai | 2010-02-05 12:38:05 -0500 (Fri, 05 Feb 2010) | 1 line

add the solr war file that is missing FogBugz #12378

to an SvnLogEntry instance.
"""

from api import SvnLogEntry

import re
import datetime

COMMIT_METADATA_RE = re.compile(('r([0-9]+) \| ([^ ]+) \| (....)-(..)-(..) '
                                 '(..):(..):(..) [^|]+ \| ([0-9]+) lines?'))

FOGBUGZ_RE = re.compile('.*(FB|FogBugz|BUGZID|Case|BugID) ?#?([0-9]+).*')

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

        for line in lines[2:]:
            re_obj = FOGBUGZ_RE.match(line, re.I)
            if re_obj:
                fogbugz = re_obj.groups()[1]
                break

        comment = '\n'.join(lines[2:])

        return SvnLogEntry(revision, author, commit_date, lines_changed,
                           comment, fogbugz)
