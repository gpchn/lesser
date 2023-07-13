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
    "br", "brotli",
    "xz", "xzip")

from pathlib import Path
from os import environ

from zipfile import ZipFile, ZIP_DEFLATED
from zipfile_xz import ZipFile as XzipFile, ZIP_XZ
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
def getargs():
    global args
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
    format_subgroup.add_argument("--xzip", action="store_true", help="Set xzip format.")
    parser.add_argument("-i", "--input", type=Path, required=True, help="Input file path. In compress mode it should be the original file, and in decompress mode it should be the compressed file.")
    parser.add_argument("-o", "--output", type=Path, default=f"{strftime('%y%m%d-%H%M%S')}.zip", help="Output file path. In compress mode it should be the compressed file, and in decompress mode it should be the folder.")
    args = parser.parse_args()


# 我知道这写法很烂，但我莫得选择（悲）
# match-case 在这用不了，因为有 in 判断
def main():
    if args.compress:
        if args.zip or args.format == "zip":
            with ZipFile(args.output, "w", ZIP_DEFLATED) as f:
                # 第二个参数 arcname 是为了避免把文件名储存为它的绝对路径
                f.write(args.input, args.input.name)
            
        elif args.bz2 or args.format == "bz2":
            with BZ2File(args.output, "wb") as f:
                with open(args.input, "rb") as g:
                    f.write(g.read())
            
        elif args.gzip or args.format in ("gz", "gzip"):
            with open(args.input, "rb") as f:
                with gzip_open(args.output, "wb") as g:
                    g.write(f.read())
            
        elif args.sevenzip or args.format in ("7z", "7zip", "sevenzip"):
            with SevenZipFile(args.output, "w")as f:
                f.writeall(args.input)
            
        elif args.tar or args.format == "tar":
            with tar_open(args.output, "w") as f:
                f.add(args.input)
            
        elif args.lzma or args.format == "lzma":
            with open(args.input, "rb") as f:
                with lzma_open(args.output, "wb") as g:
                    g.write(f.read())
            
        elif args.rar or args.format == "rar":
            print("Sorry, this program does not support rar compressed format.")
            exit(1)
        elif args.zstd or args.format in ("zst", "zstd"):
            with ZstdFile(args.output, "wb") as f:
                with open(args.input, "rb") as g:
                    f.write(g.read())
            
        elif args.brotli or args.format in ("br", "brotli"):
            with open(args.output, "wb") as f:
                with open(args.input, "rb") as g:
                    f.write(br_compress(g.read()))
            
        elif args.xzip or args.format in ("xz", "xzip"):
            with XzipFile(args.output, "w", ZIP_XZ) as f:
                f.write(args.input, args.input.name)
            
        else:
            print(f"Sorry, this program does not support '{args.format}' format yet.")
            print("To add support for this format, please open an issue in github. (https://github.com/gpchn/lesser/issues/new)")
            exit(1)

    elif args.decompress:
        if args.zip or args.format == "zip":
            with ZipFile(args.input, "r", ZIP_DEFLATED) as f:
                f.extractall(path=args.output, members=f.namelist())
            
        elif args.bz2 or args.format == "bz2":
            with BZ2File(args.input, "rb") as f:
                with open(args.output, "wb") as g:
                    g.write(f.read())
            
        elif args.gzip or args.format in ("gz", "gzip"):
            with open(args.output, "wb") as f:
                with gzip_open(args.input, "rb") as g:
                    f.write(g.read())
            
        elif args.sevenzip or args.format in ("7z", "sevenzip"):
            with SevenZipFile(args.input) as f:
                f.extractall(args.output)
            
        elif args.tar or args.format == "tar":
            with tar_open(args.input, "r") as f:
                f.extractall(args.output)
            
        elif args.lzma or args.format == "lzma":
            with lzma_open(args.input, "rb") as f:
                with open(args.output, "wb") as g:
                    g.write(f.read())
            
        elif args.rar or args.format == "rar":
            with RarFile(args.input) as f:
                f.extractall(args.output)
            
        elif args.zstd or args.format in ("zst", "zstd"):
            with ZstdFile(args.input, "rb") as f:
                with open(args.output, "wb") as g:
                    g.write(f.read())
            
        elif args.brotli or args.format in ("br", "brotli"):
            with open(args.input, "rb") as f:
                with open(args.output, "wb") as g:
                    g.write(br_decompress(f.read()))
            
        elif args.xzip or args.format in ("xz", "xzip"):
            with XzipFile(args.input, "r", ZIP_XZ) as f:
                f.extractall(path=args.output, members=f.namelist())
            
        else:
            print(f"Sorry, this program does not support '{args.format}' format yet.")
            print("To add support for this format, please open an issue in github. (https://github.com/gpchn/lesser/issues/new)")
            exit(1)

        print("Execute successfully.")


if __name__ == "__main__":
    getargs()
    main()