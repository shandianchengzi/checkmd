import globs
import os
from extractLnk import extractLinkFromRepo
import argparse
import shutil

from utils import yaml_load
from log import logByType

default_config = argparse.Namespace(
    possible_web_base_path=[], # default possible_web_base_path as the repo path
    repo_link="", # if set, add repo_link when output filepath
    fp_filter=[], # ignore some urls which have checked or no need to check.
    log_path="" # default is output+repopath
)

def _parse_config(repo_path):
    global default_config
    config_path = globs.args.repo_config
    # if not set, just use the default 
    if config_path == None:
        return default_config
    # load config
    config = yaml_load(config_path)
    # check args.repo_path
    if repo_path not in config.keys():
        logByType("debug_info", f"[-] Cannot find the config of {repo_path}, please check path.\n")
        print(f"[-] Cannot find the config of {repo_path}, please check path.")
        return default_config
    # record config content
    default_config.__dict__.update(config[repo_path])
    return default_config

def _parse_args():
    parse = argparse.ArgumentParser(description="checkmd is a helper to quickly check the error in markdown files in the whole repository.")
    parse.add_argument('repo_path', type=str, help="Your local repo path to be checked.")
    # Optional config
    parse.add_argument('-c', '--repo_config', default=None, type=str, help="Optional config for one repo, config format is yml.")
    return parse.parse_args()

if __name__ == "__main__":
    # args parse
    args = _parse_args()
    globs.args = args

    # set default log path
    default_config.log_path = "./%soutput" % args.repo_path

    # set default web path
    default_config.possible_web_base_path = [args.repo_path]

    # set optional config
    globs.config = _parse_config(args.repo_path)

    # create log path
    if not os.path.exists(globs.config.log_path):
        os.mkdir(globs.config.log_path)
    # clear exist log
    else:
        rmlog = input(f"[*] Find exist log path {globs.config.log_path}, do you want to remove them?[Y/n]")
        if rmlog not in ["n", "N"]:
            logByType("debug_info", f"[+] Remove the path {globs.config.log_path}\n")
            print(f"[+] Remove the path {globs.config.log_path}")
            shutil.rmtree(globs.config.log_path)
            os.mkdir(globs.config.log_path)

    ret = extractLinkFromRepo(args.repo_path)
