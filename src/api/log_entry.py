"""
Object to represent the elements of an SVN Log Entry as shown in SVN 1.5/1.6, example:

r36715 | amcauthor | 2010-02-05 12:38:05 -0500 (Fri, 05 Feb 2010) | 1 line

Fix for BugID #1231 in Program B.
"""

class SvnLogEntry(object):

    def __init__(self,
                 revision,
                 author,
                 commit_date,
                 lines_changed,
                 comment,
                 fogbugz):

        self.revision = revision
        self.author = author
        self.commit_date = commit_date
        self.lines_changed = lines_changed
        self.comment = comment
        self.fogbugz = fogbugz
