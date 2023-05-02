import globs
import os
from extractLnk import extractLinkFromRepo

input_path = "docs-online"

if __name__ == "__main__":
    # TODO: add args parse
    # TODO: add args[output_path] to set the output path by user.
    globs.log_path = "./%soutput"%input_path
    if not os.path.exists(globs.log_path):
        os.mkdir(globs.log_path)
    # TODO: delete all the output file safely.
    # os.system("rm %s/*.txt" % globs.log_path)
    # TODO: add arg[fp_filter] to ignore some urls which have checked or no need to check.
    # TODO: add arg[input_path] to set the input path by user.
    # TODO: add arg[a]
    globs.possible_web_base_path = [input_path] # set default possible_web_base_path as the repo path.
    ret = extractLinkFromRepo(input_path)
