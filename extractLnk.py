import re
import os
import glob
from log import logByType
from checkLink import checkUrl

class LinkInfo:
    def __init__(self, link, filepath):
        # raw error link
        self.link = link
        # other link infos, for output more info to locate the error.
        self.filepath = filepath
        self.status = (0, "") # (status_code, status_text)

    def __hash__(self):
        return hash((self.link, self.filepath))

    def __eq__(self, other):
        return self.link == other.link and self.filepath == other.filepath

    def dumpStatus(self):
        logByType('links', "%s\n" % self.link)
        logByType('links_with_info', "%s\t%s\t%d\t%s\n" % (self.link, self.filepath, self.status[0], self.status[1]))

def extractLinkFromFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    linkinfos = set()
    # Use the re module to match the link in the string
    pattern = r'\]\((.*?)\)'
    links = set(re.findall(pattern, content))
    # add the filepath info
    for link in links:
        linkinfos.add(LinkInfo(link, filepath))
    return linkinfos

def linkFilter(linkinfo):
    link = linkinfo.link
    # check whether is none
    if link == '':
        logByType('error', 'find one empty link in md: %s\n' % linkinfo.filepath)
        return False
    # ignore the anchor
    if link[0] == '#': 
        return False
    if link[0] == 'h':
        linkinfo.status = checkUrl(link)
        # ignore the success url
        if linkinfo.status[0] == 200:
            return False
        return True
    # TODO: find out the relative path error
    else:
        # Now: ignore the relative link
        return False

def extractLinkFromRepo(repopath):
    all_linkinfos = set()
    # find all the md file
    markdown_files = glob.glob(os.path.join(repopath, '**/*.md'), recursive=True)
    for file in markdown_files:
        # extract link from a file
        linkinfos = extractLinkFromFile(file)
        for linkinfo in linkinfos:
            # filte some special link
            if linkFilter(linkinfo):
                linkinfo.dumpStatus()
    return True




