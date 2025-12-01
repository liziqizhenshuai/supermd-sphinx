# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
import sys
import datetime

project = "project"
today = datetime.datetime.now().strftime("%Y-%m-%d")
copyright = "鸿之微科技（上海）股份有限公司 Last updated on " + today
author = "Hzwtech"
language = "zh_CN"  # 全局中文

# -- 核心扩展配置（保留模板原有插件 + 新增MD解析）------------------------------
extensions = [
    "sphinx_multiversion",  # 版本控制侧边栏
    "sphinxcontrib.bibtex",  # 参考文献
    "sphinx_copybutton",  # 一键复制代码块
    "sphinx.ext.mathjax",  # JS渲染公式
    "sphinx_design",  # 下拉框自定义
    "sphinx.ext.autodoc",  # 自动生成API文档
    "sphinx.ext.napoleon",  # 支持numpy风格注释
    "myst_parser"  # 新增：解析Markdown文件（核心需求）
]

# 仅为电子书启用公式转图片（模板原有逻辑）
if "epub" in sys.argv:
    extensions.append("sphinx.ext.imgmath")
    imgmath_image_format = "png"

# 公式/参考文献配置（保留模板原有）
imgmath_image_format = "svg"
bibtex_bibfiles = ["refs.bib"]

# -- 基础文档配置 -------------------------------------------------------------
master_doc = "index"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]  # 新增：排除编译目录
math_number_all = False
math_eqref_format = "Eq.{number}"
math_numfig = True

# 版本信息（覆盖模板重复定义，统一配置）
release = "2025A"

# -- 支持MD文件后缀（新增：关键配置）------------------------------------------
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',  # 识别所有.md文件
}

# -- Myst Parser配置（新增：优化MD解析）----------------------------------------
myst_enable_extensions = [
    "colon_fence",    # 支持:::tip等提示框（兼容sphinx_design）
    "strikethrough",  # 支持删除线
    "linkify"         # 自动识别URL（如需禁用，删除此行并跳过pip install linkify-it-py）
]
myst_heading_anchors = 2  # 为H1/H2标题生成锚点，优化跳转

# -- HTML输出配置（保留模板原有 + 优化）---------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# 取消rtd主题的页宽限制，代码块自动换行（模板原有）
def setup(app):
    app.add_css_file("custom.css")

# -- LATEX配置（修复中文PDF + 保留模板原有风格）--------------------------------
latex_engine = "xelatex"  # 新增：中文PDF必需的编译器
latex_elements = {
    # 纸张/字体大小（模板原有，替换为a4更通用）
    "papersize": "a4paper",  # 替换letterpaper为A4（适配国内打印）
    "pointsize": "10pt",
    # 预编译配置（修复中文 + 保留模板原有格式）
    "preamble": r"""
    \addto\captionsenglish{\renewcommand{\chaptername}{}}
    \usepackage[UTF8, scheme = plain]{ctex}
    \usepackage{fontspec}  # 新增：指定云端中文字体
    \usepackage{float}
    \usepackage{indentfirst}
    \usepackage{ragged2e}  # 新增：解决Underfull \hbox排版警告
    \setlength{\parindent}{2em}
    \setmainfont{WenQuanYi Micro Hei}  # 新增：适配云端字体
    \setCJKmainfont{WenQuanYi Micro Hei}  # 新增：中文渲染
    \RaggedRight  # 新增：自动换行，消除排版警告
    """,
    "figure_align": "H",  # 模板原有：让图片不乱跑
    # 新增：禁用超链接解析错误（避免xdvipdfmx致命错误）
    "hyperref": r'\usepackage[hidelinks,unicode]{hyperref}',
    "passoptionstopackages": r'\PassOptionsToPackage{unicode}{hyperref}',
}

# 忽略SVG图片（新增：解决LaTeX无法解析SVG的错误）
latex_ignore_images = ['.svg', '.svgz']

# PDF文档结构（保留模板原有）
latex_documents = [
    (
        master_doc,
        "project.tex",
        "project 手册",
        "2025鸿之微科技（上海）股份有限公司",
        "manual",
    ),
]

# -- EPUB配置（模板原有）-------------------------------------------------------
epub_tocscope = "chapters"