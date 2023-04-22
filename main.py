import globs
import os
from extractLnk import extractLinkFromRepo

if __name__ == "__main__":
    # TODO: add args parse and set output as an arg.
    globs.log_path = "./output"
    # os.system("rm %s/*" % globs.log_path)
    ret = extractLinkFromRepo("TencentOS-tiny")
