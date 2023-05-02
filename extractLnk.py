import re
import os
import glob
import urllib.parse
from log import logByType
from checkLink import checkUrl
import globs

class LinkInfo:
    def __init__(self, link, filepath):
        # raw error link
        self.link = link
        # other link infos, for output more info to locate the error.
        self.filepath = globs.config.repo_link + filepath.lstrip(globs.args.repo_path)
        self.status = (0, "") # (status_code, status_text)

    def __hash__(self):
        # return hash((self.link, self.filepath))
        return hash((self.link, self.filepath))

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
            logByType('error', "exist no-utf-8 char\t{}\t0\t{}\n".format(filepath, e))
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
    # ignore the link in fp_filter
    for fp_pattern in globs.config.fp_filter:
        if re.match(fp_pattern, link):
            return False
    # check whether is none
    if link == '':
        logByType('error', '""\t%s\t0\tfind one empty link in md.\n' % linkinfo.filepath)
        return False
    # ignore the anchor
    if link[0] == '#': 
        return False
    # check usual link
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
    # check web markdown
    elif link[0] == '/':
        linkinfo.status = (404, "Web File no found.")
        possible_extra_end = ["html","md","xml","wxml","xml"]
        possible_special_end = ["#", "?"]
        # ignore the special end, eg: /rt-thread/README.md#Introduction
        for end in possible_special_end:
            if end in link:
                link = link.split(end)[0]
        # ignore the exist file
        for base in globs.config.possible_web_base_path:
            # no end but exists, ignore but think it is warning
            if os.path.exists(os.path.join(base, "." + link)):
                # only warning the file, not the dir
                if os.path.isfile(os.path.join(base, "." + link)):
                    logByType('warning', '%s\t%s\t0\tfind with extra file end when web page.\n' % (link, linkinfo.filepath))
                return False
            # try to add extra end for file to check
            else:
                for end in possible_extra_end:
                    if os.path.exists(os.path.join(base, "." + link + "." + end)):
                        return False
        return True
    # TODO: find out the relative path error
    else:
        # Now: ignore the relative link
        return False

def extractLinkFromRepo(repopath):
    logByType("debug_info", "[*] Start to extract links from all the .md files...\n")
    # find all the md file
    markdown_files = glob.glob(os.path.join(repopath, '**/*.md'), recursive=True)
    for file in markdown_files:
        logByType("debug_info", f"[*] Start to extract links from {file}...\n")
        # extract link from a file
        linkinfos = extractLinkFromFile(file)
        for linkinfo in linkinfos:
            if linkFilter(linkinfo):
                linkinfo.dumpStatus()
    logByType("debug_info", "[+] Check Done!\n")
    return True




