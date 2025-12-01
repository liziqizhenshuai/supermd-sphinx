# 文档编写快速入门

这是项目模板，请根据 [reStructuredText](https://www.sphinx-doc.org/zh-cn/master/usage/restructuredtext/) 语法在 `source` 里添加新章节并编写文档，然后本地编译检查效果，循环往复直到满意

## 本地编译环境搭建

### linux / wsl 环境

先安装 [uv](https://docs.astral.sh/uv) ，这一步可能需要先激活科学上网，否则请使用 conda/pip 之类的工具自行安装

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

由于涉及 latex pdf 编译，所以还需要 xelatex 工具

```sh
sudo apt install texlive-full
```

由于涉及电子书格式 epub/mobi 等，所以还需要 calibre 工具

```sh
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
```

准备好后，可以编译了

```sh
# 同步配置
uv sync
# 激活虚拟环境
source .venv/bin/activate
# 开始编译
python build_docs.py
```

### windows 环境

先安装 [uv](https://docs.astral.sh/uv) ，这一步可能需要先激活科学上网，否则请使用 conda/pip 之类的工具自行安装

请使用 powershell 而不是 cmd

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

前往 <https://tug.org/texlive/windows.html> 安装 texlive
前往 <https://calibre-ebook.com/download_windows> 安装 calibre

然后开始编译

```powershell
# 同步配置
uv sync
# 激活虚拟环境
.venv\Scripts\activate
# 开始编译
python build_docs.py
```

编译完成后，文件将出现在 build 文件夹，直接双击相应文件即可打开查看
