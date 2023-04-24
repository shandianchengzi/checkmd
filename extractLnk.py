import re
import os
import glob
import urllib.parse
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
        # return hash((self.link, self.filepath))
        return hash(self.link)

    def __eq__(self, other):
        return self.link == other.link and self.filepath == other.filepath

    def dumpStatus(self):
        logByType('links', "%s\n" % self.link)
        logByType('links_with_info', "%s\t%s\t%d\t%s\n" % (self.link, self.filepath, self.status[0], self.status[1]))

def extractLinkFromFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
        except UnicodeDecodeError as e:
            logByType('error', "[{}] {}\n".format(filepath, e))
            return set()
    linkinfos = set()
    # 1. extract md url
    pattern = r'\]\((.*?)\)'
    links = set(re.findall(pattern, content))
    # 2. extract html url
    pattern = r'src="(.*?)"'
    links |= set(re.findall(pattern, content))
    # add the filepath info
    for link in links:
        linkinfos.add(LinkInfo(link, filepath))
    return linkinfos

def ignoreUrlDifference(item):
    # ignore the unquote difference in url
    item = urllib.parse.unquote(item)
    # ignore the lower and upper difference in url
    item = item.lower()
    return item

def checkRedirectSucuess(link, link_after):
    enditem = ""
    enditem_link = ""
    # ignore if the param is same
    try: 
        pre, enditem = link_after.rsplit('?', 1)
        pre_link, enditem_link = link.rsplit('?', 1)
        if ignoreUrlDifference(enditem) == ignoreUrlDifference(enditem_link):
            return True
    except:
        pass
    # ignore if the end link is same
    try:
        pre, enditem = link_after.rsplit('/', 1)
        pre_link, enditem_link = link.rsplit('/', 1)
        # ignore the / in the end
        if link_after[-1] == '/':
            pre, enditem = link_after[:-1].rsplit('/', 1)
        if link[-1] == '/':
            pre_link, enditem_link = link[:-1].rsplit('/', 1)
        if ignoreUrlDifference(enditem) == ignoreUrlDifference(enditem_link):
            return True
    except:
        pass
    return False

def linkFilter(linkinfo):
    link = linkinfo.link
    # check whether is none
    if link == '':
        logByType('error', '[%s] find one empty link in md.\n' % linkinfo.filepath)
        return False
    # ignore the anchor
    if link[0] == '#': 
        return False
    if link[0:4] == 'http':
        linkinfo.status = checkUrl(link)
        # ignore the success url
        if linkinfo.status[0] == 200:
            return False
        # ignore the successful redirection
        if str(linkinfo.status[0])[0] == '3':
            if checkRedirectSucuess(link, linkinfo.status[1]):
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
        all_linkinfos |= linkinfos
    for linkinfo in all_linkinfos:
        # filte some special link
        if linkFilter(linkinfo):
            linkinfo.dumpStatus()
    return True




