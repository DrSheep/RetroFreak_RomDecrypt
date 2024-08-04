# RetroFreak Toolkit

This is a toolkit intended to help players root their RetroFreak console to get more features out of it.

The RetroFreak has an rk3066 SoC and uses the Rockchip image format for updates; these updates can be modified and repackaged using imgRePackerRK.

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
