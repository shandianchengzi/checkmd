# checkmd
一个正在开发中的工具，去自动检测整个目录下所有 markdown 文档的正确性（包括错别字、失效链接等）

## Usage

1. 安装 python3 ，然后运行如下命令，安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

2. 克隆需要分析的仓库，修改 `main.py` 中的 `input_path` 变量，改成你的仓库的路径。

3. 运行 `main.py` 程序即可：
    ```bash
    python3 main.py
    ```

## Developing
- [x] 检查网页链接失效
- [ ] 检查相对路径失效
- [ ] 失效链接加上 User Agent 进一步确认是否失效
- [ ] 错别字检查
- [ ] 编码格式与文件实际保存格式的一致性检查