# Standard Readme

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![GitHub pull requests](https://img.shields.io/github/issues-pr/gpchn/lesser)
![GitHub issues](https://img.shields.io/github/issues/gpchn/lesser)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/gpchn/lesser)

Lesser.py is a command line compression and decompression software.

There are many good options for modern compression software, such as 7-zip, Bandizip, etc. (I personally prefer Bandizip). Lesser is a small script that is closer to a 'toy' and lacks much technical content.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
  - [Arguments](#arguments)
  - [Examples](#Examples)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Install

This project uses [Python3](http://www.python.org/). If you want to run the source code, please ensure that you have installed them locally and also installed the [requirements](requirements.txt)

```shell
# Install Python3
$ sudo apt install python3
# Use pip to install the requirements (Must installed pip)
$ pip install -r requirements.txt
```

## Usage

Lesser is a command-line program that you need to open your terminal to use. Use the `-h` or `--help` parameters to obtain the usage method:

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

### Arguments

One by one:

`-C` and `-d`: These two are the specified modes, compression and decompression.
`-Z `, ` - b `, ` - g `, ` - s `, ` - t `, ` - l `, ` - r `: all represent compressed formats. Lesser supports the following formats:

|      | Compress | Decompress |
| ---- | -------- | ---------- |
| zip  | √        | √          |
| bz2  | √        | √          |
| gzip | √        | √          |
| 7zip | √        | √          |
| tar  | √        | √          |
| lzma | √        | √          |
| rar  |          | √          |

`-i` and `-o`: Input and output, indicating the provision of input and output files (folders). Among them, `-i` is a necessary parameter, and `-o` can be left unspecified. The default is the formatting time of `%y%m%d-%H%M%S.zip`, for example,`230708-020158.zip`.
In compression mode, `-i` represents uncompressed files, while in decompression mode, `-i` represents compressed files; In compression mode, `-o` represents the generated compressed file name, while in decompression mode, `-o` represents the file name of the extracted file or the folder where the extracted file is stored.

~~Regarding this point, as each compression format requires the use of a third-party library, and the characteristics and usage of each compression format are not the same, I cannot distinguish when this' - o 'represents a file name and when it represents a folder... A feature, this is a feature!~~

### Examples

```shell
# Use zip format, compress movie.mp4
$ python3 lesser.py -czi movie.mp4
# Use bz2 format, decompress files of app.zip into app folder
$ python3 lesser.py -dbi app.zip -o movie.mp4
```

## Maintainers

[@gpchn](https://github.com/gpchn)

## Contributing

Feel free to dive in! [Open an issue](https://github.com/gpchn/lesser/issues/new) or submit PRs.

## License

[Apache 2.0](LICENSE) © gpchn
