# Getting started with `fave-recode`


![PyPI](https://img.shields.io/pypi/v/fave-recode.png)
[![codecov](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-recode/graph/badge.svg?token=C23B1H3DAX)](https://codecov.io/gh/Forced-Alignment-and-Vowel-Extraction/fave-recode)
[![Maintainability](https://api.codeclimate.com/v1/badges/2375ddfef5d77ba1681d/maintainability.png)](https://codeclimate.com/github/Forced-Alignment-and-Vowel-Extraction/fave-recode/maintainability)
[![FAVE Python
CI](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/test-and-run.yml/badge.svg?branch=dev)](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/test-and-run.yml)
[![Build
Docs](https://github.com/Forced-Alignment-and-Vowel-Extraction/fave-recode/actions/workflows/build-docs.yml/badge.svg)](https://forced-alignment-and-vowel-extraction.github.io/fave-recode/)
[![DOI](https://zenodo.org/badge/605740158.svg)](https://zenodo.org/badge/latestdoi/605740158)

The idea behind `fave-recode` is that no matter how much you may adjust
the dictionary of a forced-aligner, you may still want to make
programmatic changes to the output.

## Installation

You can install `fave-recode` at your system’s command line with `pip`.

``` bash
pip install fave-recode
```

## Basic usage

Installation of the `fave-recode` python package makes the `fave_recode`
executable, which can also be run at the command line. You can get help
with `--help`

``` bash
fave_recode --help
```

    Usage: fave_recode [OPTIONS]

    Inputs: [at least 1 required]
      File inputs. Either a single file with -i or a path with -p. Not both.
      -i, --input_file FILENAME  single input file
      -p, --input_path PATH      Path to a set of files

    Outputs:
      -o, --output_file TEXT     An output file name
      -d, --output_dest PATH     An output directory

    Other options:
      -a, --parser TEXT          Label set parser. Built in options are cmu_parser
      -s, --scheme TEXT          Recoding scheme. Built in options are cmu2labov
                                 and cmu2phila  [required]
      -r, --recode_stem TEXT     Stem to append to recoded TextGrid file names
      -t, --target_tier TEXT     Target tier to recode
      --help                     Show this message and exit.

To recode a single file, you need to provide `fave_recode` with,
minimally, the input file (the `-i` flag), and the recoding scheme (with
the `-s` flag). There are a few default recoding schemes that come with
`fave_recode`.

``` bash
ls data
```

    KY25A_1.TextGrid                 josef-fruehwald_speaker.TextGrid

``` bash
fave_recode -i data/josef-fruehwald_speaker.TextGrid -s cmu2phila -a cmu_parser

ls data
```

    KY25A_1.TextGrid
    josef-fruehwald_speaker.TextGrid
    josef-fruehwald_speaker_recoded.TextGrid
