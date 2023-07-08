#!/usr/bin/env python3
# coding: utf-8


from pathlib import Path
from os import environ
# 程序支持 zip, bz2, gz, 7z, tar, lzma 压缩和解压缩，rar 只能解压
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


# 获取程序运行参数
def getArgs():
    global ARGS
    from argparse import ArgumentParser
    from time import strftime

    parser = ArgumentParser(prog="lesser", description="A command line compression software (using Python)")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-c", "--compress", action="store_true", help="Set compress mode.")
    mode_group.add_argument("-d", "--decompress", action="store_true", help="Set decompress mode.")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("-z", "--zip", action="store_true", help="Set zip format.")
    format_group.add_argument("-b", "--bz2", action="store_true", help="Set bz2 format.")
    format_group.add_argument("-g", "--gzip", action="store_true", help="Set gzip format.")
    format_group.add_argument("-s", "--sevenzip", action="store_true", help="Set 7zip format.")
    format_group.add_argument("-t", "--tar", action="store_true", help="Set tar format.")
    format_group.add_argument("-l", "--lzma", action="store_true", help="Set lzma format.")
    format_group.add_argument("-r", "--rar", action="store_true", help="Set rar format.")
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input file path. In compress mode it should be the original file, and in decompress mode it should be the compressed file.")
    parser.add_argument("-o", "--output", type=Path, default=f"{strftime('%y%m%d-%H%M%S')}.zip", help="Output file path. In compress mode it should be the compressed file, and in decompress mode it should be the folder.")
    ARGS = parser.parse_args()


def main():
    getArgs()

    if ARGS.compress:
        match True:
            case ARGS.zip:
                with ZipFile(ARGS.output, "w", ZIP_DEFLATED) as f:
                    # 第二个参数 arcname 是为了避免把文件名储存为它的绝对路径
                    f.write(ARGS.input, ARGS.input.name)
            case ARGS.bz2:
                with BZ2File(ARGS.output, "wb") as f:
                    with open(ARGS.input, "rb") as g:
                        f.write(g.read())
            case ARGS.gzip:
                with open(ARGS.input, "rb") as f:
                    with gzip_open(ARGS.output, "wb") as g:
                        g.write(f.read())
            case ARGS.sevenzip:
                with SevenZipFile(ARGS.output, "w")as f:
                    f.writeall(ARGS.input)
            case ARGS.tar:
                with tar_open(ARGS.output, "w") as f:
                    f.add(ARGS.input)
            case ARGS.lzma:
                with open(ARGS.input, "rb") as f:
                    with lzma_open(ARGS.output, "wb") as g:
                        g.write(f.read())
            case ARGS.rar:
                print("Sorry, this program does not support rar compressed format.")
                exit(1)

    elif ARGS.decompress:
        match True:
            case ARGS.zip:
                with ZipFile(ARGS.input, "r", ZIP_DEFLATED) as f:
                    f.extractall(path=ARGS.output, members=f.namelist())
            case ARGS.bz2:
                    with BZ2File(ARGS.input, "rb") as f:
                        with open(ARGS.output, "wb") as g:
                            g.write(f.read())
            case ARGS.gzip:
                with open(ARGS.output, "wb") as f:
                    with gzip_open(ARGS.input, "rb") as g:
                        f.write(g.read())
            case ARGS.sevenzip:
                with SevenZipFile(ARGS.input) as f:
                    f.extractall(ARGS.output)
            case ARGS.tar:
                with tar_open(ARGS.input, "r") as f:
                    f.extractall(ARGS.output)
            case ARGS.lzma:
                with lzma_open(ARGS.input, "rb") as f:
                    with open(ARGS.output, "wb") as g:
                        g.write(f.read())
            case ARGS.rar:
                with RarFile(ARGS.input) as f:
                    f.extractall(ARGS.output)


if __name__ == "__main__":
    main()
