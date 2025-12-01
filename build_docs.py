# -*- coding: utf-8 -*-
"""文档编译自动化
为简化输出，
    网页编译过程日志输出到 making_preview.log,
    PDF编译过程日志输出到 making_tex.log, tex2pdf.log, tex2pdf_doctree.log
    EPUB编译过程日志输出到 making_epub.log
    MOBI编译过程日志输出到 mobi2epub.log

参考文献标题含有公式如果渲染失败，只能手动替换
"""

import argparse
import multiprocessing
import os
import sys
import shutil
from pathlib import Path
from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:MM-DD HH:mm:ss:SSS}</green> | <level>{message}</level>",
)


@logger.catch
def makePDF(project_name):
    """Checkout each branch and build PDFs"""
    pdf_output_dir = Path("build") / "pdf"
    if os.path.isdir(pdf_output_dir):
        shutil.rmtree(pdf_output_dir)
    logger.debug("编译PDF...")
    go(f"sphinx-build -b latex source {pdf_output_dir} > making_tex.log 2>&1")

    logger.debug("latex --> PDF...")
    # Now change to PDF directory for LaTeX compilation
    cwd = os.getcwd()
    os.chdir(pdf_output_dir)
    go(f"xelatex {project_name}.tex > {os.path.join(cwd, 'tex2pdf.log')}")

    logger.debug("PDF --> PDF with bookmarks...")
    go(f"xelatex {project_name}.tex > {os.path.join(cwd, 'tex2pdf_doctree.log')}")
    logger.info(f"📚 --> {pdf_output_dir}/{project_name}.pdf")
    os.chdir(cwd)


@logger.catch
def makeBooks(project_name):
    """Checkout each branch and build books"""
    book_output_dir = Path("build") / "books"
    if os.path.isdir(book_output_dir):
        shutil.rmtree(book_output_dir)
    logger.debug("编译EPUB...")
    go(f"sphinx-build -b epub source {book_output_dir} > making_epub.log 2>&1")
    logger.debug("epub --> mobi...")
    ebook_convert_location = shutil.which("ebook-convert")
    go(
        f"{ebook_convert_location} {os.path.join(book_output_dir, f'{project_name}.epub')} {os.path.join(book_output_dir, f'{project_name}.mobi')} > epub2mobi.log"
    )
    logger.info(f"📚 --> {book_output_dir}/{project_name}.epub/mobi")


@logger.catch
def preview(project_name):
    dst = Path("build") / "html"
    go(f"sphinx-build source {dst} > making_preview.log")
    logger.info(f"📚 --> {dst}")


@logger.catch
def go(cmd):
    logger.debug(cmd)
    return os.system(cmd)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="请在主目录下运行")
    argparser.add_argument(
        "-c", "--clean", action="store_true", help="清空整个build目录"
    )
    argparser.add_argument("-p", "--preview", action="store_true", help="编译预览网页")
    argparser.add_argument(
        "-b", "--books", action="store_true", help="编译EPUB, MOBI电子书"
    )
    argparser.add_argument("-l", "--latex", action="store_true", help="编译PDF")
    argparser.add_argument("-v", action="store_true", help="verbose")

    args = argparser.parse_args()
    # if no args, do all
    if not any(vars(args).values()):
        default = True
    else:
        default = False

    if args.v:
        verbose = True
    else:
        verbose = False

    rst_source_dir = "source"
    build_dir = "build"

    # get the project debug by sphinx-build
    confpy = os.path.join(rst_source_dir, "conf.py")

    go(f"ruff format {confpy}")  # format conf.py so that it can be parsed
    project_name = None
    with open(f"{confpy}", encoding="utf-8") as file:
        for line in file:
            if line.startswith("project = "):
                project_name = (
                    line.split("=")[1].strip().strip('"')
                )  # DS-PAW or RESCU ...
                break

    logger.info(f"🌀 项目名称：{project_name}")
    assert project_name is not None, "project name not found in conf.py"

    if args.clean:
        logger.warning(f"清空 {build_dir} 目录...")
        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir)

    if args.preview:
        logger.debug("🚀 预览...")
        preview(project_name)
    if args.books:
        logger.debug("🚀 编译电子书...")
        makeBooks(project_name)
    if args.latex:
        logger.debug("🚀 编译latex PDF...")
        makePDF(project_name)

    if default:
        multiprocessing.freeze_support()
        logger.debug("🚀 编译 EPUB, MOBI, PDF & html...")
        # old pdf, books do not need to be rebuilt
        p1 = multiprocessing.Process(target=makeBooks, args=(project_name,))
        p2 = multiprocessing.Process(target=makePDF, args=(project_name,))
        p3 = multiprocessing.Process(target=preview, args=(project_name,))
        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

        logger.info("--> ✅ EPUB, MOBI, PDF, html 编译完成！")
