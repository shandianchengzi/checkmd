import re
import os
import glob
from log import logByType

class LinkInfo:
    def __init__(self, link, filepath):
        # raw error link
        self.link = link
        # other link infos, for output more info to locate the error.
        self.filepath = filepath

    def __hash__(self):
        return hash((self.link, self.filepath))

    def __eq__(self, other):
        return self.link == other.link and self.filepath == other.filepath

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

def linkFilter(linkinfos):
    linkinfos_fixed = set()
    for linkinfo in linkinfos:
        # check whether is none
        if linkinfo.link == '':
            logByType('error', 'find one empty link in md: %s\n' % linkinfo.filepath)
            continue
        # ignore the anchor
        if linkinfo.link[0] == '#': 
            pass
        # [TODO: find out the relative path error] ignore the relative link
        # https://github.com/OpenAtomFoundation/TencentOS-tiny/blob/master/README_en.md
        if linkinfo.link[0] == 'h':
            linkinfos_fixed.add(linkinfo)
    return linkinfos_fixed

def dumpLinkFromLinkInfo(linkinfos):
    for linkinfo in linkinfos:
        logByType('links', "%s\n" % linkinfo.link)
        logByType('links_with_file', "%s\t%s\n" % (linkinfo.link, linkinfo.filepath))

def extractLinkFromRepo(repopath):
    all_linkinfos = set()
    # find all the md file
    markdown_files = glob.glob(os.path.join(repopath, '**/*.md'), recursive=True)
    for file in markdown_files:
        # extract link from a file
        linkinfos = extractLinkFromFile(file)
        # filte some special link
        linkinfos = linkFilter(linkinfos)
        all_linkinfos |= linkinfos
    dumpLinkFromLinkInfo(all_linkinfos)
    return True




