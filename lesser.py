#!/usr/bin/env python3
# coding: utf-8


SUPPORTED_FORMATS = (
    "zip",
    "bz2", "bztwo",
    "gz", "gzip",
    "7z", "7zip", "sevenzip",
    "tar",
    "lzma",
    "rar",
    "zst", "zstd",
    "br", "brotli")

from pathlib import Path
from os import environ

from zipfile import ZipFile, ZIP_DEFLATED
from bz2 import BZ2File
from gzip import open as gzip_open
from py7zr import SevenZipFile
from tarfile import open as tar_open
from lzma import open as lzma_open
# 为了让 unrar 库读取 dll，暂时把它添加到环境变量中
environ["UNRAR_LIB_PATH"] = str(Path("unrar.dll").absolute())
from unrar.rarfile import RarFile
del environ["UNRAR_LIB_PATH"]
from pyzstd import ZstdFile
from brotli import compress as br_compress, decompress as br_decompress


# 获取程序运行参数
def getArgs():
    global ARGS
    from argparse import ArgumentParser
    from time import strftime

    parser = ArgumentParser(prog="lesser",
                            description="A command line compression software (using Python)",
                            epilog="For more information, please visit https://github.com/gpchn/lesser/README.md/")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-c", "--compress", action="store_true", help="Set compress mode.")
    mode_group.add_argument("-d", "--decompress", action="store_true", help="Set decompress mode.")

    format_group = parser.add_mutually_exclusive_group(required=True)
    format_group.add_argument("-f", "--format", choices=SUPPORTED_FORMATS, help="Set format. Choices include some different writing format, such as 'gz' and 'gzip'. They are the same in the code level.")
    format_subgroup = format_group.add_mutually_exclusive_group()
    format_subgroup.add_argument("--zip", action="store_true", help="Set zip format.")
    format_subgroup.add_argument("--bz2", action="store_true", help="Set bz2 format.")
    format_subgroup.add_argument("--gzip", action="store_true", help="Set gzip format.")
    format_subgroup.add_argument("--7zip", dest="sevenzip", action="store_true", help="Set 7zip format.")
    format_subgroup.add_argument("--tar", action="store_true", help="Set tar format.")
    format_subgroup.add_argument("--lzma", action="store_true", help="Set lzma format.")
    format_subgroup.add_argument("--rar", action="store_true", help="Set rar format.")
    format_subgroup.add_argument("--zstd", action="store_true", help="Set zstd format.")
    format_subgroup.add_argument("--brotli", action="store_true", help="Set brotli format.")
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input file path. In compress mode it should be the original file, and in decompress mode it should be the compressed file.")
    parser.add_argument("-o", "--output", type=Path, default=f"{strftime('%y%m%d-%H%M%S')}.zip", help="Output file path. In compress mode it should be the compressed file, and in decompress mode it should be the folder.")
    ARGS = parser.parse_args()


# 我知道这写法很烂，但我莫得选择（悲）
def main():
    if ARGS.compress:
        if ARGS.zip or ARGS.format == "zip":
            with ZipFile(ARGS.output, "w", ZIP_DEFLATED) as f:
                # 第二个参数 arcname 是为了避免把文件名储存为它的绝对路径
                f.write(ARGS.input, ARGS.input.name)
            end()
        if ARGS.bz2 or ARGS.format == "bz2":
            with BZ2File(ARGS.output, "wb") as f:
                with open(ARGS.input, "rb") as g:
                    f.write(g.read())
            end()
        if ARGS.gzip or ARGS.format in ("gz", "gzip"):
            with open(ARGS.input, "rb") as f:
                with gzip_open(ARGS.output, "wb") as g:
                    g.write(f.read())
            end()
        if ARGS.sevenzip or ARGS.format in ("7z", "7zip", "sevenzip"):
            with SevenZipFile(ARGS.output, "w")as f:
                f.writeall(ARGS.input)
            end()
        if ARGS.tar or ARGS.format == "tar":
            with tar_open(ARGS.output, "w") as f:
                f.add(ARGS.input)
            end()
        if ARGS.lzma or ARGS.format == "lzma":
            with open(ARGS.input, "rb") as f:
                with lzma_open(ARGS.output, "wb") as g:
                    g.write(f.read())
            end()
        if ARGS.rar or ARGS.format == "rar":
            print("Sorry, this program does not support rar compressed format.")
            exit(1)
        if ARGS.zstd or ARGS.format in ("zst", "zstd"):
            with ZstdFile(ARGS.output, "wb") as f:
                with open(ARGS.input, "rb") as g:
                    f.write(g.read())
            end()
        if ARGS.brotli or ARGS.format in ("br", "brotli"):
            with open(ARGS.output, "wb") as f:
                with open(ARGS.input, "rb") as g:
                    f.write(br_compress(g.read()))
            end()
        else:
            print(f"Sorry, this program does not support '{ARGS.format}' format yet.")
            print("To add support for this format, please open an issue in github. (https://github.com/gpchn/lesser/issues/new)")
            exit(1)

    elif ARGS.decompress:
        if ARGS.zip or ARGS.format == "zip":
            with ZipFile(ARGS.input, "r", ZIP_DEFLATED) as f:
                f.extractall(path=ARGS.output, members=f.namelist())
            end()
        if ARGS.bz2 or ARGS.format == "bz2":
            with BZ2File(ARGS.input, "rb") as f:
                with open(ARGS.output, "wb") as g:
                    g.write(f.read())
            end()
        if ARGS.gzip or ARGS.format in ("gz", "gzip"):
            with open(ARGS.output, "wb") as f:
                with gzip_open(ARGS.input, "rb") as g:
                    f.write(g.read())
            end()
        if ARGS.sevenzip or ARGS.format in ("7z", "sevenzip"):
            with SevenZipFile(ARGS.input) as f:
                f.extractall(ARGS.output)
            end()
        if ARGS.tar or ARGS.format == "tar":
            with tar_open(ARGS.input, "r") as f:
                f.extractall(ARGS.output)
            end()
        if ARGS.lzma or ARGS.format == "lzma":
            with lzma_open(ARGS.input, "rb") as f:
                with open(ARGS.output, "wb") as g:
                    g.write(f.read())
            end()
        if ARGS.rar or ARGS.format == "rar":
            with RarFile(ARGS.input) as f:
                f.extractall(ARGS.output)
            end()
        if ARGS.zstd or ARGS.format in ("zst", "zstd"):
            with ZstdFile(ARGS.input, "rb") as f:
                with open(ARGS.output, "wb") as g:
                    g.write(f.read())
            end()
        if ARGS.brotli or ARGS.format in ("br", "brotli"):
            with open(ARGS.input, "rb") as f:
                with open(ARGS.output, "wb") as g:
                    g.write(br_decompress(f.read()))
            end()
        else:
            print(f"Sorry, this program does not support '{ARGS.format}' format yet.")
            print("To add support for this format, please open an issue in github. (https://github.com/gpchn/lesser/issues/new)")
            exit(1)


def end():
    print("Execute successfully.")
    exit(0)


if __name__ == "__main__":
    getArgs()
    main()
