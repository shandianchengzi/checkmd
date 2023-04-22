import globs
import os
from extractLnk import extractLinkFromRepo

input_path = "TencentOS-tiny"

if __name__ == "__main__":
    # TODO: add args parse
    # TODO: add args[output_path] to set the output path by user.
    globs.log_path = "./output"
    # TODO: delete all the output file safely.
    # os.system("rm %s/*.txt" % globs.log_path)
    # TODO: add arg[url_filter] to ignore some urls which have checked or no need to check.
    # TODO: add arg[input_path] to set the input path by user.
    ret = extractLinkFromRepo(input_path)
