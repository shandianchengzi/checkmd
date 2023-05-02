中文版 | [English](./README.md)

# checkmd
一个正在开发中的工具，去自动检测整个目录下所有 markdown 文档的正确性（包括错别字、失效链接等）

## Usage

1. 安装 python3 ，然后运行如下命令，安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 克隆需要分析的仓库，如 `docs-online`：
    ```bash
    git clone https://gitee.com/rtthread/docs-online
    ```
    克隆完成后，当前目录下会增加目录 `docs-online`。

3. 运行 `main.py` 程序：
    ```bash
    python3 main.py <你需要分析的仓库的目录的路径>
    ```
    如：
    ```bash
    python3 main.py docs-online
    ```
4. 如需更多配置，请参考 [repo_config.yml](./repo_config.yml) 和 [main.py](./main.py) 中的参数解析部分，这些针对每个分析仓库的额外配置将会为你提供非常大的便利！

## Developing
- [x] 检查网页链接失效
- [x] 检查是否发生重定向并输出重定向前后的链接是否一致，可以通过检测文件名（最后一个斜杠后的值）是否一致来判断
- [x] 提取src标签内的链接
- [x] 询问用户是否需要清空输出文件夹，如果清空则自动清空输出文件夹
- [x] 添加命令行参数解析：
  - [x] repo_path: 你需要分析的仓库的路径
- [x] 添加 config.yml 参数解析以及其功能：
  - [x] log_path: 分析结果存放的路径
  - [x] possible_web_base_path: 用于渲染 web 网页的仓库的相对路径链接的可能的基址
  - [x] repo_link: 仓库的网页链接头。设置了这个之后，输出分析结果时将会自动加上仓库的链接，以便直接点击跳转定位问题
  - [x] fp_filter: 一些正则表达式，用于忽略已知的不需要关注的链接
- [ ] 检查相对路径失效
  - [x] 检查用于渲染网页的仓库的、具备根目录的仓库中的链接是否失效
  - [ ] 检查相对于当前文件的相对路径是否失效

- [ ] 失效链接加上 User Agent 排除无 header 无法访问的 FP
- [ ] 错别字检查（优先做中文的错别字检查）
- [ ] 编码格式与文件实际保存格式的一致性检查