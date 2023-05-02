import globs
import os

def logByType(logtype, logstr):
    with open(os.path.join(globs.config.log_path, logtype+".txt"), 'a', encoding='utf-8') as f:
        f.write(logstr)