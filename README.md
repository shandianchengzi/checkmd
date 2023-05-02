[中文版](./README_zh.md) | English

# checkmd
A tool under development that automatically detects the correctness of all markdown documents in a directory (including typos, broken links, etc.).

## Usage

1. Install Python3 and run the following command to install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Clone the repository you want to analyze, such as `docs-online`:
    ```bash
    git clone https://gitee.com/rtthread/docs-online
    ```
    After cloning, a directory named `docs-online` will be created in the current directory.

3. Run the `main.py` program:
    ```bash
    python3 main.py <path to the repository you want to analyze>
    ```
    For example:
    ```bash
    python3 main.py docs-online
    ```
4. For more configuration options, refer to the parameter parsing section in [repo_config.yml](./repo_config.yml) and [main.py](./main.py). These additional configurations specific to each analyzed repository will provide you with great convenience!

## Developing
- [x] Check for broken web links.
- [x] Check for redirection and output whether the link before and after redirection is consistent. It can be judged by checking whether the file name (the value after the last slash) is consistent.
- [x] Extract links in the `src` tag.
- [x] Ask the user if they want to clear the output folder. If cleared, the output folder will be automatically cleared.
- [x] Add command line argument parsing:
  - [x] `repo_path`: set the input repo path by user.
- [x] Add `config.yml` argument parsing and its functionality:
  - [x] `log_path`: set the log path by user.
  - [x] `possible_web_base_path`: possible web base path list.
  - [x] `repo_link`: set the repo link by user.
  - [x] `fp_filter`: ignore some URLs which have been checked or no need to check.
- [ ] Check for broken relative links:
  - [x] Check if links in repositories with root directories used for rendering web pages are broken.
  - [ ] Check if relative links based on the current file are broken.
- [ ] Add User Agent to handle broken links that cannot be accessed without headers.
- [ ] Spell-checking (Prioritize Chinese typo checking)
- [ ] Check consistency between encoding formats and file-saving formats.