# lesser.py

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![GitHub pull requests](https://img.shields.io/github/issues-pr/gpchn/lesser)
![GitHub issues](https://img.shields.io/github/issues/gpchn/lesser)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/gpchn/lesser)

lesser.py 是一个命令行压缩、解压缩软件

现代压缩软件有很多不错的选择，例如 7-zip、Bandizip 等（我本人更喜欢 Bandizip）。lesser 是一个更接近于“玩具”的小脚本，没有什么技术含量。

## 内容列表

- [安装](#安装)
- [使用说明](#使用说明)
  - [参数解读](#参数解读)
  - [例子](#例子)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 安装

这个项目使用 [Python3](http://www.python.org/)。如果要运行源代码，请确保你本地安装了它们，并且也安装了[依赖库](requirements.txt)

```shell
# 安装 Python3
$ sudo apt install python3
# 使用 pip 安装依赖库（前提是已经安装 pip）
$ pip install -r requirements.txt
```

## 使用说明

lesser 是一个命令行程序，你需要打开命令行来使用它。使用 `-h` 或 `--help` 参数来获取使用方法：

```shell
$ python3 lesser.py -h
usage: lesser [-h] (-c | -d) [-z | -b | -g | -s | -t | -l | -r] -i INPUT [-o OUTPUT]

A command line compression software (using Python)

options:
  -h, --help            show this help message and exit
  -c, --compress        Set compress mode.
  -d, --decompress      Set decompress mode.
  -z, --zip             Set zip format.
  -b, --bz2             Set bz2 format.
  -g, --gzip            Set gzip format.
  -s, --sevenzip        Set 7zip format.
  -t, --tar             Set tar format.
  -l, --lzma            Set lzma format.
  -r, --rar             Set rar format.
  -i INPUT, --input INPUT
                        Input file path. In compress mode it should be the original file, and in decompress mode it
                        should be the compressed file.
  -o OUTPUT, --output OUTPUT
                        Output file path. In compress mode it should be the compressed file, and in decompress mode
                        it should be the decompressed file's name or the folder of decompressed files.
```

### 参数解读

一个一个来：

`-c` 和 `-d`：这两个是指定模式，压缩（compress）和解压缩（decompress）。

`-z`、`-b`、`-g`、`-s`、`-t`、`-l`、`-r`：都表示压缩格式。lesser 支持以下格式：

|      | 压缩  | 解压  |
| ---- | --- | --- |
| zip  | √   | √   |
| bz2  | √   | √   |
| gzip | √   | √   |
| 7zip | √   | √   |
| tar  | √   | √   |
| lzma | √   | √   |
| rar  |     | √   |

`-i` 和 `-o`：输入和输出，表示提供输入文件和输出文件（夹）。其中 `-i` 是必要参数，`-o` 可以不指定，默认是格式化时间 `%y%m%d-%H%M%S.zip` ，例如 `230708-020158.zip`

压缩模式下 `-i` 表示未压缩文件，解压模式下 `-i` 表示压缩文件；压缩模式下 `-o` 表示生成的压缩文件名，解压模式下 `-o` 表示解压出文件的文件名，或存放解压文件的文件夹

~~关于这点，由于每个压缩格式都要使用一个第三方库，而每个压缩格式的特性和第三方库的用法都不大相同，我自己都分不清这个 `-o` 什么时候代表文件名，什么时候代表文件夹……feature，这是个 feature！（悲）~~

### 例子

```shell
# 使用 zip 格式，压缩 movie.mp4
$ python3 lesser.py -czi movie.mp4
# 使用 bz2 格式，把 app.zip 中的内容解压到 app 文件夹中
$ python3 lesser.py -dbi app.zip -o movie.mp4
```

## 维护者

[@gpchn](https://github.com/gpchn)

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/gpchn/lesser/issues/new) 或者提交一个 Pull Request。

## 使用许可

[Apache 2.0](LICENSE) © gpchn