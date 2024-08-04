# RetroFreak Toolkit NES Rom Decryption Bug Fix

This is an update to the original encrypt / decrypt logic with bug fix to handle NES / Famicom rom dump

##### Requirements:
* Python 3
* Pycryptodomex >= 3.9.0

##### RetroFreakROM.py
This file is used to encrypt/decrypt ROM's so you can play them on your RetroFreak or PC.

##### RetroFreakROM.py Usage:
```
usage: RetroFreakROM.py [-h] [-o O] [-s SERIAL] [-k KEYFILE] ifile

A script to encrypt/decrypt ROM's to/from the RetroFreak

positional arguments:
  ifile                 The ROM to read from

optional arguments:
  -h, --help            show this help message and exit
  -o O                  The ROM file to write to
  -s SERIAL, --serial SERIAL
                        The serial number you want to use
  -k KEYFILE, --keyfile KEYFILE
                        The serial number you want to use saved in serial.txt
```

##### Credits:
> [RedScoripoXDA](https://forum.xda-developers.com/member.php?u=4582467) for [imgRePackerRK](https://forum.xda-developers.com/showthread.php?t=2257331)
